// the app's namespace
var App = window.App = {};

//conflicts with Flask
//_.templateSettings = { interpolate: /\{\{(.+?)\}\}/g };

App.QUERY_URL = '/api/v1/dictionaries/ahd/find/exact';
App.ENTRY_URL = '/api/v1/dictionaries/ahd/get/entry';
App.MAX_RECENT = 25;

App.Router = Backbone.Router.extend({
    routes: {
        "find/exact/:keyword": "findExact",
        "get/entry/*entry_id": "getEntry"
    },
    findExact: function(keyword) {
        App.form.findExact(keyword);
    },
    getEntry: function(entry_id) {
        App.form.getEntry(entry_id);
    }
});

App.Form = Backbone.View.extend({
    el: '#main-content',
    events: {
        'keypress .search-query': 'searchOnEnter',
        'click .search': 'searchBtn',
        'click .reset': 'resetBtn'
    },
    initialize: function(options) {
        this.recentList = options.recentList;
        this.input = this.$('.search-query');
        this.results = this.$('.results');
    },
    resetBtn: function(e) {
        e.preventDefault();
        this.input.val('');
        this.input.focus();
    },
    searchBtn: function(e) {
        e.preventDefault();
        this.findExact();
    },
    searchOnEnter: function(e) {
        if (e.keyCode != 13) return;
        e.preventDefault();
        this.findExact();
    },
    findExact: function(keyword) {
        if (!keyword) {
            keyword = this.input.val();
        }
        if (!keyword) return;

        App.router.navigate('find/exact/' + keyword);
        var url = App.QUERY_URL + "/" + keyword;

        this.input.val('');
        var _this = this;
        var success = function(json) {
            _this.onApiSuccess(keyword, json);
        };
        var error = function(jqXHR, textStatus, errorThrown) {
            _this.onApiError(url, jqXHR, textStatus, errorThrown);
        };

        $('.loading').removeClass('loading-hidden');
        $.ajax({
            url: url,
            success: success,
            error: error
        });
    },
    getEntry: function(entry_id) {
        App.router.navigate('get/entry/' + entry_id);
        var url = App.ENTRY_URL + "/" + entry_id;

        this.input.focus();
        var _this = this;
        var success = function(json) {
            _this.onApiSuccess(null, json);
        };
        var error = function(jqXHR, textStatus, errorThrown) {
            _this.onApiError(url, jqXHR, textStatus, errorThrown);
        };

        $('.loading').removeClass('loading-hidden');
        $.ajax({
            url: url,
            success: success,
            error: error
        });
    },
    onApiSuccess: function(keyword, json) {
        $('.loading').addClass('loading-hidden');
        $('.api-error').addClass('api-error-hidden');

        var $results = this.results;
        var recentList = this.recentList;
        var entries = json.matches[0].entries;
        if (!entries.length) {
            $('.no-matches').removeClass('no-matches-hidden');
            return;
        }
        $('.no-matches').addClass('no-matches-hidden');

        function render_subscripts(str) {
            return str.replace(/-(\d+)/, '<sub>$1</sub>');
        }

        var noExactMatches = keyword && keyword != entries[0].name.substr(0, keyword.length);

        if (entries.length) {
            $results.empty();
            _.each(entries, function(entry) {
                var name = render_subscripts(entry.name);
                if (!noExactMatches) {
                    recentList.addCustom({
                        name: name,
                        entry_id: entry.id
                    });
                }
                $results.append($('<h3/>').append(name));
                var refs = [];
                var refs_links = {};
                if (entry.content[entry.content.length - 1][0] == 'REFERENCES') {
                    refs = entry.content.pop()[1];
                    _.each(refs, function(ref) {
                        var parts = ref.split(':');
                        var ref_name = render_subscripts(parts[2]);
                        refs_links[ref] = $('<a/>').append(ref_name).attr('href', '#get/entry/' + parts[1]).prop('outerHTML');
                    });
                }
                var dl = $('<dl/>');
                _.each(entry.content, function(item) {
                    var dt = item[0];
                    var dd = item[1];
                    dd = dd.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    dd = dd.replace(/\*(.*?)\*/g, '<em>$1</em>');
                    dd = render_subscripts(dd);
                    _.each(refs, function(ref, i) {
                        var pattern = "\\[.*?\\]\\[" + (parseInt(i) + 1) + "\\]";
                        dd = dd.replace(new RegExp(pattern, "g"), refs_links[ref]);
                    });
                    dl.append($('<dt/>').append(dt));
                    dl.append($('<dd/>').append(dd));
                });
                $results.append(dl);
            });
        }

        if (noExactMatches) {
            var items = [];
            _.each(entries, function(entry) {
                items.push(new App.Entry({
                    entry_id: entry.id,
                    name: render_subscripts(entry.name)
                }));
            });
            App.similarList.reset(items);
        }
    },
    onApiError: function(url, jqXHR, textStatus, statusText) {
        $('.loading').addClass('loading-hidden');
        var $apiError = $('.api-error');
        $apiError.removeClass('api-error-hidden');
        $apiError.find('a').attr('href', url).text(url);
        $apiError.find('.statusNum').text(jqXHR.status);
        $apiError.find('.statusText').text(statusText);
    }
});

App.Entry = Backbone.Model.extend({
    defaults: {
        entry_id: null,
        name: null
    }
});

App.RecentList = Backbone.Collection.extend({
    model: App.Entry,
    localStorage: new Store('webdict-backbone'),
    addCustom: function(obj) {
        var filter = function(item) {
            return item.get('entry_id') == obj.entry_id;
        };
        var remove = function(item) {
            item.destroy();
        };
        _.each(this.filter(filter), remove);

        this.create(obj);

        var excessItemsNum = this.length - App.MAX_RECENT;
        if (excessItemsNum > 0) {
            _.each(this.toArray().slice(0, excessItemsNum), remove);
        }

        this.trigger('updated');
    }
});

App.SimilarList = Backbone.Collection.extend({
    model: App.Entry
});

App.EntryView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#entry-template').html()),
    initialize: function() {
        this.model.bind('destroy', this.remove, this);
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    clear: function() {
        this.model.clear();
    }
});

App.RecentListView = Backbone.View.extend({
    el: '#recent',
    initialize: function(options) {
        this.list = options.list;
        this.list.bind('reset', this.render, this);
        this.list.bind('updated', this.render, this);
        this.list.fetch();
    },
    render: function() {
        this.$('.recent-list').empty();
        this.list.each(this.add);
        if (this.list.length) {
            this.$el.removeClass('hidden');
        }
    },
    add: function(entry) {
        var view = new App.EntryView({model: entry});
        this.$('.recent-list').prepend(view.render().el);
    }
});

App.SimilarListView = Backbone.View.extend({
    el: '#similar',
    initialize: function(options) {
        this.list = options.list;
        this.list.bind('reset', this.render, this);
    },
    render: function() {
        this.$('.similar-list').empty();
        this.list.each(this.add);
        if (this.list.length) {
            this.$el.removeClass('hidden');
        }
    },
    add: function(entry) {
        var view = new App.EntryView({model: entry});
        this.$('.similar-list').append(view.render().el);
    }
});

function onDomReady() {
    App.recentList = new App.RecentList();
    App.recentListView = new App.RecentListView({
        list: App.recentList
    });

    App.similarList = new App.SimilarList();
    App.similarListView = new App.SimilarListView({
        list: App.similarList
    });

    App.form = new App.Form({
        recentList: App.recentList
    });
    App.form.input.focus();

    App.router = new App.Router();

    Backbone.history.start();

    if (!window.location.hash) {
        App.form.findExact('hello');
    }
}

$(function() {
    onDomReady();
});