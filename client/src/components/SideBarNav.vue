<template>
    <v-navigation-drawer v-model="drawer" app clipped color="grey lighten-4">
        <v-list dense class="grey lighten-4">
            <template v-for="(item, i) in items">
                <v-row v-if="item.heading" :key="i" align="center">
                    <v-col cols="6">
                        <v-subheader v-if="item.heading">{{ item.heading }}</v-subheader>
                    </v-col>
                    <v-col cols="6" class="text-right">
                        <v-btn small text>edit</v-btn>
                    </v-col>
                </v-row>
                <v-divider v-else-if="item.divider" :key="i" dark class="my-4"></v-divider>
                <v-list-item v-else :key="i" link @click="$router.push({ path: item.route })">
                    <v-list-item-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </template>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class SideBarNav extends Vue {
    drawer = null;
    items = [
        { title: 'Debug', icon: 'mdi-bug', route: 'debug' },
        { title: 'DNS Config', icon: 'mdi-dns', route: 'bitchns' },
        { title: 'IP Tools', icon: 'mdi-ip', route: 'myip' },
        { title: 'JWT Decoder', icon: 'mdi-code-array', route: 'jwt' },
        { title: 'Lights', icon: 'mdi-lightbulb', route: 'lights' },
    ];
}
</script>
