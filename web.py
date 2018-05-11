from flask import Flask
from flask import request
from flask import render_template, url_for, redirect

from find import search_components, IDS_FILE_NAME

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/find', methods = ['GET'])
def find():
    lookup = request.args.get('lookup')
    reverse = request.args.get('reverse')
    norecurse = request.args.get('norecurse')
    if lookup:
        with open(IDS_FILE_NAME, encoding="utf-8") as f_obj:
            return '\n'.join(search_components(f_obj, lookup, reverse = (reverse == 'on'), norecurse = (norecurse == 'on')))
    else:
        return 'Invalid Query Parameters'

if __name__ == '__main__':
    app.run()
