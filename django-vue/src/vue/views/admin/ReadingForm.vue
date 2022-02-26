<template>
    <div id="app" class="container-fluid">
        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Reading</h4>
                    </div>
                    <div class="card-content">
                        <form>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <textarea v-model="readingData.reading" rows="15" class="form-control"
                                                  placeholder="Write a reading material"></textarea>
                                    </div>
                                </div>
                            </div>
                            <fieldset class="form-horizontal">
                                <div class="form-group">
                                    <label class="col-sm-2 control-label" style="text-align: left;">Difficulty</label>
                                    <div class="col-sm-4">
                                        <input v-model="readingData.difficulty" type="number" class="form-control"
                                               placeholder="Score">
                                    </div>
                                </div>
                            </fieldset>
                            <div class="row">
                                <fieldset class="col-md-6">
                                    <div class="form-group">
                                        <div class="row" v-if="imageUrl" v-cloak>
                                            <span class="col-md-12">
                                                <a :href="imageUrl" target="_blank"><i class="ti-image"></i></a>
                                            </span>
                                        </div>
                                        <label>Image</label>
                                        <el-upload
                                            class="file-uploader"
                                            name="image-uploader"
                                            action="#"
                                            ref="image_uploader"
                                            :show-file-list="true"
                                            :on-change="handleImageUploaderChange"
                                            :auto-upload="false">
                                                <el-button slot="trigger" size="small" type="primary">select file</el-button>
                                                <div class="el-upload__tip" slot="tip">jpg/png files</div>
                                        </el-upload>
                                    </div>
                                </fieldset>
                                <fieldset class="col-md-6">
                                    <div class="form-group">
                                        <div class="row" v-if="audioUrl" v-cloak>
                                            <span class="col-md-12">
                                                <a :href="audioUrl" target="_blank"><i class="ti-image"></i></a>
                                            </span>
                                        </div>
                                        <label>Audio</label>
                                        <el-upload
                                            class="file-uploader"
                                            name="audio-uploader"
                                            action="#"
                                            ref="audio_uploader"
                                            :show-file-list="true"
                                            :on-change="handleAudioUploaderChange"
                                            :auto-upload="false">
                                                <el-button slot="trigger" size="small" type="primary">select file</el-button>
                                                <div class="el-upload__tip" slot="tip">wav/mp3 files</div>
                                        </el-upload>
                                    </div>
                                </fieldset>
                            </div>
                            <fieldset class="form-horizontal">
                                <div class="form-group">
                                    <label class="col-sm-2 control-label" style="text-align: left;">Tags</label>
                                    <div class="col-sm-10">
                                        <input v-model="readingData.tags" type="text" class="form-control" placeholder="Comma separated tags">
                                    </div>
                                </div>
                            </fieldset>
                            <div class="clearfix"></div>
                        </form>
                    </div>
                    <hr>
                    <div class="card-header">
                        <h4 class="card-title">Questions</h4>
                    </div>
                    <div class="card-content">
                        <el-collapse v-for="(qData, qIndex) in readingData.questions" :key="'q' + qIndex">
                            <el-collapse-item :title="'Question' + qIndex + 1" :name="qIndex">
                                <template slot="title">
                                    Question {{ qIndex + 1 }}
                                    <a @click.stop="removeQuestion(qIndex)" href="#"><i class="header-icon ti-close"></i></a>
                                </template>
                                <div class="row">
                                    <div class="col-md-12">
                                        <div class="form-group">
                                            <textarea v-model="qData.question" rows="3"
                                                      class="form-control border-input"
                                                      placeholder="Insert a question"></textarea>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-5">
                                        <div class="choice-wrapper" v-for="(cData, cIndex) in qData.choices" :key="'c' + cIndex">
                                            <div class="col-md-12">
                                                <input type="radio" v-model="qData.answer" :name="'qAnswers' + qIndex" :value="cIndex">
                                                <input type="text" v-model="cData.value" class="form-control border-input" :placeholder="'Choice ' + (cIndex+1)">
                                                <a @click.prevent="removeChoice(qIndex, cIndex)" href="#"><i class="ti-close"></i></a>
                                            </div>
                                            <div class="clearfix"></div>
                                        </div>
                                    </div>

                                    <div class="col-md-3">
                                        <div class="text-center">
                                            <button @click="addChoice(qIndex)"
                                                    class="btn btn-wd btn-sm">
                                                Add Choices
                                            </button>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="text-center">
                                            <input type="file" ref="tutorial" @change="selectTutorial(qIndex)"
                                                    class="btn btn-wd btn-sm">                                               
                                        </div>
                                    </div>
                                </div>
                            </el-collapse-item>
                        </el-collapse>
                    </div>
                    <div class="card-footer">
                        <div class="text-center">
                            <button @click="addQuestion" class="btn btn-wd btn-sm">Add Question</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Details</h4>
                    </div>
                    <div class="card-content">
                        <div class="row widget">
                            <div class="col-md-12" style="margin-top: 15px;">
                                <p>Status: <span v-cloak>{{ statusText }}</span></p>
                                <p>Last updated: <span v-if="updated" v-cloak>{{ updated }}</span><span v-else="!updated">-</span></p>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="text-center">
                                <a @click="saveReading(false)" class="btn" :class="{disabled: inProgress}">Save</a>
                                <a @click="saveReading(true)" class="btn btn-fill" :class="{disabled: inProgress}">Publish</a>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Reading Calculator</h4>
                    </div>
                    <div class="card-content">
                        <form>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Kata</label>
                                        <input type="number" class="form-control border-input" placeholder="Kata">
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Sub-kata</label>
                                        <input type="number" class="form-control border-input" placeholder="Sub-kata">
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <label>Kalimat</label>
                                        <input type="number" class="form-control border-input" placeholder="Kalimat">
                                    </div>
                                </div>

                                <div class="text-center">
                                    <a class="btn">Auto-fill</a>
                                    <a type="submit" class="btn btn-fill btn-wd">Calculate</a>
                                </div>
                            </div>
                        </form>
                    </div>
                </div -->
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'app',
    data () {
        return {
            inProgress: false,
            audioUrl: null,
            imageUrl: null,
            readingId: null,
            updated: null,
            tutorial: '',
            readingData: {
                status: null,
                tags: '',
                reading: '',
                difficulty: 0,
                questions: []
            }
        }
    },
    computed: {
        statusText: function() {
            switch (this.readingData.status) {
            case 0:
                return "Draft";
            case 10:
                return "Published";
            default:
                return "-";
            }
        }
    },
    mounted() {
        let pageAction = this.$route.params.action.toLowerCase();

        if (pageAction === 'add') {
            let num_question = 4;
            let num_choices = 3;

            this.populateQuestionForm();
        }
        else if (pageAction === 'edit') {
            let readingId = getParameterByName('id');
            if (isNaN(readingId)) return;
            if (!(readingId > 0)) return;

            let formData = new FormData();
            formData.append('params', JSON.stringify({'type': 'request'}));

            let self = this;
            self.inProgress = true;
            axios.post('/reading/edit?id=' + readingId, formData)
                .then(function (response) {
                    console.log(response.data);
                    let resp = response.data;
                    if (resp.status == 0) {
                        self.readingId = resp.data.id;
                        self.readingData.status = resp.data.status;
                        self.updated = resp.data.updated;

                        self.readingData.reading = resp.data.reading;
                        self.readingData.difficulty = resp.data.difficulty;
                        self.readingData.questions = resp.data.questions;
                        self.readingData.tags = resp.data.tags;

                        self.imageUrl = resp.data.files.image;
                        self.audioUrl = resp.data.files.audio;
                    }
                    else {
                    }
                    self.inProgress = false;
                })
                .catch(function (error) {
                    //console.log(error);
                    self.inProgress = false;
                });
        }
    },
	created() {

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
        saveReading: function(isPublished) {
            let formData = new FormData();

            if (this.$refs.image_uploader.uploadFiles.length > 0) {
                formData.append("image", this.$refs.image_uploader.uploadFiles[0].raw);
            }

            if (this.$refs.audio_uploader.uploadFiles.length > 0) {
                formData.append("audio", this.$refs.audio_uploader.uploadFiles[0].raw);
            }
            
            for (let i=0; i <= this.readingData.questions.length; i++) {
                if (this.readingData.questions[i]["tutorial"] != null){
                    console.log('here',this.readingData.questions[i]["tutorial"]);
                    formData.append(''+i, this.readingData.questions[i]["tutorial"]);
                }
            }

            if (isPublished) {
                this.readingData.status = 10;
            }
            else {
                this.readingData.status = 0;
            }

            formData.append('data', JSON.stringify(this.readingData));
            formData.append('params', JSON.stringify({'type': 'save'}));

            let self = this;
            self.inProgress = true;
            axios.post((self.readingId === null) ? '/reading/add' : '/reading/edit?id=' + self.readingId, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }})
                .then(function (response) {
                    console.log(response.data);
                    let resp = response.data;
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
            let uploader = this.$refs.audio_uploader.uploadFiles;
            if (uploader.length > 1) {
                this.$refs.audio_uploader.uploadFiles = uploader.slice(-1);
            }
        },
        handleImageUploaderChange: function(file, fileList) {
            let uploader = this.$refs.image_uploader.uploadFiles;
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
            this.readingData.reading = '';
            this.readingData.difficulty = 0;
            this.readingData.questions = [];

            this.$refs.audio_uploader.clearFiles();
            this.$refs.image_uploader.clearFiles();

            this.populateQuestionForm();
        },
        populateQuestionForm: function() {
            let num_question = 4;
            let num_choices = 3;

            // Add 4 new questions
            for (let i=0; i < num_question; i++) {
                this.addQuestion();
                // Default: 4 choices/question
                for (let j=0; j < num_choices; j++) {
                    this.addChoice(i);
                }
            }
        }
    }
}
</script>
