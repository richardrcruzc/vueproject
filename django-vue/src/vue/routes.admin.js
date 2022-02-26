import Vue from 'vue'
import VueRouter from 'vue-router'

import Dashboard from './views/admin/Dashboard.vue'
import Readings from './views/admin/Readings.vue'
import ReadingForm from './views/admin/ReadingForm.vue'

Vue.use(VueRouter)

let routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/readings',
        name: 'Readings',
        component: Readings
    },
    {
        path: '/readings/:action/:id?',
        name: 'Reading',
        component: ReadingForm
    },
];

export default new VueRouter({
    routes,
    linkActiveClass: 'active'
});