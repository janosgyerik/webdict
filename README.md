Simple Web Dictionary
=====================

A simple web interface for dictionaries.

Features
--------

- Remember recent searches // local storage
- Find similar words when no exact matches
- Restful API
- Easy to extend, one dictionary = one plugin

Requirements
------------

- Python packages: pip, virtualenv, Flask
- Backbone
- Bootstrap

Installing
----------

Create virtualenv:

    virtualenv --distribute virtualenv

Install requirements inside virtualenv:

    ./pip.sh install -r requirements.txt

Download dictionary data, for example:

    curl TODO_URL_TO_WEBSTER_DATA_FILE
    tar zxf TODO_PATH_TO_WEBSTER_DATA_FILE
    mv TODO_WEBSTER_DATA_PATH /path/to/where/you/want

Create plugin settings file and set `dictionary_path`:

    cp plugins/wud/settings.py.sample plugins/wud/settings.py

Run the site locally:

    ./run.sh

Links
-----

- https://github.com/janosgyerik/webdict
- http://webdict.janosgyerik.com/

