var App = window.App = {};

App.API_BASEURL = '/api/v1/dictionaries';

App.FindByKeywordParams = Backbone.Model.extend({
    defaults: {
        dict_id: 'wud',
        method: 'exact',
        keyword: 'explorez',
        similar: true
    }
});

App.FindByKeywordFormView = Backbone.View.extend({
    el: '#find-by-keyword-form',
    events: {
        'keypress .keyword': 'runOnEnter',
        'click .run': 'runBtn',
        'change .dictionary': 'run',
        'change .method': 'run',
        'change .keyword': 'run',
        'change .find-similar': 'run',
        'change .list-only': 'run'
    },
    initialize: function () {
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
        var similar = this.$el.find('.find-similar:checked').size() > 0;
        var list = this.$el.find('.list-only:checked').size() > 0;
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
            extras.similar = true;
        }
        if (list) {
            extras.list = true;
        }

        var _this = this;
        var success = function (json) {
            _this.onApiSuccess(json);
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
    onApiSuccess: function (json) {
        this.$el.find('.api-error').addClass('api-error-hidden');

        this.output.empty();
        this.output.text(JSON.stringify(json, null, 2));
    },
    onApiError: function (url, jqXHR, textStatus, statusText) {
        var $apiError = this.$el.find('.api-error');
        $apiError.removeClass('api-error-hidden');
        $apiError.find('a').attr('href', url).text(url);
        $apiError.find('.statusNum').text(jqXHR.status);
        $apiError.find('.statusText').text(statusText);
    }
});

App.FindByKeywordCurlView = Backbone.View.extend({
    el: '#find-by-keyword-curl',
    initialize: function () {
        this.model.on('change', this.render, this);
        this.model.trigger('change');
    },
    events: {
        'click': 'selectEntireCurl'
    },
    selectEntireCurl: function () {
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(this.el);
        selection.removeAllRanges();
        selection.addRange(range);
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

        var curl_url = String.format('{0}{1}/{2}/find/{3}/{4}',
            location.origin, App.API_BASEURL,
            this.model.get('dict_id'), this.model.get('method'), this.model.get('keyword'));
        if (curl_url.indexOf(' ') > -1) {
            curl_url = '"' + curl_url + '"';
        }

        this.$el.text('curl ' + curl_url + extras);
        return this;
    }
});

App.GetEntryParams = Backbone.Model.extend({
    defaults: {
        dict_id: 'wud',
        entry_id: 's/su/sus/sustainable-102522.txt'
    }
});

App.GetEntryFormView = Backbone.View.extend({
    el: '#get-entry-form',
    events: {
        'keypress .entry-id': 'runOnEnter',
        'click .run': 'runBtn',
        'change .dictionary': 'run',
        'change .entry-id': 'run'
    },
    initialize: function () {
        this.entry_id = this.$('.entry-id');
        this.entry_id.val(this.model.get('entry_id'));
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
        var entry_id = this.entry_id.val();
        if (!entry_id) return;
        this.runWithEntryId(entry_id);
    },
    runWithEntryId: function (entry_id) {
        var dict_id = this.dictionary.val();
        this.get_entry(dict_id, entry_id);
    },
    get_entry: function (dict_id, entry_id) {
        this.model.set({
            dict_id: dict_id,
            entry_id: entry_id
        });
        var url = App.API_BASEURL + "/" + dict_id + "/entries/" + entry_id;

        var _this = this;
        var success = function (json) {
            _this.onApiSuccess(json);
        };
        var error = function (jqXHR, textStatus, errorThrown) {
            _this.onApiError(url, jqXHR, textStatus, errorThrown);
        };

        $.ajax({
            url: url,
            success: success,
            error: error
        });
    },
    onApiSuccess: function (json) {
        this.$el.find('.api-error').addClass('api-error-hidden');

        this.output.empty();
        this.output.text(JSON.stringify(json, null, 2));
    },
    onApiError: function (url, jqXHR, textStatus, statusText) {
        var $apiError = this.$el.find('.api-error');
        $apiError.removeClass('api-error-hidden');
        $apiError.find('a').attr('href', url).text(url);
        $apiError.find('.statusNum').text(jqXHR.status);
        $apiError.find('.statusText').text(statusText);
    }
});

App.GetEntryCurlView = Backbone.View.extend({
    el: '#get-entry-curl',
    initialize: function () {
        this.model.on('change', this.render, this);
        this.model.trigger('change');
    },
    events: {
        'click': 'selectEntireCurl'
    },
    selectEntireCurl: function () {
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(this.el);
        selection.removeAllRanges();
        selection.addRange(range);
    },
    render: function () {
        var curl_url = String.format('{0}{1}/{2}/entries/{3}',
            location.origin, App.API_BASEURL,
            this.model.get('dict_id'), this.model.get('entry_id'));
        if (curl_url.indexOf(' ') > -1) {
            curl_url = '"' + curl_url + '"';
        }

        this.$el.text('curl ' + curl_url);
        return this;
    }
});

if (!String.format) {
    String.format = function (format) {
        var args = Array.prototype.slice.call(arguments, 1);
        return format.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
}

function onDomReady() {
    var findByKeywordParams = new App.FindByKeywordParams();
    new App.FindByKeywordCurlView({model: findByKeywordParams});
    var findByKeywordForm = new App.FindByKeywordFormView({model: findByKeywordParams});
    findByKeywordForm.run();
    findByKeywordForm.keyword.focus();

    var getEntryParams = new App.GetEntryParams();
    new App.GetEntryCurlView({model: getEntryParams});
    var getEntryForm = new App.GetEntryFormView({model: getEntryParams});
    getEntryForm.run();
}

$(function () {
    onDomReady();
});
