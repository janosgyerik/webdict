- create interactive api doc

- upload the wud data files *somewhere*

- make wud (webster) more attractive
    - add subscript to multiple matches
        - add index in file, NOT in index
        - example words: anger
    - make keywords like `Defn:`, `Syn.` bold
    - make `\([A-Z][a-z]+\.\)` bold
    - make `\[[A-Z][a-z]+\.\]` bold
    - decorate poet names:
        - ` Shak.` -> `*--Shak.*`
        - Milton. Chapman. Addison. Dryden.
        - Young. Rowe. Pope.
    - add cross references:
        - "See Flame" (in inflame)
        - `Syn. -- To provoke; fire; kindle; irritate; exasperate; incense; enrage; anger; excite; arouse.`

-----------------------------

create restful cli

upgrade components
    - jquery
    - bootstrap
    - backbone
    - flask

add missing ui elements
    - radio buttons
        - find exact match
        - find by prefix
        - find by suffix
        - find by partial
    - find similar -- checkbox

polish cli
    --ref NUM option to jump to reference

add more dictionaries
    - find creative commons data
        - http://dumps.wikimedia.org/enwiktionary/20140728/
        - http://www.androidtech.com/downloads/wordnet20-from-prolog-all-3.zip
        - http://www.gutenberg.org/ebooks/29765

-----------------------------

Useful links:

- http://flask.pocoo.org/docs/api/
- http://flask-restful.readthedocs.org/en/latest/quickstart.html
- http://flask-restful.readthedocs.org/en/latest/api.html
- http://backbonejs.org/
- http://git-scm.com/book/en/Git-Tools-Submodules
