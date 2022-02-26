import './bootstrap';
import router from './routes.student';
import StudentApp from './views/Student.vue';

window.Router = router;

new Vue({
  el: '#app',
  router,
  template: '<StudentApp/>',
  components: { StudentApp }
})
