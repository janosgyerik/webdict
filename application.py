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


class FindByExact(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find(keyword, find_similar=True)
        return self.get_response(entries)


class FindByPrefix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_prefix(keyword, find_similar=True)[:MAX_RESULTS]
        return self.get_response(entries)


class FindBySuffix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_suffix(keyword)[:MAX_RESULTS]
        return self.get_response(entries)


class FindByFragment(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_fragment(keyword)[:MAX_RESULTS]
        return self.get_response(entries)


class GetEntry(AmericanHeritageDictionaryResults):
    def get(self, entry_id):
        entries = dictionary.get_entry(entry_id)
        return self.get_response(entries)


api_baseurl = '/api/v1/dictionaries'
# api.add_resource(GetDictionaries, api_baseurl + '/')

for dict_id in ('ahd',):
    api.add_resource(FindByExact, '{}/{}/find/exact/<string:keyword>'.format(api_baseurl, dict_id))
    api.add_resource(FindByPrefix, '{}/{}/find/prefix/<string:keyword>'.format(api_baseurl, dict_id))
    api.add_resource(FindBySuffix, '{}/{}/find/suffix/<string:keyword>'.format(api_baseurl, dict_id))
    api.add_resource(FindByFragment, '{}/{}/find/partial/<string:keyword>'.format(api_baseurl, dict_id))
    api.add_resource(GetEntry, '{}/{}/get/entry/<path:entry_id>'.format(api_baseurl, dict_id))

if __name__ == '__main__':
    app.run()
