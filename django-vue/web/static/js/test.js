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
    widgetStat: 'word_stat',
    inProgress: false,
    audioUrl: null,
    imageUrl: null,
    readingId: null,
    updated: null,
    readingData: {
        status: null,
        tags: '',
        title: '',
        reading: '',
        difficulty: 0,
        questions: [],
        wordList: [],
        stat: {
            words: 0,
            unique: 0,
            lexical_diversity: 0
        },
        score1: 0,
        score2: 0,
        totalSyllable: 0,
        totalSentence: 0
    }
  },
  computed: {
    statusText: function() {
        switch (this.readingData.status) {
        case 0:
            return "Draft";
        case 5:
            return "To be published";
        case 10:
            return "Published";
        default:
            return "-";
        }
    }
  },
  mounted: function () {
    var regex = new RegExp("test_list\/([^/?#]+).*"),
        results = regex.exec(window.location.href);

    if (!results) return;
    if (!results[1]) return;

    var pageAction = results[1].toLowerCase()

    if (pageAction === 'add') {
        var num_question = 4;
        var num_choices = 3;

        this.populateQuestionForm();
    }
    else if (pageAction === 'edit') {
        var readingId = getParameterByName('id');
        if (isNaN(readingId)) return;
        if (!(readingId > 0)) return;

        var formData = new FormData();
        formData.append('params', JSON.stringify({'type': 'request'}));

        var self = this;
        self.inProgress = true;
        axios.post('/test_list/edit?id=' + readingId, formData)
            .then(function (response) {
                var resp = response.data;
                if (resp.status == 0) {
                    self.readingId = resp.data.id;
                    self.readingData.status = resp.data.status;
                    self.updated = resp.data.updated;

                    self.readingData.title = resp.data.title;
                    self.readingData.reading = resp.data.reading;
                    self.readingData.difficulty = resp.data.difficulty;
                    self.readingData.questions = resp.data.questions;
                    self.readingData.tags = resp.data.tags;

                    self.imageUrl = resp.data.files.image;
                    self.audioUrl = resp.data.files.audio;

                    self.readingData.score1 = resp.data.stats.score_1;
                    self.readingData.score2 = resp.data.stats.score_2;
                    self.readingData.wordList = resp.data.stats.words;
                    self.readingData.totalSyllable = resp.data.stats.total_syllable;
                    self.readingData.totalSentence = resp.data.stats.total_sentence;

                    self.readingData.stat.words = resp.data.stats.total_word;
                    self.readingData.stat.unique = resp.data.stats.total_unique_word;
                    self.readingData.stat.lexical_diversity = resp.data.stats.lexical_diversity;
                }
                else {
                    swal({
                        title: `Kesilapan!`,
                        text: 'Bacaan tidak tersedia.',
                        buttonsStyling: false,
                        confirmButtonText: 'Kembali',
                        confirmButtonClass: 'btn btn-error btn-fill',
                        type: 'error'
                    }).then(function () {
                        window.location.replace("/test_list/");
                    });
                }
                self.inProgress = false;
            })
            .catch(function (error) {
                //console.log(error);
                self.inProgress = false;
            });
    }
  },
  methods: {
    addQuestion: function () {
      this.readingData.questions.push({
            question: "",
            choices: [
                { value: '' }
            ],
            tutorial: null,
            answer: 0
        });
    },
    addChoice: function(questionId) {
      this.readingData.questions[questionId].choices.push({ value: ''});
    },
    selectTutorial: function(questionId) {
        this.readingData.questions[questionId]['tutorial'] = this.$refs.tutorial[questionId].files[0];
    },
    saveReading: function(saving_type) {
        var formData = new FormData();

        if (this.$refs.image_uploader.uploadFiles.length > 0) {
            formData.append("image", this.$refs.image_uploader.uploadFiles[0].raw);
        }

        if (this.$refs.audio_uploader.uploadFiles.length > 0) {
            formData.append("audio", this.$refs.audio_uploader.uploadFiles[0].raw);
        }

        for (let i=0; i < this.readingData.questions.length; i++) {
            if (this.readingData.questions[i]["tutorial"] != null){
                console.log('here',this.readingData.questions[i]["tutorial"]);
                formData.append(''+i, this.readingData.questions[i]["tutorial"]);
            }
        }
        
        formData.append('data', JSON.stringify(this.readingData));
        formData.append('publish', saving_type);
        formData.append('params', JSON.stringify({'type': 'save'}));

        var self = this;
        self.inProgress = true;
        axios.post((self.readingId === null) ? '/test_list/add' : '/test_list/edit?id=' + self.readingId, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }})
            .then(function (response) {
                var resp = response.data;
                if (resp.status == 0) {
                    swal({
                        title: `Tersimpan!`,
                        text: 'Bacaan telah disimpan!',
                        buttonsStyling: false,
                        showCancelButton: true,
                        confirmButtonText: 'Add new reading',
                        cancelButtonText: 'Continue to edit',
                        confirmButtonClass: 'btn btn-success btn-fill',
                        cancelButtonClass: 'btn btn-success btn-fill',
                        type: 'success'
                    })
                    .then(function () {
                            console.log('reset');
                            self.resetForm();
                         },
                        function (dismiss) {
                          if (dismiss === 'cancel') {
                            // Continue to edit
                            console.log('continue');
                            self.readingId = resp.data.id;
                            self.updated = resp.data.updated;
                            self.readingData.status = resp.data.status;
                            self.audioUrl = resp.data.files.audio;
                            self.imageUrl = resp.data.files.image;
                          }
                        });
                }
                else {
                    swal({
                        title: `Error!`,
                        text: 'Bacaan tidak dapat disimpan!',
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
    removeChoice: function(questionId, choiceId) {
        this.readingData.questions[questionId].choices.splice(choiceId, 1);
        if (this.readingData.questions[questionId].choices.length <= this.readingData.questions[questionId].answer) {
            this.readingData.questions[questionId].answer = this.readingData.questions[questionId].choices.length-1;
        }
    },
    removeQuestion: function(questionId) {
        this.readingData.questions.splice(questionId, 1);
    },
    handleAudioUploaderChange: function(file, fileList) {
        var uploader = this.$refs.audio_uploader.uploadFiles;
        if (uploader.length > 1) {
            this.$refs.audio_uploader.uploadFiles = uploader.slice(-1);
        }
    },
    handleImageUploaderChange: function(file, fileList) {
        var uploader = this.$refs.image_uploader.uploadFiles;
        if (uploader.length > 1) {
            this.$refs.image_uploader.uploadFiles = uploader.slice(-1);
        }
    },
    resetForm: function() {
        this.updated = null;
        this.audioUrl = null;
        this.imageUrl = null;
        this.readingId = null;

        this.readingData.status = null;
        this.readingData.title = '';
        this.readingData.reading = '';
        this.readingData.difficulty = 0;
        this.readingData.questions = [];

        this.$refs.audio_uploader.clearFiles();
        this.$refs.image_uploader.clearFiles();

        this.populateQuestionForm();
    },
    populateQuestionForm: function() {
        var num_question = 0; //4;
        var num_choices = 0; //3;

        // Add 4 new questions
        for (var i=0; i < num_question; i++) {
            this.addQuestion();
            // Default: 4 choices/question
            for (var j=0; j < num_choices; j++) {
                this.addChoice(i);
            }
        }
    },
    fillScore: function() {
        this.readingData.difficulty = this.readingData.score1;
    },
    calculateScore: function() {
        var formData = new FormData();
        formData.append('reading', JSON.stringify(this.readingData.reading));

        var self = this;
        axios.post('/test_list/calculate', formData)
            .then(function (response) {
                console.log(response.data);
                var resp = response.data;
                if (resp.status == 0) {
                    self.readingData.score1 = resp.data.stats.score_1;
                    self.readingData.score2 = resp.data.stats.score_2;
                    self.readingData.wordList = resp.data.stats.words;
                    self.readingData.totalSyllable = resp.data.stats.total_syllable;
                    self.readingData.totalSentence = resp.data.stats.total_sentence;

                    self.readingData.stat.words = resp.data.stats.total_word;
                    self.readingData.stat.unique = resp.data.stats.total_unique_word;
                    self.readingData.stat.lexical_diversity = resp.data.stats.lexical_diversity;
                }
                else {
                }
            })
            .catch(function (error) {
                //console.log(error);
            });
    }
  }
})


$('#tutorialVideo').change(function() {
    alert("gh");
    var i = $(this).prev('label').clone();
    var file = $('#tutorialVideo')[0].files[0].name;
    $(this).parent('label').text(file);
});