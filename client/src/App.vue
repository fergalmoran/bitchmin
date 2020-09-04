<template>
    <div>
        <div class="container-scroller" v-if="isAuthenticated">
            <TopBarNav />
            <div class="container-fluid page-body-wrapper">
                <SideBarNav />
                <div class="main-panel">
                    <div class="content-wrapper">
                        <router-view />
                    </div>
                    <Footer />
                </div>
            </div>
        </div>

        <div v-if="!isAuthenticated">
            <router-view />
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import TopBarNav from '@/components/TopBarNav.vue'; // @ is an alias to /src
import SideBarNav from '@/components/SideBarNav.vue'; // @ is an alias to /src
import Footer from '@/components/Footer.vue'; // @ is an alias to /src
import vSelect from 'vue-select';

import store from '@/store';

Vue.component('v-select', vSelect);

@Component({
    components: {
        TopBarNav,
        SideBarNav,
        Footer,
    },
})
export default class App extends Vue {
    async mounted() {
        console.log('App', 'mounted');
        store.dispatch('loadInitialState');
    }
    get isAuthenticated() {
        return store.getters.isLoggedIn;
    }
}
</script>

<style lang="scss">
@import '@/assets/styles/_mixins.scss';
</style>
