<template>
    <div class="card">
        <div class="card-header">Add new record</div>
        <div class="card-body">
            <form class="forms-sample" @submit.prevent="processUpdate">
                <div class="form-group">
                    <label for="ipAddress">IP Address</label>
                    <input type="text" class="form-control" id="ipAddress" v-model="ipAddress" />
                </div>

                <div class="form-group">
                    <label for="hostName">Host name</label>
                    <input type="text" class="form-control" id="hostName" v-model="hostName" />
                </div>
                <div class="alert alert-danger" role="alert" v-if="error">{{error}}</div>
                <button type="submit" class="btn btn-gradient-primary mr-2">Submit</button>
                <button class="btn btn-light">Cancel</button>
            </form>
            <p v-if="msg">{{ msg }}</p>
        </div>
    </div>
</template>
<script lang="ts">
import { Component, PropSync, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';
import { DnsRecord } from '@/models/interfaces/dnsRecord';
import { DataApiResult } from '@/api/apiResult';

@Component({
    name: 'DnsUpdateForm',
})
export default class DnsUpdateForm extends Vue {
    public ipAddress = '';
    public hostName = '';
    public msg = '';
    error = '';

    @PropSync("inrecords")
    public records!: DnsRecord[];

    processUpdate() {
        dnsApi
            .updateDnsRecord(this.hostName, this.ipAddress)
            .then((r: DataApiResult<DnsRecord>) => {
                if (r.status === 'success') {
                    this.error = '';
                    Vue.toasted.success('Update successful');
                    if (r.payload) {
                        this.records.unshift(r.payload);
                        this.$emit('update:inrecords', this.records);
                    }
                    this.ipAddress = '';
                    this.hostName = '';
                } else {
                    this.error = 'Unable to add DNS record';
                }
            })
            .catch((e) => {
                console.log('DnsUpdateForm', 'error', e);
                if (e.response && e.response.data.payload) {
                    this.error = e.response.data.payload;
                } else {
                    this.error = e;
                }
            });
    }
}
</script>
