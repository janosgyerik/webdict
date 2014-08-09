#!/usr/bin/env python

from flask import Flask, render_template, jsonify
from flask.ext.restful import Resource, Api, reqparse

import os
from imp import find_module, load_module

from dictionary.base import lazy_property

PLUGINS_PATH = 'plugins'
MAX_RESULTS = 10

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('similar', type=bool, help='Try to find similar matches when there are no exact')
parser.add_argument('list', type=bool, help='Show list of matches instead of content')


def discover_dictionaries():
    import plugins
    for plugin_name in os.listdir(PLUGINS_PATH):
        plugin_path = os.path.join(PLUGINS_PATH, plugin_name, plugin_name + '.py')
        if os.path.isfile(plugin_path):
            try:
                fp, pathname, description = find_module(plugin_name, plugins.__path__)
                m1 = load_module(plugin_name, fp, pathname, description)
                fp, pathname, description = find_module(plugin_name, m1.__path__)
                m2 = load_module(plugin_name, fp, pathname, description)
                class_ = getattr(m2, 'Dictionary')
                yield plugin_name, class_()
            except ImportError:
                print('Error: could not import Dictionary from {}'.format(plugin_path))


@app.route('/')
def index():
    return render_template('index.html')


class DictionaryResource(Resource):
    @lazy_property
    def args(self):
        return parser.parse_args()

    @property
    def dictionary(self):
        """Dynamically when creating subclass using type()"""
        return None

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


class FindByExact(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find(keyword, find_similar=self.args['similar'])
        return self.get_response(entries, list_only=self.args['list'])


class FindByPrefix(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_prefix(keyword, find_similar=self.args['similar'])[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindBySuffix(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_suffix(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindByFragment(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_fragment(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class GetEntry(DictionaryResource):
    def get(self, entry_id):
        entries = self.dictionary.get_entry(entry_id)
        return self.get_response(entries)


api_baseurl = '/api/v1/dictionaries'
# api.add_resource(GetDictionaries, api_baseurl + '/')


def add_resource(cname, url_template, dict_id, dictionary):
    subclass = type(dict_id + cname.__name__, (cname,), {'dictionary': dictionary})
    api.add_resource(subclass, url_template.format(api_baseurl, dict_id))


def register_dictionary_endpoints():
    for dict_id, dictionary in discover_dictionaries():
        add_resource(FindByExact, '{}/{}/find/exact/<string:keyword>', dict_id, dictionary)
        add_resource(FindByPrefix, '{}/{}/find/prefix/<string:keyword>', dict_id, dictionary)
        add_resource(FindBySuffix, '{}/{}/find/suffix/<string:keyword>', dict_id, dictionary)
        add_resource(FindByFragment, '{}/{}/find/partial/<string:keyword>', dict_id, dictionary)
        add_resource(GetEntry, '{}/{}/get/entry/<path:entry_id>', dict_id, dictionary)

if __name__ == '__main__':
    register_dictionary_endpoints()
    app.run()
