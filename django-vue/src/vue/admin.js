import './bootstrap';
import router from './routes.admin';
import AdminApp from './views/Admin.vue';

window.Router = router;

new Vue({
  el: '#app',
  router,
  template: '<AdminApp/>',
  components: { AdminApp }
})
