#!/usr/bin/env python

from flask import Flask, request, url_for, redirect, render_template
app = Flask(__name__)

import simplejson as json
import english

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET'])
def query():
    keyword = request.args.get('keyword', '')
    filename = request.args.get('file', '')
    if keyword:
        words = [x for x in english.find(keyword)]
        if len(words):
            similar = []
        else:
            similar = english.similar(keyword)
        return json.dumps({
            'words': words,
            'similar': similar,
            }, indent=4)
    elif filename:
        return json.dumps([english.get(filename)])

@app.route('/st')
def st():
    return redirect(url_for('static', filename='css/english.css'))

if __name__ == '__main__':
    app.run()


# eof
