#!/usr/bin/env python

from flask import Flask, render_template, jsonify
from flask.ext.restful import Resource, Api, reqparse

from dictionary.base import lazy_property
from util import discover_dictionaries


MAX_RESULTS = 10

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('similar', type=bool,
                    help='Try to find similar matches when there are no exact')
parser.add_argument('list', type=bool,
                    help='Show list of matches instead of content')

dictionaries = [_ for _ in discover_dictionaries()]


class DictionaryResource(Resource):
    @lazy_property
    def args(self):
        return parser.parse_args()

    @property
    def dict_id(self):
        """Dynamically set when creating subclass using type()"""
        return None

    @property
    def dictionary(self):
        """Dynamically set when creating subclass using type()"""
        return None

    @staticmethod
    def get_serializable_entries(entries):
        return [x.content for x in entries]

    def get_json_entries(self, serializable_entries):
        return jsonify({
            'matches': [
                {
                    'dict': self.dict_id,
                    'format': 'dl-md',
                    'entries': serializable_entries,
                }]
        })

    def get_entries(self, entries):
        return self.get_json_entries(self.get_serializable_entries(entries))

    def get_entries_without_content(self, entries):
        return self.get_json_entries(
            [{'id': x.entry_id, 'name': x.name} for x in entries])

    def get_response(self, entries, list_only=False):
        if list_only:
            return self.get_entries_without_content(entries)
        return self.get_entries(entries)


class FindExact(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find(keyword,
                                       find_similar=self.args['similar'])
        return self.get_response(entries, list_only=self.args['list'])


class GetWord(FindExact):
    pass


class FindByPrefix(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_prefix(keyword,
                                                 find_similar=self.args['similar'])[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindBySuffix(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_suffix(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class FindByPartial(DictionaryResource):
    def get(self, keyword):
        entries = self.dictionary.find_by_partial(keyword)[:MAX_RESULTS]
        return self.get_response(entries, list_only=self.args['list'])


class GetEntry(DictionaryResource):
    def get(self, entry_id):
        entries = self.dictionary.get_entry(entry_id)
        return self.get_response(entries)


@app.route('/')
def index():
    return render_template('index.html', dictionaries=dictionaries)


@app.route('/source')
def source():
    return render_template('source.html', dictionaries=dictionaries)


@app.route('/docs')
def docs():
    return render_template('docs.html', dictionaries=dictionaries)


def dictionary_app_gen(dict_id, dictionary):
    def dictionary_app():
        return render_template('dictionary.html', dictionaries=dictionaries,
                               dict_id=dict_id, dictionary=dictionary)

    return dictionary_app


api_baseurl = '/api/v1/dictionaries'
# api.add_resource(GetDictionaries, api_baseurl + '/')


def add_resource(cname, url_template, dict_id, dictionary):
    extra_props = {'dict_id': dict_id, 'dictionary': dictionary}
    subclass = type(dict_id + cname.__name__, (cname,), extra_props)
    api.add_resource(subclass, url_template.format(api_baseurl, dict_id))


def register_dictionary_endpoints():
    for dict_id, dictionary in dictionaries:
        app.add_url_rule('/' + dict_id, dict_id,
                         dictionary_app_gen(dict_id, dictionary))

        add_resource(GetWord,
                     '{0}/{1}/words/<string:keyword>',
                     dict_id, dictionary)

        add_resource(FindExact,
                     '{0}/{1}/find/exact/<string:keyword>',
                     dict_id, dictionary)

        add_resource(FindByPrefix,
                     '{0}/{1}/find/prefix/<string:keyword>',
                     dict_id, dictionary)

        add_resource(FindBySuffix,
                     '{0}/{1}/find/suffix/<string:keyword>',
                     dict_id, dictionary)

        add_resource(FindByPartial,
                     '{0}/{1}/find/partial/<string:keyword>',
                     dict_id, dictionary)

        add_resource(GetEntry,
                     '{0}/{1}/entries/<path:entry_id>',
                     dict_id, dictionary)


if __name__ == '__main__':
    register_dictionary_endpoints()
    app.run()
