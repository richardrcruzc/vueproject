import Vue from 'vue';
import VueRouter from 'vue-router';
import axios from 'axios';
//import {Button, Collapse, CollapseItem, Pagination, Table, TableColumn, Upload} from 'element-ui'
import Element from 'element-ui'

window.Vue = Vue;
Vue.use(VueRouter);

Vue.use(Element);
/*
Vue.use(Button);
Vue.use(Collapse);
Vue.use(CollapseItem);
Vue.use(Pagination);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Upload);
*/

window.axios = axios;
window.axios.defaults.headers.common = {
    'X-Requested-With': 'XMLHttpRequest'
};

window.sharedData = {
    serverHost: '/',
    events: {
    }
};

window.Event = new class {
    constructor() {
        this.vue = new Vue();
    }

    fire(event, data = null) {
        this.vue.$emit(event, data);
    }

    listen(event, callback) {
        this.vue.$on(event, callback);
    }
}

window.Helper = new class {
    constructor() {
    }

    convertToDate(unixTime) {
        let date = new Date(unixTime*1000);

        return ('0' + date.getDate()).slice(-2) + '/'
            + ('0' + (date.getMonth() + 1)).slice(-2)
            + '/' + date.getFullYear() + ' '
            + ('0' + date.getHours()).slice(-2) + ':'
            + ('0' + date.getMinutes()).slice(-2);
    }
}