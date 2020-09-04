<template>
    <v-app id="login" class="secondary">
        <v-content>
            <v-container fluid fill-height>
                <v-layout align-center justify-center>
                    <v-flex xs12 sm8 md4 lg4>
                        <v-card class="elevation-1 pa-3">
                            <v-card-text>
                                <div class="layout column align-center">
                                    <img src="/images/bitchmints.jpg" alt="Vue Material Admin" width="120" height="120">
                                    <h1 class="flex my-4 primary--text">Bitch::Mints</h1>
                                </div>
                                <v-form>
                                    <v-text-field
                                        name="login"
                                        label="Login"
                                        type="text"
                                        v-model="email"
                                        :error="error"
                                        :rules="[rules.required]" />
                                    <v-text-field
                                        type="password"
                                        name="password"
                                        label="Password"
                                        id="password"
                                        :rules="[rules.required]"
                                        v-model="password"
                                        :error="error" />
                                </v-form>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn block color="primary" @click="authenticate" :loading="loading">Login</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-flex>
                </v-layout>
                <v-snackbar
                    v-model="showResult"
                    :timeout="2000"
                    top>
                    {{ result }}
                </v-snackbar>
            </v-container>
        </v-content>
    </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import store from '@/store';

@Component({
    components: {}
})
export default class Login extends Vue {
    loading: false;
    error = false;
    rules = {
        required: (value: string) => !!value || 'Required.'
    };
    email = '';

    password = '';

    errorMsg = '';

    authenticate() {
        if (!this.email || !this.password) {
            this.result = 'Email and Password can\'t be null.';
            this.showResult = true;
            return;
        }
        store
            .dispatch('login', { email: this.email, password: this.password })
            .then(() => {
                console.log('Login', 'store_dispatch_login');
                this.$router.push('/');
            }).error(() => {
            this.error = true;
            this.result = 'Email or Password is incorrect.';
            this.showResult = true;
        });
    }

    register() {
        store
            .dispatch('register', {
                email: this.email,
                password: this.password
            })
            .then(() => this.$router.push('/login'));
    }
}
</script>
