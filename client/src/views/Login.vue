<template>
    <div class="container-scroller">
        <div class="container-fluid page-body-wrapper full-page-wrapper">
            <div class="content-wrapper d-flex align-items-center auth">
                <div class="row flex-grow">
                    <div class="col-lg-4 mx-auto">
                        <div class="auth-form-light text-left p-5">
                            <div class="brand-logo">
                                <img src="/images/logo.png" />
                            </div>
                            <h4>Hello! let's get started</h4>

                            <h6 class="font-weight-light">Sign in to continue.</h6>
                            <p class="subtitle error-msg">{{ errorMsg }}</p>
                            <form class="pt-3">
                                <div class="form-group">
                                    <input
                                        type="email"
                                        class="form-control form-control-lg"
                                        id="exampleInputEmail1"
                                        placeholder="Email address"
                                        v-model="email"
                                    />
                                </div>
                                <div class="form-group">
                                    <input
                                        type="password"
                                        class="form-control form-control-lg"
                                        id="exampleInputPassword1"
                                        placeholder="Password"
                                        v-model="password"
                                    />
                                </div>
                                <div class="mt-3">
                                    <a
                                        class="btn btn-block btn-gradient-primary btn-lg font-weight-medium auth-form-btn"
                                        @click="authenticate"
                                    >SIGN IN</a>
                                </div>
                                <div class="my-2 d-flex justify-content-between align-items-center">
                                    <div class="form-check">
                                        <label class="form-check-label text-muted">
                                            <input type="checkbox" class="form-check-input" /> Keep me signed in
                                        </label>
                                    </div>
                                    <a href="#" class="auth-link text-black">Forgot password?</a>
                                </div>
                                <div class="text-center mt-4 font-weight-light">
                                    Don't have an account?
                                    <a
                                        href="register.html"
                                        class="text-primary"
                                        @click="register"
                                    >Create</a>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <!-- content-wrapper ends -->
        </div>
        <!-- page-body-wrapper ends -->
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import store from '@/store';

@Component({
    components: {},
})
export default class Login extends Vue {
    email = '';
    password = '';
    errorMsg = '';
    authenticate() {
        store.dispatch('login', { email: this.email, password: this.password })
            .then(() => {
                console.log('Login', 'store_dispatch_login');
                this.$router.push('/');
            });
    }
    register() {
        store
            .dispatch('register', {
                email: this.email,
                password: this.password,
            })
            .then(() => this.$router.push('/login'));
    }
}
</script>
