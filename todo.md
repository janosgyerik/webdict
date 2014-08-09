multi-dictionary support
    public (wiktionary) or private (american heritage)
    change individual dictionary pages
        add dictionary name somewhere near the top
    perhaps marshal_with can simplify jsonify?
    move ahd to git submodule
        eliminate all references to ahd, american heritage from main source

create a free dictionary
    find creative commons data
        http://dumps.wikimedia.org/enwiktionary/20140728/
        http://www.androidtech.com/downloads/wordnet20-from-prolog-all-3.zip
        http://www.gutenberg.org/ebooks/29765

install on server
    new subdomain: webdict.janosgyerik.com

polish ui
    jazz up the dictionary list with some fancy bootstrap stuff, like jumbotron or something
    use hover rows in recent and similar lists
    add a button to clear similar list

create interactive api doc

-----------------------------

create restful cli

upgrade components
    jquery
    bootstrap
    backbone
    flask

add missing ui elements
    radio buttons
        find exact match
        find by prefix
        find by suffix
        find by fragment
    find similar -- checkbox

polish cli
    --ref NUM option to jump to reference
