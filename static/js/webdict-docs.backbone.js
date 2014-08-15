var App = window.App = {};

App.API_BASEURL = '/api/v1/dictionaries';

App.ApiParams = Backbone.Model.extend({
    defaults: {
        dict_id: 'wud',
        method: 'exact',
        keyword: 'soundx',
        similar: true
    }
});

App.FormView = Backbone.View.extend({
    el: '#find-by-keyword',
    events: {
        'keypress .keyword': 'runOnEnter',
        'click .run': 'runBtn',
        'change .dictionary': 'run',
        'change .method': 'run',
        'change .keyword': 'run',
        'change #find-similar': 'run',
        'change #list-only': 'run'
    },
    initialize: function (options) {
        this.keyword = this.$('.keyword');
        this.keyword.val(this.model.get('keyword'));
        this.dictionary = this.$('select[name="dictionary"]');
        this.output = this.$('.api-output');
    },
    runBtn: function (e) {
        e.preventDefault();
        this.run();
    },
    runOnEnter: function (e) {
        if (e.keyCode != 13) return;
        e.preventDefault();
        this.run();
    },
    run: function () {
        var keyword = this.keyword.val();
        if (!keyword) return;
        this.runWithKeyword(keyword);
    },
    runWithKeyword: function (keyword) {
        var dictionary = this.dictionary.val();
        var method = this.$el.find('.method:checked').val();
        var similar = this.$el.find('#find-similar:checked').size() > 0;
        var list = this.$el.find('#list-only:checked').size() > 0;
        this.find(dictionary, method, keyword, similar, list);
    },
    find: function (dict_id, method, keyword, similar, list) {
        this.model.set({
            dict_id: dict_id,
            method: method,
            keyword: keyword,
            similar: similar,
            list: list
        });
        var url = App.API_BASEURL + "/" + dict_id + "/find/" + method + "/" + keyword;
        var extras = {};
        if (similar) {
            extras['similar'] = true;
        }
        if (list) {
            extras['list'] = true;
        }

        var _this = this;
        var success = function (json) {
            _this.onApiSuccess(keyword, json);
        };
        var error = function (jqXHR, textStatus, errorThrown) {
            _this.onApiError(url, jqXHR, textStatus, errorThrown);
        };

        $.ajax({
            url: url,
            data: extras,
            success: success,
            error: error
        });
    },
    onApiSuccess: function (keyword, json) {
        $('.loading').addClass('loading-hidden');
        $('.api-error').addClass('api-error-hidden');

        this.output.empty();
        this.output.text(JSON.stringify(json, null, 2));
    },
    onApiError: function (url, jqXHR, textStatus, statusText) {
        $('.loading').addClass('loading-hidden');
        var $apiError = $('.api-error');
        $apiError.removeClass('api-error-hidden');
        $apiError.find('a').attr('href', url).text(url);
        $apiError.find('.statusNum').text(jqXHR.status);
        $apiError.find('.statusText').text(statusText);
    }
});

function format(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
}

App.CurlView = Backbone.View.extend({
    el: '#api-curl',
    initialize: function () {
        this.model.on('change', this.render, this);
    },
    render: function () {
        var extras = '';
        var similar = this.model.get('similar');
        var list = this.model.get('list');
        if (similar || list) {
            extras += ' --get';
            if (similar) {
                extras += ' -d similar=1';
            }
            if (list) {
                extras += ' -d list=1';
            }
        }

        var curl_url = format('{0}{1}/{2}/find/{3}/{4}',
            location.origin, App.API_BASEURL,
            this.model.get('dict_id'), this.model.get('method'), this.model.get('keyword'));
        if (curl_url.indexOf(' ') > -1) {
            curl_url = '"' + curl_url + '"';
        }

        this.$el.text('curl ' + curl_url + extras);
        return this;
    },
    clear: function () {
        this.model.clear();
    }
});

function onDomReady() {
    var apiParams = new App.ApiParams();
    new App.CurlView({model: apiParams}).render();
    var form = new App.FormView({model: apiParams});
    form.run();
}

$(function () {
    onDomReady();
});
