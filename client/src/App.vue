<template>
    <v-app id="bitchmin">
        <TopBarNav />
        <SideBarNav />
        <v-main>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import TopBarNav from '@/components/TopBarNav.vue'; // @ is an alias to /src
import SideBarNav from '@/components/SideBarNav.vue'; // @ is an alias to /src
import Footer from '@/components/Footer.vue'; // @ is an alias to /src
import store from '@/store';
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
<style>
#keep .v-navigation-drawer__border {
    display: none;
}
</style>
