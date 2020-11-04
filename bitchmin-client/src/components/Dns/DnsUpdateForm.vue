<template>
    <v-card class="mx-auto" outlined>
        <template slot="progress">
            <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
        </template>
        <v-card-title>Add New Host</v-card-title>
        <v-card-text>
            <v-row align="start" justify="start" class="mx-0">
                <v-form ref="form" v-model="valid" :lazy-validation="lazy">
                    <v-text-field
                        v-model="hostName"
                        :rules="hostNameRules"
                        label="Host Name"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="ipAddress"
                        :rules="ipAddressRules"
                        label="IP Address"
                        required
                    ></v-text-field>

                    <v-btn color="warning" :disabled="!valid" @click="processUpdate">Add record</v-btn>
                </v-form>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script lang="ts">
import { Component, PropSync, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';
import { DnsRecord } from '@/models/dnsRecord';
import { DataApiResult } from '@/api/apiResult';

@Component({
    name: 'DnsUpdateForm',
})
export default class DnsUpdateForm extends Vue {
    msg = '';

    error = '';

    valid = true;

    lazy = false;

    hostName = '';

    hostNameRules = [
        (v: string) => !!v || 'Host name is required',
        (v: string) =>
            (v && v.length < 253) || 'Hostname cannot exceed 253 characters',
    ];

    ipAddress = '';

    ipAddressRules = [
        (v: string) => !!v || 'IP address is required',
        (v: string) =>
            // eslint-disable-next-line max-len
            /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(
                v
            ) || 'Invalid IP Address',
        (v: string) =>
            (v && v.length < 16) || 'IP address cannot exceed 16 characters',
    ];

    @PropSync('inrecords')
    public records!: DnsRecord[];

    validate() {
        // this.$refs.form.validate();
    }

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
            .catch((e: any) => {
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
