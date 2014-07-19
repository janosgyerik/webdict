#!/usr/bin/env python

from flask import Flask, request, render_template

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
        return json.dumps({'words': words, 'similar': similar, }, indent=4)
    elif filename:
        return json.dumps({'words': [english.get(filename)], 'similar': [], }, indent=4)


if __name__ == '__main__':
    app.run()
