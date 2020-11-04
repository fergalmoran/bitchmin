<template>
    <v-app id="bitchmin">
        <TopBarNav v-on:toggle-sidebar="drawerOpen = !drawerOpen" v-if="isAuthenticated" />
        <SideBarNav v-if="isAuthenticated" v-model="drawerOpen" />
        <v-main>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-main>
        <Footer />
    </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import TopBarNav from '@/components/TopBarNav.vue'; // @ is an alias to /src
import SideBarNav from '@/components/SideBarNav.vue'; // @ is an alias to /src
import Footer from '@/components/Footer.vue'; // @ is an alias to /src

@Component({
    components: {
        TopBarNav,
        SideBarNav,
        Footer,
    },
})
export default class App extends Vue {
    drawerOpen = true;

    async mounted() {
        this.$store.dispatch('loadInitialState');
    }

    get isAuthenticated() {
        return this.$store.getters.isLoggedIn;
    }
}
</script>
<style>
#keep .v-navigation-drawer__border {
    display: none;
}
</style>
