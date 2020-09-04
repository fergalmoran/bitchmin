<template>
    <div class="card">
        <div class="card-header header-sm">
            <div class="d-flex align-items-center">
                <div class="wrapper d-flex align-items-center media-info text-linkedin">
                    <h2 class="card-title ml-3">Existing records</h2>
                </div>
                <div class="wrapper ml-auto action-bar" v-if="callInProgress">
                    <i class="mdi mdi-image-filter-vintage text-danger mdi-spin"></i>
                </div>
            </div>
        </div>
        <div class="card-body">
            <transition name="fade">
                <div class="alert alert-fill-danger" role="alert" v-if="errorMessage">
                    <i class="mdi mdi-alert-circle"></i>
                    {{errorMessage}}
                </div>
            </transition>
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
                                    :disabled="callInProgress"
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
import { error } from 'jquery';

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
            this.records = this.records.filter((t) => {
                return t.host !== record.host;
            });
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
