axios.defaults.xsrfHeaderName = "X-CSRFToken";

Vue.component('modal', {
    template: '#modal-template',
    props: {
        type: 0,
        tutorialUrl: null,
        tutorial: {
            questionType: 0,
            level: 0,
            current: 0,
            images: []
        },
        dict: {
            error: false,
            loading: true,
            error_desc: '',
            word: '',
            definition: ''
        }
    },
    computed: {
        imageSource() {
            if (this.tutorial.current < this.tutorial.images.length) return this.tutorial.images[this.tutorial.current];
            else return '';
        }
    },
    methods: {
        nextSlide() {
            this.tutorial.current++;
            if (this.tutorial.current >= this.tutorial.images.length) this.$emit('close');
        }
    }
});

Vue.component('tutorial', {
    template: '#modal-tutorial',
    props: {
        tutorialUrl: null,
    }
});

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
        showPopup: false,
        popupType: 0,
        inProgress: false,
        audioUrl: null,
        imageUrl: null,
        tutorialUrl: null,
        readingId: null,
        trial: 0,
        currentQId: 0,
        currentAnswer: -1,
        readingData: {
            reading: '',
            level: 0,
            reading_component: [],
            questions: []
        },
        dict: {
            error: false,
            loading: true,
            error_desc: '',
            word: '',
            definition: ''
        },
        tutorialData: {
            questionType: 0,
            level: 0,
            current: 0,
            images: []
        },
        tutorials: [
            {name: 'P1', slides: [9]},
            {name: 'P2', slides: [9]},
            {name: 'P3', slides: [8, 8, 6, 6]},
            {name: 'P3', slides: [8, 8, 6, 6]},
            {name: 'P5', slides: [10, 10, 8, 8]},
            {name: 'P5', slides: [10, 10, 8, 8]},
            {name: 'S1', slides: [10, 10, 10, 8]},
            {name: 'S1', slides: [10, 10, 10, 8]},
            {name: 'S3', slides: [12, 12, 10, 8]},
            {name: 'S3', slides: [12, 12, 10, 8]}],
        quizToken: -1,
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

    },
    methods: {
        generateTutorialMaterials: function(difficultyLevel, question) {
            let tutorialMaterials = [];
            let level = difficultyLevel-1;
            if ((level < 0) || (level > 9)) return tutorialMaterials;

            let slideSet = (question < this.tutorials[level].slides.length) ? question : this.tutorials[level].slides.length-1;

            for (let i=0; i < this.tutorials[level].slides[slideSet]; i++) {
                tutorialMaterials.push('/static/tutorials/' + this.tutorials[level].name + '_' + (slideSet+1) + '/Slide' + (i+1) + '.jpg');
            }

            return tutorialMaterials;
        },
        openTutorial: function(url) {
            // this.tutorialData.images = this.generateTutorialMaterials(this.readingData.level, this.currentQId);

            // this.tutorialData.questionType = self.currentQId;
            // this.tutorialData.current = 0;
            // this.tutorialData.level = this.readingData.level;
            // this.tutorialUrl = url
            this.popupType = 1;
            this.showPopup = true;
        },
        getNextQuestion: function() {
            this.currentAnswer = -1;
            this.currentQId++;
            this.trial = 0;
            var self = this;
            if (this.currentQId >= this.readingData.questions.length) {
                swal({
                    title: `Selesai!`,
                    text: 'Soalan untuk bacaan ini telah selesai!',
                    buttonsStyling: false,
                    showCancelButton: true,
                    confirmButtonText: 'Bacaan selanjutnya',
                    cancelButtonText: 'Berhenti',
                    confirmButtonClass: 'btn btn-success btn-fill',
                    cancelButtonClass: 'btn btn-success btn-fill',
                    type: 'success'
                })
                .then(function () {
                        //console.log('next question');
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
            axios.post('/quiz/question', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }})
                .then(function (response) {
                    var resp = response.data;
                    if (resp.status == 0) {
                        self.readingId = resp.data.id;
                        //console.log(resp.data);
                        //resp.data.reading.replace(/\n/g, "<br/>");
                        //var reading_content = reading_content.split(/[\n,;-. ]/);

                        //
                        //self.readingData.reading_component = resp.data.reading.split(' ');

                        var reading_content = resp.data.reading.replace(/\n/g, "<br/>").split(' ');
                        var mod_content = '';

                        for (var i=0; i < reading_content.length; i++) {
                            mod_content += '<span onclick="self.app.findWord(this)" data-word="' + reading_content[i] + '">' + reading_content[i] + '</span> ';
                        }
                        self.readingData.reading = mod_content;
                        self.readingData.questions = resp.data.questions;
                        self.readingData.level = resp.data.level;

                        //self.quizToken = resp.data.qtoken;
                    }
                    else {
                        swal({
                            title: `Error!`,
                            text: 'Ralat!',
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
                    'token': this.quizToken,
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
                    //console.log(response.data);
                    var resp = response.data;
                    if (resp.status == 0) {
                        self.quizToken = resp.qtoken;
                        if (resp.correct == 1) {
                            swal({
                                title: `Betul!`,
                                text: 'Pilihan Betul!',
                                buttonsStyling: false,
                                confirmButtonText: 'Seterusnya',
                                confirmButtonClass: 'btn btn-success btn-fill',
                                type: 'success'
                            })
                            .then(function () {
                                self.getNextQuestion();
                            });
                        }
                        else {
                            self.trial++;
                            // swal({
                            //     title: `Tidak betul!`,
                            //     text: 'Jawapan anda tidak betul.',
                            //     buttonsStyling: false,
                            //     confirmButtonText: 'Cuba lagi',
                            //     confirmButtonClass: 'btn btn-error btn-fill',
                            //     type: 'error'
                            // });
                            /* */
                            if (self.trial++ < 2) {
                                swal({
                                    title: `Tidak betul!`,
                                    text: 'Jawapan anda tidak betul.',
                                    buttonsStyling: false,
                                    confirmButtonText: 'Cuba lagi',
                                    confirmButtonClass: 'btn btn-error btn-fill',
                                    type: 'error'
                                });
                            } else {
                                swal({
                                    title: `Mari Belajar!`,
                                    text: 'Jawapan anda tidak betul. Mari kita belajar!',
                                    buttonsStyling: false,
                                    showCancelButton: true,
                                    confirmButtonText: 'Mula belajar',
                                    cancelButtonText: 'Cuba lagi',
                                    confirmButtonClass: 'btn btn-success btn-fill',
                                    cancelButtonClass: 'btn btn-success btn-fill',
                                    type: 'error'
                                })
                                .then(function () {
                                        // window.open("/belajar/?id="+self.readingData.questions[self.currentQId].id);
                                        
                                        console.log(self.readingData.questions[self.currentQId].tutorial_file)
                                        if (self.readingData.questions[self.currentQId].tutorial_file == null) {
                                            self.tutorialUrl = null;
                                            console.log('when null',self.tutorial);
                                        }
                                        else {
                                            self.tutorialUrl = self.readingData.questions[self.currentQId].tutorial_file;
                                            console.log('when not null',self.tutorial);
                                        }                            
                                        self.openTutorial();
                                     },
                                    function (dismiss) {
                                      if (dismiss === 'cancel') {
                                        // Try again
                                      }
                                    });
                            }
                            /* */
                        }
                    }
                    else {
                        // Error
                    }
                    self.inProgress = false;
                })
                .catch(function (error) {
                    //console.log(error);
                    self.inProgress = false;
                });
        },
        openDictionary: function() {
            var x = document.getElementById("wordSearchBox");

            if (x.value.length > 0) {
                var el = {textContent: x.value};
                this.findWord(el);
            }
        },
        findWord: function(el){
            var selectedWord = el.textContent;
            var self = this;
            this.popupType = 0;
            this.showPopup = true;
            this.dict.word = selectedWord;
            this.dict.definition = '';
            this.dict.loading = true;
            this.dict.error = false;

            axios.get('/tools/dict/' + selectedWord)
                .then(function (response) {
                    var resp = response.data;
                    self.dict.loading = false;
                    if (resp.status == 0) {
                        self.dict.definition = resp.def;
                    }
                    else {
                        self.dict.error_desc = "Carian tiada dalam kamus.";
                        self.dict.error = true;
                    }
                })
                .catch(function (error) {
                    //console.log(error);
                    self.dict.loading = false;
                    self.dict.error = false;
                });
        },
        reset: function() {
            this.inProgress = false;
            this.audioUrl = null;
            this.imageUrl = null;
            this.tutorialUrl= null,
            this.readingId = null;
            this.trial = 0;
            this.currentQId = 0;
            this.currentAnswer = -1;
            this.quizToken = -1;
            this.readingData.reading = '';
            this.readingData.questions = [];
        }
    }
})