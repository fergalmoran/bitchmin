import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import Toasted from 'vue-toasted';

Vue.config.productionTip = false;

Vue.use(Toasted, {
  theme: 'toasted-primary',
  position: 'top-right',
  duration: 2000,
});

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
