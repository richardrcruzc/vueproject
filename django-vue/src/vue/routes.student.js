import Vue from 'vue'
import VueRouter from 'vue-router'

import Dashboard from './views/student/Dashboard.vue'

Vue.use(VueRouter)

let routes = [
 {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
 }
];

export default new VueRouter({
    routes,
    linkActiveClass: 'active'
});