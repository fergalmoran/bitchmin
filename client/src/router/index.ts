import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import store from '@/store';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Lights from '../views/Lights.vue';
import About from '../views/About.vue';
import Debug from '../views/Debug.vue';
import BitchNS from '../views/BitchNS.vue';
import JwtDecoder from '../views/JwtDecoder.vue';
import MyIp from '../views/MyIp.vue';
import Media from '../views/Media.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: '/media',
    name: 'Media',
    component: Media,
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: '/bitchns',
    name: 'BitchNS',
    component: BitchNS,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/jwt',
    name: 'JwtDecoder',
    component: JwtDecoder,

  },
  {
    path: '/myip',
    name: 'MyIP',
    component: MyIp,
  },
  {
    path: '/debug',
    name: 'Debug',
    component: Debug,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/lights',
    name: 'Lights',
    component: Lights,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = new VueRouter({
  // abstract: true,
  mode: 'history',
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.name === 'Home') {
    console.log('index', 'Home Route Called', store.getters.isLoggedIn);
  }
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router;
