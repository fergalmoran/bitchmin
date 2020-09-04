<template>
    <v-container grid-list-xl fluid>
        <v-layout row wrap class="mb-12">
            <v-card
                v-if="ip"
                class="mx-16"
                max-width="344"
            >
                <v-card-title>
                    Your IP Address is
                </v-card-title>
                <v-card-subtitle>
                    {{ ip }}
                </v-card-subtitle>

                <v-card-actions>
                    <v-btn class="ma-2" tile outlined color="success"
                           v-clipboard:copy="ip"
                           v-clipboard:success="onCopy"
                           v-clipboard:error="onError"
                    >
                        <v-icon left>mdi-clipboard-account</v-icon>
                        Copy
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-layout>
        <v-spacer></v-spacer>
        <v-layout row wrap>
            <v-expansion-panels popout>
                <v-expansion-panel>
                    <v-expansion-panel-header>More Network details....</v-expansion-panel-header>
                    <v-expansion-panel-content>
                        <v-simple-table>
                            <template v-slot:default>
                                <thead>
                                <tr>
                                    <th scope="col">Name</th>
                                    <th scope="col">Value</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="(value, propertyName) in headers" :key="propertyName">
                                    <th scope="row">{{ propertyName }}</th>
                                    <td>{{ value }}</td>
                                </tr>
                                </tbody>
                            </template>
                        </v-simple-table>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-layout>
    </v-container>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';

@Component({
    components: {}
})
export default class MyIp extends Vue {
    ip: any = 'Unknown';

    headers: any = {};

    async mounted() {
        this.ip = await dnsApi.getMyIP();
        this.headers = await dnsApi.getHeaders();
        console.log('MyIp', '', this.headers);
    }

    onCopy() {
        Vue.toasted.success('Address succesfully copied to clipboard');
    }

    onError() {
        Vue.toasted.error('There was an error copying the IP to your clipboard');
    }
}
</script>
