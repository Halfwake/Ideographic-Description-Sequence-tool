from flask import Flask
from flask import request
from flask import render_template, url_for, redirect

from find import search_components, IDS_FILE_NAME
from find import load as find_load

app = Flask(__name__)

inited = False
def check_init():
    global inited
    if not inited:
        with open(IDS_FILE_NAME, encoding="utf-8") as f_obj:
            find_load(f_obj)
        inited = True

@app.route('/', methods = ['GET'])
def index():
    check_init()
    return render_template("index.html")

@app.route('/find', methods = ['GET'])
def find():
    check_init()
    lookup = request.args.get('lookup')
    reverse = request.args.get('reverse')
    norecurse = request.args.get('norecurse')
    if lookup:
        with open(IDS_FILE_NAME, encoding="utf-8") as f_obj:
            output = '\n'.join(search_components(lookup, reverse = (reverse == 'on'), norecurse = (norecurse == 'on')))
            reverse_checked = "checked"
            if reverse != 'on':
                reverse_checked = ""
            norecurse_checked = "checked"
            if norecurse != 'on':
                norecurse_checked = ""
            print(output)
            return render_template("index.html", lookup = lookup, output = output, reverse_checked = reverse_checked, norecurse_checked = norecurse_checked)
    else:
        return 'Invalid Query Parameters'

if __name__ == '__main__':
    app.run()
