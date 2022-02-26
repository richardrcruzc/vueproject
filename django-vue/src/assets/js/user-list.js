axios.defaults.xsrfHeaderName = "X-CSRFToken";

var app = new Vue({
    el: '#app',
    data: {
        inProgress: false,
    },
    computed: {},
    mounted: function () {},
    methods: {
        reset: function(target_uid, target_user) {
            swal({
                title: `Menetapkan Kata Laluan`,
                text: 'Tetapkan semula kata laluan untuk: ' + target_user + '?',
                buttonsStyling: false,
                showCancelButton: true,
                confirmButtonText: 'Ya',
                cancelButtonText: 'Tidak',
                confirmButtonClass: 'btn btn-success btn-fill',
                cancelButtonClass: 'btn btn-success btn-fill',
                type: 'success'
            })
            .then(function () {
                var self = this;
                self.inProgress = true;
                axios.post('/user/reset?id=' + target_uid)
                    .then(function (response) {
                        var resp = response.data;
                        if (resp.status == 0) {
                            swal({
                                title: `Tersimpan!`,
                                text: 'Kata laluan telah diubah!',
                                buttonsStyling: false,
                                confirmButtonText: 'OK',
                                confirmButtonClass: 'btn btn-success btn-fill',
                                type: 'success'
                            })
                            .then(function () {});
                        }
                        else {
                            swal({
                                title: `Error!`,
                                text: 'Kata laluan tidak dapat diubah.',
                                buttonsStyling: false,
                                confirmButtonText: 'Kembali',
                                confirmButtonClass: 'btn btn-error btn-fill',
                                type: 'error'
                            });
                        }
                        self.inProgress = false;
                    })
                    .catch(function (error) {
                        self.inProgress = false;
                    });
                },
                function (dismiss) {
                });
        },
    }
})