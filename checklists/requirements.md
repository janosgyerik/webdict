Specific functional requirements
--------------------------------

### Inputs

- What?
    + word, expression, phrase to find
        - may contain spaces and special characters
    - search options
        - prefix, suffix, partial search
        - find similar // by shortening prefix
        - find matches but don't load details // index search only, no content
        - get cross reference
            + web interface
            - cli
    + entry id, for bookmarks, cross references
    - auto-suggest
        - load entire index on web interface
    - dictionaries to use
- From where?
    + input field in browser form
    + command line arg
    - restful call
- Accuracy?
    + nice to have: option to tolerate failures, typos // find_similar = True
+ Range of values?
    - dictionary backend should implement input validation
    - any range can be valid
+ Frequency?
    - not a concern, arbitrary

### Outputs

- What?
    - need html and structured text
    + need cross references to related entries, similar entries
    - markdown can be suitable
    + json for restful calls
    - dictionary should specify the format it provides: md, html
    - dictionary should specify available formats
    - dictionary should handle accepted formats
    - entries may be complex
        - japanese entries need: kanji, furigana, romaji
        - entry may be structured object
- Destination?
    + web page -- html
    + terminal -- md
    - mobile device -- responsive html
+ Accuracy?
    - not a concern
- Range of values?
    - cap on output size by default
    - dictionary may support changing the cap
    - single entry length depends on the dictionary content
+ Frequency?
    - not a concern
+ Format? -> web pages?
    - web page, html
    - terminal, markdown
- Format? -> reports?
    - usage statistics might be nice, but not required
- Format? -> other?

### External interfaces

+ External hardware to interface with?
- External software to interface with?
    - allow custom dictionary plugins
        - need good documentation with examples
        - use git submodules, need examples

### External communication interfaces

- What are they?
    - restful api
    + browser
- Error checking?
    + no matches = empty list
    - no such entry = empty list
    - invalid api calls // 404 page
- Protocols?
    + json response, describing
        - list of matching entries
    + entry is a definition list = label + content pairs
    - entry may need to be complex object
        - japanese: kanji field, furigana field, romaji field
        - pronunciation field
        - definition list label can be used as css class

### Tasks

- What are the tasks the user wants to perform?
    + find word in dictionary
    - find by prefix, suffix or partial
        + cli
        + restful api
        - web interface
    - list only
        + cli
        - restful api
        - web interface
    - find similar
        + cli
        - restful api
        - web interface
    - find in multiple sources
    - remember recent searches
        - web interface
+ What are the data used by each task?
    - json input, json output, rendered as markdown or html
+ What are the data resulting from each task?


Non-functional quality requirements
-----------------------------------

### Time constraints

+ What is the expected response time of all necessary operations?
    - reasonably fast
- Any considerations about processing time?
    - index should be preloaded from native format (compiled), ideally zipped
- Any considerations about data transfer rate?
    + normal usage should be lightweight
    - avoid loading entries when listing is enough
+ Any considerations about system throughput?
    - nothing special

### Security, stability, safety

+ Any security considerations? Any concerns?
    - intellectual property concerns of dictionary content
+ Is the reliability specified?
    - no special concerns
+ Consequences of failure?
    - no special consequences
- Any vital information that needs to be protected?
    - don't add proprietary dictionary data to version control
        - organize the project to make such mistake difficult (ignore patterns) 
- Anything vital that needs to be protected from failure?
    - user preferences and bookmarks
- Strategy for error detection?
    - test driven development recommended

### System requirements

- Maximum memory?
    + expected lightweight: example dictionary non-optimized index size 2.4 MB
    - optimize index
- Maximum storage?
    + medium: example dictionary non-optimized content size 376 MB
    - optimize storage format (zip?)

### Maintainability

- Any maintainability considerations?
    - adding new dictionaries should be easy
- Any anticipated changes?
    - Multiple query strings?
        - for example: Japanese dictionary with separate kanji/furigana/romaji fields?
        - let the plugin implement distinguishing different types of input
    - Dictionary specific UI?
        - for example:
            - multiple input fields and corresponding new API endpoints
            - multiple input fields collapsed to existing API endpoints
              but with special markup for specialized dictionary
            - dictionary provider might want to enable sexy features
              of his new dictionary not supported by simplistic default UI
                - example: support for sound files of pronunciation
        - dictionary specific behavior is possible:
            - use appropriate dt.CLASS fields
            - extend the UI to post-process matches, with appropriate handling
              for dt.CLASS
    - Extending the API
        - no big changes expected in the search API
        - extending dictionary properties should be possible
    - Extending the UI
        - should be possible to modularize the JavaScript client
          and add dictionary specific behavior
    - Extending the command line interface
        - no significant changes expected
    - Non-text input, for example image search
        - too different concept, won't support
    - Non-markdown output
        - for dictionaries that are hard to normalize but produce reasonably good
          html output, the markdown output requirement might be harsh.
          -> allow raw output
- Definition of success?
    - easy to use web interface
    - easy to use api
    - great api documentation with live examples
- Definition of failure?
    - failure of items listed under success

