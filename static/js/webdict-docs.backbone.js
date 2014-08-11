var App = window.App = {};

App.API_BASEURL = '/api/v1/dictionaries';
App.MAX_RECENT = 25;

App.Form = Backbone.View.extend({
    el: '#find-by-keyword',
    events: {
        'keypress .keyword': 'runOnEnter',
        'click .run': 'runBtn'
    },
    initialize: function(options) {
        this.keyword = this.$('.keyword');
        this.dictionary = this.$('select[name="dictionary"]');
        this.curl = this.$('.api-curl');
        this.output = this.$('.api-output');
    },
    runBtn: function(e) {
        e.preventDefault();
        this.run();
    },
    runOnEnter: function(e) {
        if (e.keyCode != 13) return;
        e.preventDefault();
        this.run();
    },
    run: function() {
        var keyword = this.keyword.val();
        if (!keyword) return;
        this.runWithKeyword(keyword);
    },
    runWithKeyword: function(keyword) {
        var dictionary = this.dictionary.val();
        var method = this.$el.find('.method:checked').val();
        this.find(dictionary, method, keyword);
    },
    find: function(dictionary, method, keyword) {
        var url = App.API_BASEURL + "/" + dictionary + "/find/" + method + "/" + keyword;

        this.curl.text('curl ' + url);

        //this.keyword.val('');
        var _this = this;
        var success = function(json) {
            _this.onApiSuccess(keyword, json);
        };
        var error = function(jqXHR, textStatus, errorThrown) {
            _this.onApiError(url, jqXHR, textStatus, errorThrown);
        };

        $.ajax({
            url: url,
            data: {
                similar: true
            },
            success: success,
            error: error
        });
    },
    onApiSuccess: function(keyword, json) {
        $('.loading').addClass('loading-hidden');
        $('.api-error').addClass('api-error-hidden');

        this.output.empty();
        this.output.text(JSON.stringify(json, null, 2));
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

function onDomReady() {
    App.form = new App.Form();
    App.form.keyword.val('lo');
    App.form.run();
}

$(function() {
    onDomReady();
});
