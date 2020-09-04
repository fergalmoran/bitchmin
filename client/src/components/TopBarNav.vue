<template>
    <v-app-bar app clipped-left color="#90CAF9">
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <span class="title ml-3 mr-5">
            Bitch&nbsp;
            <span class="font-weight-light">Mints</span>
        </span>
        <v-spacer></v-spacer>
        <v-btn icon>
            <v-icon>mdi-exit-to-app</v-icon>
        </v-btn>
    </v-app-bar>
</template>
<script>
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class TopBarNav extends Vue {
    signout() {
        this.$store.dispatch('logout').then(() => this.$router.push('/login'));
    }
}
</script>
