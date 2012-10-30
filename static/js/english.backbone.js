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

_.templateSettings = { interpolate: /\{\{(.+?)\}\}/g };

// classes
// TODO: put in app/*.js


App.queryURL = '/query';

App.Form = Backbone.View.extend({
    el: '#main-content',
    events: {
        'keypress .search-query': 'searchOnEnter',
        'click .search': 'searchBtn',
        'click .reset': 'resetBtn'
    },
    initialize: function() {
        this.input = this.$('.search-query');
        this.results = this.$('.results');
    },
    resetBtn: function(e) {
        e.preventDefault();
        this.input.val('');
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
            url: App.queryURL,
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
    onLookupSuccess: function(json) {
        var results = this.results;
        results.empty();
        _.each(json, function(bundle) {
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
            console.log($(this).attr('href'));
            $(this).click(function(e) {
                e.preventDefault();
                console.log('hello');
            });
        });
    }
});


function onDomReady() {
    // instances
    // TODO: put in setup.js
    // 
    App.form = new App.Form();
    App.form.search('hello');
    App.form.input.focus();

    // debugging
    //App.form.input.val('indignation');
    //App.form.search();
}

$(function() {
    onDomReady();
});

// eof
