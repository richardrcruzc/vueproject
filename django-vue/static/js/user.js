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
    userId: null,
    userData: {
        username: '',
        password: '',
        role: 2
    }
  },
  computed: {
  },
  mounted: function () {
    var regex = new RegExp("user\/([^/?#]+).*"),
        results = regex.exec(window.location.href);

    if (!results) return;
    if (!results[1]) return;

    var pageAction = results[1].toLowerCase()

    if (pageAction === 'add') {
        this.resetForm();
    }
    else if (pageAction === 'edit') {
        var userId = getParameterByName('id');
        if (isNaN(userId)) return;
        if (!(userId > 0)) return;

        var formData = new FormData();
        formData.append('params', JSON.stringify({'type': 'request'}));

        var self = this;
        self.inProgress = true;
        axios.post('/user/edit?id=' + userId, formData)
            .then(function (response) {
                console.log(response.data);
                var resp = response.data;
                if (resp.status == 0) {
                    self.userId = resp.data.id;
                    self.userData.username = resp.data.username;
                    self.userData.role = resp.data.role;
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
  methods: {
    saveUser: function() {
        var formData = new FormData();
        formData.append('data', JSON.stringify(this.userData));
        formData.append('params', JSON.stringify({'type': 'save'}));

        var self = this;
        self.inProgress = true;
        axios.post((self.userId === null) ? '/user/add' : '/user/edit?id=' + self.userId, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }})
            .then(function (response) {
                console.log(response.data);
                var resp = response.data;
                if (resp.status == 0) {
                    swal({
                        title: `Tersimpan!`,
                        text: 'User telah disimpan!',
                        buttonsStyling: false,
                        showCancelButton: true,
                        confirmButtonText: 'Add new user',
                        cancelButtonText: 'Back to user list',
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
                            console.log('return ti user list');
                            window.location.replace("/user");
                          }
                        });
                }
                else {
                    swal({
                        title: `Error!`,
                        text: 'User tidak dapat disimpan!',
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
    backToUserList: function() {
        window.location.replace("/user");
    },
    resetForm: function() {
        this.userData.username = '';
        this.userData.password = '';
        this.userData.role = 2;
    }
  }
})