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
- Backbone.js
- Bootstrap

Installing
----------

Create virtualenv:

    virtualenv --distribute virtualenv

Install requirements inside virtualenv:

    ./pip.sh install -r requirements.txt

Configure plugins. Every dictionary is a plugin.
Plugins are in the `./plugins` directory.
See the README file in each plugins directory for installation steps,
for example `./plugins/wud/README.md` for Webster's Unabridged Dictionary.

Run the site locally:

    ./run.sh

Creating a new dictionary plugin
--------------------------------

TODO

Links
-----

- https://github.com/janosgyerik/webdict
- http://webdict.janosgyerik.com/
