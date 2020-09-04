import Vue from 'vue';
import Vuex from 'vuex';

import { authApi } from '@/api';
import { userApi } from '@/api';

import { UserLoginModel } from '@/models/interfaces';

Vue.use(Vuex);
const isObjectEmpty = (object: Record<string, any>) => {
    let isEmpty = true;
    for (const keys in object) {
        isEmpty = false;
        break;
    }
    return isEmpty;
};
export default new Vuex.Store({
    state: {
        status: '',
        accessToken: localStorage.getItem('access_token') || '',
        refreshToken: localStorage.getItem('refresh_token') || '',
        user: {},
    },
    mutations: {
        authRequest(state) {
            state.status = 'loading';
        },
        loadUser(state) {
            state.status = 'loading';
        },
        loadUserSuccess(state, { user }) {
            state.status = 'success';
            state.user = user;
        },
        authError(state) {
            state.status = 'error';
        },
        authSuccess(state, { user, accessToken, refreshToken }) {
            state.status = 'success';
            state.accessToken = accessToken;
            state.refreshToken = refreshToken;
            state.user = user;
        },
        logout(state) {
            state.status = '';
            state.accessToken = '';
            state.refreshToken = '';
            state.user = {};
        },
        updateToken(state, { accessToken, refreshToken }) {
            console.log('STORE', 'UpdatingTokens' );
            state.accessToken = accessToken;
            state.refreshToken = refreshToken;
        },
    },
    actions: {
        loadInitialState({ commit }) {
            console.log('index', 'loadInitialState', 'Starting');
            return new Promise((resolve, reject) => {
                console.log('index', 'loadInitialState', 'Resolving');
                //if we have a JWT but don't have a user, we should try to load the user
                if (
                    this.state.accessToken &&
                    (!this.state.user || isObjectEmpty(this.state.user))
                ) {
                    console.log('index', 'loadInitialState', 'Starting');
                    commit('loadUser');
                    userApi.getUser().then((resp) => {
                        console.log('index', 'loadInitialState', 'Done', resp);
                        commit('loadUserSuccess', {
                            user: resp,
                        });
                        resolve(resp);
                    });
                } else {
                    resolve({});
                }
            });
        },
        login({ commit }, user: UserLoginModel) {
            return new Promise((resolve, reject) => {
                console.log('store', 'login_start');
                commit('refreshToken');
                authApi
                    .login(user)
                    .then((resp) => {
                        localStorage.setItem(
                            'access_token',
                            resp.data.accessToken
                        );
                        localStorage.setItem(
                            'refresh_token',
                            resp.data.refreshToken
                        );
                        commit('authSuccess', {
                            user: resp.data.user,
                            accessToken: resp.data.accessToken,
                            refreshToken: resp.data.refreshToken,
                        });
                        resolve(resp);
                    })
                    .catch((err) => {
                        commit('authError');
                        localStorage.removeItem('token');
                        reject(err);
                    });
            });
        },
        logout({ commit }) {
            return new Promise((resolve, reject) => {
                commit('logout');
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                resolve();
            });
        },
    },
    getters: {
        isLoggedIn: (state) => !!state.accessToken,
        authStatus: (state) => state.status,
    },
});
