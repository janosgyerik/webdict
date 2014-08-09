#!/usr/bin/env python

from flask import Flask, render_template, jsonify
from flask.ext.restful import Resource, Api, reqparse

from dictionary.base import lazy_property
from plugins.ahd.ahd import AmericanHeritageDictionary

app = Flask(__name__)
api = Api(app)

dictionary = AmericanHeritageDictionary()

MAX_RESULTS = 10


parser = reqparse.RequestParser()
parser.add_argument('similar', type=bool, help='Try to find similar matches when there are no exact')
parser.add_argument('list', type=bool, help='Show list of matches instead of content')


@app.route('/')
def index():
    return render_template('index.html')


class AmericanHeritageDictionaryResults(Resource):
    @lazy_property
    def args(self):
        return parser.parse_args()

    @staticmethod
    def get_serializable_entries(entries):
        return [x.content for x in entries]

    @staticmethod
    def get_json_entries(serializable_entries):
        return jsonify({
            'version': 'v1',
            'success': True,
            'matches': [{
                'dict': 'ahd',
                'format': 'dl-md',
                'entries': serializable_entries,
            }]
        })

    def get_entries(self, entries):
        return self.get_json_entries(self.get_serializable_entries(entries))

    def get_entries_without_content(self, entries):
        return self.get_json_entries([{'id': x.entry_id, 'name': x.name} for x in entries])

    def get_response(self, entries, list_only=False):
        if list_only:
            return self.get_entries_without_content(entries)
        return self.get_entries(entries)


class FindByExact(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find(keyword, find_similar=self.args['similar'])
        return self.get_response(entries, list_only=self.args['list'])


class FindByPrefix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_prefix(keyword, find_similar=self.args['similar'])[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindBySuffix(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_suffix(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindByFragment(AmericanHeritageDictionaryResults):
    def get(self, keyword):
        entries = dictionary.find_by_fragment(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


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
