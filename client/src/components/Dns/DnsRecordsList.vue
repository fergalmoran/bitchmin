<template>
    <v-card outlined>
        <template slot="progress">
            <v-progress-linear color="deep-purple" height="10" indeterminate>
            </v-progress-linear>
        </template>
        <v-card-title>Existing records</v-card-title>
        <v-card-text>
            <v-row>
                <v-alert type="error" v-if="errorMessage">
                    {{errorMessage}}
                </v-alert>
                <v-simple-table>
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Host</th>
                                <th class="text-left">IP</th>
                                <th class="text-left">Added</th>
                                <th class="text-left">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="host in records" :key="host.id">
                                <td>{{host.host}}</td>
                                <td>{{host.ip}}</td>
                                <td>{{host.created_on | formatDate}}</td>
                                <td>
                                    <v-btn-toggle dense
                                            background-color="pink"
                                            rounded>
                                        <v-btn icon color="pink"
                                                @click="refreshRecord(host)">
                                            <v-icon dark>mdi-refresh</v-icon>
                                        </v-btn>
                                        <v-btn icon
                                                color="pink"
                                                @click="verifyRecord(host)">
                                            <v-icon dark>mdi-eye-check</v-icon>
                                        </v-btn>
                                        <v-btn icon
                                                color="pink"
                                                @click="deleteRecord(host)">
                                            <v-icon dark>mdi-delete</v-icon>
                                        </v-btn>
                                    </v-btn-toggle>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { Component, PropSync, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';
import { DnsRecord } from '@/models/dnsRecord';
import dayjs from 'dayjs';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
import relativeTime from 'dayjs/plugin/relativeTime';
import localizedFormat from 'dayjs/plugin/localizedFormat';

@Component({
    name: 'DnsRecordsList',
    filters: {
        formatDate: (date: string) => {
            if (!date) {
                return null;
            }
            const d = dayjs(date);
            return d.format('L LT');
        },
    },
})
export default class DnsRecordsList extends Vue {
    @PropSync('inrecords')
    public records!: DnsRecord[];

    private callInProgress = false;

    errorMessage = '';

    async refreshRecord(host: DnsRecord) {
        this.callInProgress = true;
        console.log('DnsRecordsList', 'refreshRecord', host);
        const result = await dnsApi.refreshDnsRecord(host.host, host.ip);
        if (result.status === 'success') {
            Vue.toasted.success('Refreshed successfully');
        }
        this.callInProgress = false;
    }

    async verifyRecord(record: DnsRecord) {
        this.callInProgress = true;
        const result = await dnsApi.verifyDnsRecord(record.host, record.ip);
        if (result.status === 'success') {
            Vue.toasted.success(result.payload || 'Record checks out');
        } else {
            this.errorMessage = result.payload || 'Error checking record';
            Vue.toasted.error(this.errorMessage);
        }
        this.callInProgress = false;
    }

    async deleteRecord(record: DnsRecord) {
        this.callInProgress = true;
        const result = await dnsApi.deleteDnsRecord(record.host);
        if (result === 200) {
            Vue.toasted.success('Record deleted successfully');
            this.records = this.records.filter((t) => t.host !== record.host);
            console.log('DnsRecordsList', 'delete', this.records);
        }
        this.callInProgress = false;
    }

    mounted() {
        dayjs.extend(localizedFormat);
        console.log('DnsRecordsList', 'mounded_after', this.records);
    }
}
</script>
<style scoped="true">
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>
