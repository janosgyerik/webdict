#!/usr/bin/env python

from flask import Flask, request, render_template
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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


class SearchByExact(Resource):
    def get(self, keyword):
        words = [x for x in english.find(keyword)]
        if len(words):
            similar = []
        else:
            similar = english.similar(keyword)
        return json.dumps({'words': words, 'similar': similar, }, indent=4)


'''
/search/exact
/search/prefix
/search/suffix
/search/partial
/entry
'''
api.add_resource(SearchByExact, '/search/exact/<string:keyword>')


if __name__ == '__main__':
    app.run()
