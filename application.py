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


class GetEntry(Resource):
    def get(self, entry_id):
        return json.dumps({'words': [english.get(entry_id)], 'similar': [], }, indent=4)


api.add_resource(SearchByExact, '/search/exact/<string:keyword>')
# api.add_resource(SearchByPrefix, '/search/prefix/<string:keyword>')
# api.add_resource(SearchBySuffix, '/search/suffix/<string:keyword>')
# api.add_resource(SearchByPartial, '/search/partial/<string:keyword>')
api.add_resource(GetEntry, '/entry/<path:entry_id>')


if __name__ == '__main__':
    app.run()
