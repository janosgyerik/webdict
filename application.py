#!/usr/bin/env python

from flask import Flask, render_template, jsonify
from flask.ext.restful import Resource, Api

from plugins.ahd.ahd import AmericanHeritageDictionary

app = Flask(__name__)
api = Api(app)

dictionary = AmericanHeritageDictionary()

MAX_RESULTS = 10


@app.route('/')
def index():
    return render_template('index.html')


class AmericanHeritageDictionaryResults(Resource):
    def get_serializable_entries(self, entries):
        return [x.content for x in entries]

    def get_response(self, entries):
        return jsonify({
            'version': 'v1',
            'success': True,
            'matches': [{
                'dict': 'ahd',
                'format': 'dl-md',
                'entries': self.get_serializable_entries(entries)
            }]
        })


class SearchByExact(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find(keyword, find_similar=True)
        return self.get_response(entries)


class SearchByPrefix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_prefix(keyword, find_similar=True)[:MAX_RESULTS]
        return self.get_response(entries)


class SearchBySuffix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_suffix(keyword)[:MAX_RESULTS]
        return self.get_response(entries)


class SearchByFragment(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_fragment(keyword)[:MAX_RESULTS]
        return self.get_response(entries)


class GetEntry(AmericanHeritageDictionaryResults):
    def get(self, entry_id):
        entries = dictionary.get(entry_id)
        return self.get_response(entries)


api.add_resource(SearchByExact, '/search/exact/<string:keyword>')
api.add_resource(SearchByPrefix, '/search/prefix/<string:keyword>')
api.add_resource(SearchBySuffix, '/search/suffix/<string:keyword>')
api.add_resource(SearchByFragment, '/search/partial/<string:keyword>')
api.add_resource(GetEntry, '/entry/<path:entry_id>')

if __name__ == '__main__':
    app.run()
