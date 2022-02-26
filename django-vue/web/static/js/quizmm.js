axios.defaults.xsrfHeaderName = "X-CSRFToken";

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
    inProgress: false,
    audioUrl: null,
    imageUrl: null,
    readingId: null,
    trial: 0,
    currentQId: 0,
    currentAnswer: -1,
    readingData: {
        reading: '',
        questions: []
    }
  },
  computed: {
    currentQuestionNumber() {
        return this.currentQId + 1;
    },
    currentQuestion() {
        if (this.currentQId < this.readingData.questions.length) {
            return this.readingData.questions[this.currentQId].question;
        }
    },
    currentChoices() {
        if (this.currentQId < this.readingData.questions.length) {
            return this.readingData.questions[this.currentQId].choices;
        }
    }
  },
  mounted: function () {
    this.getQuizMaterial();

    this.$watch('audioUrl', () => {
        this.$refs.player.load()
    })

  },
  methods: {
    getNextQuestion: function() {
        this.currentAnswer = -1;
        this.currentQId++;
        this.trial = 0;
        var self = this;
        if (this.currentQId >= this.readingData.questions.length) {
            swal({
                title: `Selesai!`,
                text: 'Pertanyaan untuk bacaan ini telah selesai!',
                buttonsStyling: false,
                showCancelButton: true,
                confirmButtonText: 'Ke bacaan berikut',
                cancelButtonText: 'Berhenti',
                confirmButtonClass: 'btn btn-success btn-fill',
                cancelButtonClass: 'btn btn-success btn-fill',
                type: 'success'
            })
            .then(function () {
                    console.log('next question');
                    self.reset();
                    self.getQuizMaterial();
                 },
                function (dismiss) {
                  if (dismiss === 'cancel') {
                    // Back to dashboard
                    window.location.replace("/dashboard");
                  }
                });
        }
    },
    getQuizMaterial: function() {
        var formData = new FormData();

        formData.append('data', JSON.stringify(this.readingData));
        formData.append('params', JSON.stringify({'type': 'save'}));

        var self = this;
        self.inProgress = true;
        axios.post('/quiz/mm', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }})
            .then(function (response) {
                var resp = response.data;
                if (resp.status == 0) {
                    self.readingId = resp.data.id;
                    self.readingData.reading = resp.data.reading.replace(/\n/g, "<br />");
                    self.readingData.questions = resp.data.questions;

                    self.audioUrl = resp.data.files.audio;
                    self.imageUrl = resp.data.files.image;
                }
                else {
                    swal({
                        title: `Error!`,
                        text: 'Kesalahan pada server!',
                        buttonsStyling: false,
                        confirmButtonText: 'Kembali',
                        confirmButtonClass: 'btn btn-error btn-fill',
                        type: 'error'
                    });
                }
                self.inProgress = false;
            })
            .catch(function (error) {
                //console.log(error);
                self.inProgress = false;
            });
    },
    submitAnswer: function() {
        if (this.currentAnswer == -1) {
            swal('Pilih satu jawapan');
            return ;
        }


        var formData = new FormData();
        formData.append('data',
            JSON.stringify({
                'answer': this.currentAnswer,
                'question': this.readingData.questions[this.currentQId].id
            })
        );

        var self = this;
        self.inProgress = true;
        axios.post('/quiz/answer', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }})
            .then(function (response) {
                console.log(response.data);
                var resp = response.data;
                if (resp.status == 0) {
                    swal({
                        title: `Betul!`,
                        text: 'Pilihan Betul!',
                        buttonsStyling: false,
                        confirmButtonText: 'Berikut',
                        confirmButtonClass: 'btn btn-success btn-fill',
                        type: 'success'
                    })
                    .then(function () {
                        self.getNextQuestion();
                    });
                }
                else {
                    self.trial++;

                    if (self.trial++ < 2) {
                        swal({
                            title: `Belum Betul!`,
                            text: 'Jawapan belum betul!',
                            buttonsStyling: false,
                            confirmButtonText: 'Coba lagi',
                            confirmButtonClass: 'btn btn-error btn-fill',
                            type: 'error'
                        });
                    } else {
                        swal({
                            title: `Mari Belajar!`,
                            text: 'Jawapan belum lagi betul, mari belajar',
                            buttonsStyling: false,
                            showCancelButton: true,
                            confirmButtonText: 'Mula belajar',
                            cancelButtonText: 'Coba lagi',
                            confirmButtonClass: 'btn btn-success btn-fill',
                            cancelButtonClass: 'btn btn-success btn-fill',
                            type: 'error'
                        })
                        .then(function () {
                                window.open("https://www.w3schools.com");
                             },
                            function (dismiss) {
                              if (dismiss === 'cancel') {
                                // Try again
                              }
                            });
                    }
                }
                self.inProgress = false;
            })
            .catch(function (error) {
                //console.log(error);
                self.inProgress = false;
            });
    },
    reset: function() {
        this.inProgress = false;
        this.audioUrl = null;
        this.imageUrl = null;
        this.readingId = null;
        this.trial = 0;
        this.currentQId = 0;
        this.currentAnswer = -1;
        this.readingData.reading = '';
        this.readingData.questions = [];
    }
  }
})