#!python
# coding=utf-8

# Get ids.txt from https://github.com/cjkvi/cjkvi-ids/ and place it next to this script
# ~requires python 3.6 or newer on windows~
# note: depends on the accuracy of ids.txt. for some characters, like 祭, it's pretty bad.
# see also: http://www.chise.org/ids-find

contains_forward = {}
contains_reverse = {}
common_set = set()

def is_descriptor(c):
    c = ord(c)
    return c >= 0x2FF0 and c <= 0x2FFB

import sys, re

def find_recursive(c, first, reverse, norecurse):
    recurse = set()
    if not reverse:
        mycontains = contains_forward
    else:
        mycontains = contains_reverse
    if c in mycontains and (first or not norecurse):
        if not first:
            recurse = recurse | set([c])
        for n in mycontains[c]:
            recurse = recurse | find_recursive(n, False, reverse, norecurse)
    else:
        recurse = recurse | set([c])
    return recurse

def find_string(string, reverse, norecurse):
    string = string.strip()
    sets = []
    for char in string:
        myset = find_recursive(char, True, reverse, norecurse)
        sets += [myset]
    
    myset = sets[0]
    for nextset in sets:
        myset = myset & nextset
    return myset

def force_print(string):
    sys.stdout.buffer.write(string.encode("utf-8"))

IDS_FILE_NAME = 'ids.txt'
COMMON_FILE_NAME = 'likely.txt'

def load(f_obj):
    global contains_forward, contains_reverse
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
            
            if c not in contains_forward:
                contains_forward[c] = set()
            contains_forward[c].add(char)
            
            if char not in contains_reverse:
                contains_reverse[char] = set()
            contains_reverse[char].add(c)


def load_common(f_obj):
    global common_set
    for s in f_obj:
        s = s.strip()
        if s != "":
            common_set.add(s)

def search_components(lookup_char, reverse = False, norecurse = False, common = False):
    ret = sorted(find_string(lookup_char, reverse, norecurse))
    if common and not reverse:
        oldret = ret
        ret = []
        for n in oldret:
            if n in common_set:
                ret += [n]
    return ret

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ideographic Description Sequence tool")
    parser.add_argument("lookup_char", help="String of components to find in characters.")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true", help="Decompose instead of compose.")
    parser.add_argument("-n", "--norecurse", dest="norecurse", action="store_true", help="First level of recursion only.")
    parser.add_argument("-c", "--common", dest="norecurse", action="store_true", help="First level of recursion only.")
    args = parser.parse_args()
    with open(IDS_FILE_NAME, encoding="utf-8") as f_obj:
        load(f_obj)
    with open(COMMON_FILE_NAME, encoding="utf-8") as f_obj:
        load_common(f_obj)
    force_print("\n".join(search_components(args.lookup_char, args.reverse, args.norecurse)))

