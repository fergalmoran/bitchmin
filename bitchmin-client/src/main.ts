import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import Toasted from 'vue-toasted';
import VueClipboard from 'vue-clipboard2';


Vue.config.productionTip = false;
Vue.use(VueClipboard);
Vue.use(Toasted, {
    theme: 'toasted-primary',
    position: 'top-right',
    duration: 2000
});

new Vue({
    router,
    store,
    vuetify,
    render: (h: any) => h(App)
}).$mount('#app');
