Overview
--------
+ dictionary library -- core functionality
- restful api
    - server
    - client
- user interface
    - web interface
    - native command line interface
    - restful command line interface
- interactive api documentation


Dictionary library
------------------
+ implementation of core functionality
+ unit tests
- plugin support
    + interface to implement
    + default indexing logic, plugin may override
    + plugin testing framework
    - run all tests
    - documentation
        - how to implement a new plugin
        - how to test new plugin
        - how to run all tests
    - handle gracefully if plugin cannot be loaded (missing data files)
+ methods
    - find
    - find_by_prefix
    - find_by_suffix
    - find_by_partial
+ mandatory params
    - query string
- optional params
    + find similar
        - only if no match
        - only apply to exact search or prefix search
    - max results to return
    + list only, don't load content
- python modules
    + dictionary.py
        Dictionary
        Entry
            - entry id
            - entry name
            - content
    + test_dictionary.py
        DictionaryTest
    + plugins/id/id.py
        PxDictionary(Dictionary)
        PxEntry(Entry)
    + plugins/id/test_id.py
        PxTest(DictionaryTest)
            - run specialized tests with real examples for given dictionary
    - use git submodule
- Discover plugins
    - standalone mode
        - load a specified plugin
    - multi-user mode
        - load all available plugins
    - loading a plugin
        - import python module
        - load index
    - no need for global settings, only per-plugin settings 


RESTful API server
------------------
+ http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api

+ client of dictionary library
    - native calls to dictionary library
    - output as json
- methods
    - /api/<version>/dictionaries/
        - id
        - name
        - description
    + /api/<version>/dictionaries/<dict>/find/exact/<query>
    + ? similar=1
    + ? list=1
    - ? max=10
    - ? format=raw
    + /api/<version>/dictionaries/<dict>/find/prefix/<query>
    + /api/<version>/dictionaries/<dict>/find/suffix/<query>
    + /api/<version>/dictionaries/<dict>/find/partial/<query>
    + /api/<version>/dictionaries/<dict>/entries/<query>
- example param values
    + version: v1
    + dict: wud (Webster's Unabridged Dictionary)
    - max: 10
- possible changes
    - search multiple dictionaries: comma separated ids
        - don't allow commas in ids
    - implement different api
+ no such method: standard http 404
+ success response example
    {
        'matches': [{
            'dict': 'wud',
            'format': 'dl-md',  // definition list + markdown
            'entries': [
                {
                    'id': '60/H0136000.html',
                    'name': 'hello',
                    'content': [
                        ['syllabication', 'hel-lo'],
                        ['noun', 'A calling or greeting of "hello"']
                    ],
                    'references': []
                }
            ]
        }]
    }
- errors should have JSON representation, example:
    {
      "code" : 1234,
      "message" : "Something bad happened :(",
      "description" : "More details about the error here"
    }
- need pagination?
    - use the link header values: next, prev, first, last
    - https://developer.github.com/v3/#pagination

+ list_only responses have no 'content' field


RESTful API client
------------------
- inherits from Dictionary
- overrides interface methods to delegate to RESTful API server


Web interface
-------------
+ Responsive grid: bootstrap
+ Web 2.0: ajax via jquery
- Single-page app: backbone with router
    + hashtag routes to cross references
    - list of recent searches
        - hashtag routes to recent entries
    + bookmarkable search results
- Options
    - checkboxes for dictionaries to use
        - hide if only one dictionary
    - search type radio buttons
        - exact match
        - find by prefix, suffix, partial
    - find similar
    - no need to expose more
- Sensible default options
    - default max results = 10
    - default history size = 25
    - list-only = false
- Store user selections and user data in local storage or cookies
    - selected dictionaries
    - recent searches
    - last query


Native command line interface
-----------------------------
- import dictionary modules
+ run in standalone mode
+ output results formatted as markdown


Restful command line interface
------------------------------
- import restful api client
- run in standalone mode
- output results formatted as markdown


Interactive api documentation
-----------------------------
- Similar to web interface
    - no recent searches
- Query examples
    - editable URL field
    - live results below
    - example code below
