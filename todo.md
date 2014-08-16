- make wud (webster) more attractive
    - decorate poet names:
        - ` Shak.` -> `*--Shak.*`
        - Milton. Chapman. Addison. Dryden.
        - Young. Rowe. Pope.
    - add cross references:
        - "See Flame" (in inflame)
        - `Syn. -- To provoke; fire; kindle; irritate; exasperate; incense; enrage; anger; excite; arouse.`

-----------------------------

- create restful cli

- upgrade components
    - jquery
    - bootstrap
    - backbone
    - flask

- add unimplemented ui elements
    - radio buttons
        - find exact match
        - find by prefix
        - find by suffix
        - find by partial
    - find similar -- checkbox

- polish cli
    --ref NUM option to jump to reference

- api improvements
    - maybe: change 'references' values to api urls
        - clients should not have to know how to interpret the values
        - clients should not have to know how to format urls of subsequent requests
            - the router logic can be simplified
                - match the end part to get the hashtag path
                - use the original url in the actual request
    - maybe: change id to url
        - the url *is* an id: unique identifier of the resource
        - on the other hand, id is stable across versions, url is not
        - perhaps the api could suggest a route
        - the client could keep track of the mapping between route and url
        - when the url is not cached, only then the client could format the url,
            simply by sticking at the end of the api base url

- add more dictionaries
    - find creative commons data
        - http://dumps.wikimedia.org/enwiktionary/20140728/
        - http://www.androidtech.com/downloads/wordnet20-from-prolog-all-3.zip
        - http://www.gutenberg.org/ebooks/29765

- improve interactive api doc
    - use backbone router
    - tabbed output
        - default tab: output
        - python cli code, derive from model like curl view does

- make common HTML reusable somehow, especially the navbar content

-----------------------------

Useful links:

- http://flask.pocoo.org/docs/api/
- http://flask-restful.readthedocs.org/en/latest/quickstart.html
- http://flask-restful.readthedocs.org/en/latest/api.html
- http://backbonejs.org/
- http://git-scm.com/book/en/Git-Tools-Submodules
- http://getbootstrap.com/2.3.2/
