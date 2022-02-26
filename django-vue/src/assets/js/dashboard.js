axios.defaults.xsrfHeaderName = "X-CSRFToken";

Vue.component('modal', {
    template: '#modal-template',
    props: {
        imgsource: '',
    }
});

var app = new Vue({
    el: '#app',
    data: {
        showPopup: false,
        imgSrc: '',
        chart: {
            scores: [],
            low: 0,
            high: 0,
        },
        rank: 0,
    },
    computed: {
        getRankName: function() {
            switch (this.rank) {
                case 1:
                    return 'Gangsa';
                case 2:
                    return 'Perak';
                case 3:
                    return 'Emas';
                default:
                    return 'Tiada Peringkat';
            }
        },
        getRankBadge: function() {
            var badge;
            switch (this.rank) {
                case 1:
                    badge = 'bronze';
                    break;
                case 2:
                    badge = 'silver';
                    break;
                case 3:
                    badge = 'gold';
                    break;
                default:
                    badge = 'unranked';
                    break;
            }

            return '/static/img/' + badge + '.png';
        }
    },
    mounted: function () {
        var self = this;
        self.inProgress = true;

        axios.get('/report')
            .then(function (response) {
                var resp = response.data;
                if (resp.status == 0) {
                    self.chart.low = resp.data.low;
                    self.chart.high = resp.data.high;
                    self.chart.scores = resp.data.scores;
                    self.rank = resp.data.rank;

                    new Chartist.Line(self.$refs.chartStudentRank, {
                        series: [self.chart.scores,]
                    },
                    {
                        lineSmooth: false,
                        fullWidth: true,
                        chartPadding: { right: 40 },
                        axisX: { showGrid: false, showLabel: false },
                        axisY: { showLabel: true },
                        high: self.chart.high,
                        low: self.chart.low,
                    });
                }

                self.inProgress = false;
            })
            .catch(function (error) {
                self.inProgress = false;
            });
    },
    methods: {
        openImage: function(url) {
            this.imgSrc = url;
            this.showPopup = true;
        }
    }
})