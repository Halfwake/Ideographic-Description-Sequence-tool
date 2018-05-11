#!python
# coding=utf-8

# Get ids.txt from https://github.com/cjkvi/cjkvi-ids/ and place it next to this script
# ~requires python 3.6 or newer on windows~
# note: depends on the accuracy of ids.txt. for some characters, like 祭, it's pretty bad.
# see also: http://www.chise.org/ids-find

contains = {}

def is_descriptor(c):
    c = ord(c)
    if c < 0x2FF0 or c > 0x2FFB:
        return False
    else:
        return True

import argparse, sys, re

def find_recursive(c, first=True, norecurse = False):
    recurse = set()
    if c in contains and (first or not norecurse):
        if not first:
            recurse = recurse | set([c])
        for n in contains[c]:
            recurse = recurse | find_recursive(n, False)
    else:
        recurse = recurse | set([c])
    return recurse

def find_string(string, norecurse):
    string = string.strip()
    sets = []
    for char in string:
        myset = find_recursive(char, norecurse)
        sets += [myset]
    
    myset = sets[0]
    for nextset in sets:
        myset = myset & nextset
    return myset

def force_print(string):
    sys.stdout.buffer.write(string.encode("utf-8"))

IDS_FILE_NAME = 'ids.txt'
    
def search_components(f_obj, lookup_char, reverse = False, norecurse = False):
    for s in f_obj:
        s = re.sub(r"\[[^\]]*\]", "", s)
        fields = s.split("\t")
        if len(fields) < 3:
            continue
        char = fields[1].strip()
        # fields 2+ are each particular decompositions
        ids = "".join(fields[2:]).strip()
        for c in ids:
            if is_descriptor(c):
                continue
            if c == char:
                continue
            if not reverse:
                if c not in contains:
                    contains[c] = set()
                contains[c].add(char)
            else:
                if char not in contains:
                    contains[char] = set()
                contains[char].add(c)
    
        return sorted(find_string(lookup_char, norecurse))
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Ideographic Description Sequence tool")
    parser.add_argument("lookup_char", help="String of components to find in characters.")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true", help="Decompose instead of compose.")
    parser.add_argument("-n", "--norecurse", dest="norecurse", action="store_true", help="First level of recursion only.")    
    args = parser.parse_args()    
    with open(IDS_FILE_NAME, encoding="utf-8") as f_obj:
        force_print("\n".join(search_components(f_obj, args.lookup_char, args.reverse, args.norecurse)))
                        
