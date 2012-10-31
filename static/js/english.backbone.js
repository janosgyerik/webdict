/*!
 * english backbone JavaScript Library v0.1
 * http://.../
 *
 * Copyright 2012, Janos Gyerik
 * http://.../license
 *
 * Date: Fri Oct  5 18:56:59 CEST 2012
 */


// the basic namespace
// TODO: put in app.js
window.App = {};

//conflicts with Flask
//_.templateSettings = { interpolate: /\{\{(.+?)\}\}/g };

// classes
// TODO: put in app/*.js


// app constants
App.QUERY_URL = '/query';
App.MAX_RECENT = 15;

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
        this.search();
    },
    search: function(keyword) {
        if (!keyword) {
            keyword = this.input.val();
        }
        if (!keyword) return;
        this.input.val('');
        var _this = this;
        var success = function(json) {
            _this.onLookupSuccess(json);
        };
        var error = function(jqXHR, textStatus, errorThrown) {
            _this.onLookupError(jqXHR, textStatus, errorThrown);
        };
        $.ajax({
            url: App.QUERY_URL,
            dataType: 'json',
            data: {
                keyword: keyword
            },
            success: success,
            error: error
        });
    },
    searchOnEnter: function(e) {
        if (e.keyCode != 13) return;
        e.preventDefault();
        this.search();
    },
    getfile: function(filename) {
        this.input.focus();
        var _this = this;
        var success = function(json) {
            _this.onLookupSuccess(json);
        };
        var error = function(jqXHR, textStatus, errorThrown) {
            _this.onLookupError(jqXHR, textStatus, errorThrown);
        };
        $.ajax({
            url: App.QUERY_URL,
            dataType: 'json',
            data: {
                file: filename
            },
            success: success,
            error: error
        });
    },
    onLookupSuccess: function(json, quiet) {
        var _this = this;
        var results = this.results;
        results.empty();
        var recentList = this.recentList;
        _.each(json, function(bundle) {
            if (!quiet) {
                recentList.addCustom({word: bundle.word, filename: bundle.filename});
            }
            results.append($('<h3/>').append(bundle.word));
            var dl = $('<dl/>');
            _.each(bundle.dl, function(item) {
                var tag = item[0];
                var value = item[1];
                dl.append($('<' + tag + '/>').append(value));
            });
            results.append(dl);
        });
        results.find('a').each(function(i, item) {
            var href = $(this).attr('href');
            var key = 'file=';
            var filename = href.substr(href.indexOf(key) + key.length);
            $(this).click(function(e) {
                e.preventDefault();
                _this.getfile(filename);
            });
        });
    }
});

App.Word = Backbone.Model.extend({
    defaults: {
        word: null,
        file: null
    }
});

App.RecentList = Backbone.Collection.extend({
    model: App.Word,
    localStorage: new Store('english-backbone'),
    addCustom: function(obj) {
        var filter = function(item) {
            return item.get('filename') == obj.filename;
        };
        var remove = function(item) {
            item.destroy();
        };
        _.each(this.filter(filter), remove);
        this.create(obj);
        var itemsToSlice = this.length - App.MAX_RECENT;
        if (itemsToSlice > 0) {
            _.each(this.toArray().slice(itemsToSlice), remove);
        }
        this.trigger('updated');
    }
});

App.WordView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#word-template').html()),
    events: {
        'click a.destroy': 'clear'
    },
    initialize: function() {
        this.model.bind('destroy', this.remove, this);
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        var filename = this.model.get('filename');
        this.$el.find('a').click(function(e) {
            e.preventDefault();
            App.form.getfile(filename);
        });
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
        this.$('.list').empty();
        this.list.each(this.add);
        if (this.list.length) {
            this.$el.removeClass('hidden');
        }
        else {
            this.$el.addClass('hidden');
        }
    },
    add: function(word) {
        var view = new App.WordView({model: word});
        this.$('.list').prepend(view.render().el);
    }
});

function onDomReady() {
    // instances
    // TODO: put in setup.js
    // 
    App.recentList = new App.RecentList();
    App.recentListView = new App.RecentListView({
        list: App.recentList
    });

    App.form = new App.Form({
        recentList: App.recentList
    });
    App.form.onLookupSuccess(window.hello, true);
    App.form.input.focus();

    // debugging
    //App.form.search('indignation');
}

$(function() {
    onDomReady();
});

// eof
