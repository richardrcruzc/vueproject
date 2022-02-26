
var getParameterByName = function (name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

var app = new Vue({
    el: '#app',
    data: {
        published: true,
        review: true,
        draft: true,
        level: new Array(10).fill(true),
    },
    computed: {},
    mounted: function () {
        var url = window.location.href;
        var startIndex = url.indexOf("?");

        if (startIndex == -1) return;

        var req_level = new Array(10).fill(false);
        var req_published = new Array(3).fill(false);

        var param_str = url.substring(startIndex+1);
        params = param_str.split("&");
        for (var i=0; i < params.length; i++) {
            param_parts = params[i].split('=');
            if (param_parts.length == 2) {
                param_parts[0] = param_parts[0].toLowerCase();
                if (param_parts[0] === 'level') {
                    var level = parseInt(param_parts[1]);
                    if ((1 <= level) && (level <= 10)) {
                        req_level[level-1] = true;
                    }
                }
                else if (param_parts[0] == 'published') {
                    req_published[0] = true;
                }
                else if (param_parts[0] == 'review') {
                    req_published[1] = true;
                }
                else if (param_parts[0] == 'draft') {
                    req_published[2] = true;
                }
            }
        }

        for (var i=0; i < this.level.length; i++) {
            this.level.splice(i, 1, req_level[i]);
        }

        this.published = req_published[0];
        this.review = req_published[1];
        this.draft = req_published[2];
    },
    methods: {
        filter: function() {
            total_level = 0;
            filter = '';

            if (this.published) filter += '&published=1';
            if (this.review) filter += '&review=1';
            if (this.draft) filter += '&draft=1';

            for (var i=0; i < 10; i++) {
                if (this.level[i] === true) {
                    total_level++;
                    filter += '&level=' + (i+1);
                }
            }

            if ((this.published) && (this.review) && (this.draft) && total_level == 10) {
                window.location.href = '/reading';
            }
            else {
                window.location.href = '/reading?' + filter.substring(1, filter.length);
            }

        }
    }
})