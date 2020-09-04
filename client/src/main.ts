import Vue from 'vue';
import App from './App.vue';
import Toasted from 'vue-toasted';

import router from './router';
import store from '@/store';
import $ from 'jquery';
import 'bootstrap';
import vuetify from '@/plugins/vuetify';


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
    render: (h) => h(App)
}).$mount('#app');
