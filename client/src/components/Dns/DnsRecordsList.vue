<template>
    <div class="card">
        <div class="card-header">Existing records</div>
        <div class="card-body">
            <table class="table table-hover table-bordered" v-if="records && records.length > 0">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Host</th>
                        <th scope="col">IP</th>
                        <th scope="col">Added</th>
                        <th scope="col">#</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="host in records" :key="host.id">
                        <td>{{host.host}}</td>
                        <td>{{host.ip}}</td>
                        <td>{{host.created_on | formatDate}}</td>
                        <td>
                            <div class="btn-group" role="group" aria-label="Basic example">
                                <button
                                    @click="refreshRecord(host)"
                                    data-toggle="tooltip"
                                    title="Refresh record in BIND"
                                    type="button"
                                    class="btn btn-sm btn-primary btn-rounded btn-icon"
                                >
                                    <i class="mdi mdi-refresh"></i>
                                </button>
                                <button
                                    @click="verifyRecord(host)"
                                    data-toggle="tooltip"
                                    title="Verify record in BIND"
                                    type="button"
                                    class="btn btn-sm btn-primary btn-rounded btn-icon"
                                >
                                    <i class="mdi mdi-eye-check"></i>
                                </button>
                                <button
                                    @click="deleteRecord(host)"
                                    data-toggle="tooltip"
                                    title="Delete record"
                                    type="button"
                                    class="btn btn-sm btn-primary btn-rounded btn-icon"
                                >
                                    <i class="mdi mdi-delete"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, PropSync, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';
import { DnsRecord } from '@/models/interfaces/dnsRecord';
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

    async refreshRecord(host: DnsRecord) {
        console.log('DnsRecordsList', 'refreshRecord', host);
        const result = await dnsApi.refreshDnsRecord(host.host, host.ip);
        if (result.status === 'success') {
            Vue.toasted.success('Refreshed successfully');
        }
    }

    async verifyRecord(record: DnsRecord) {
        const result = await dnsApi.verifyDnsRecord(record.host, record.ip);
        if (result.status === 'success') {
            Vue.toasted.success(result.payload || 'Record checks out');
        } else {
            Vue.toasted.error(result.payload || 'Error checking record');
        }
    }

    async deleteRecord(record: DnsRecord) {
        const result = await dnsApi.deleteDnsRecord(record.host);
        if (result === 200) {
            Vue.toasted.success('Record deleted successfully');
            this.records = this.records.filter((t) => {
                return t.host !== record.host;
            });
            console.log('DnsRecordsList', 'delete', this.records);
        }
    }
    mounted() {
        dayjs.extend(localizedFormat);
        console.log('DnsRecordsList', 'mounded_after', this.records);
    }
}
</script>
