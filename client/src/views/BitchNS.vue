<template>
    <div>
        <div class="page-header">
            <h3 class="page-title">
                <span class="page-title-icon bg-gradient-primary text-white mr-2">
                    <i class="mdi mdi-dns"></i>
                </span> BitchMints Dynamic DNS Stuff
            </h3>
        </div>

        <div class="row">
            <div class="col-md-6 grid-margin stretch-card">
                <DnsUpdateForm :inrecords.sync="dnsRecords"/>
            </div>
            <div class="col-md-6 grid-margin stretch-card">
                <DnsRecordsList :inrecords.sync="dnsRecords"/>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import DnsRecordsList from '@/components/Dns/DnsRecordsList.vue';
import DnsUpdateForm from '@/components/Dns/DnsUpdateForm.vue';
import { DnsRecord } from '@/models/interfaces/dnsRecord';
import { dnsApi } from '@/api';

@Component({
    components: {
        HelloWorld,
        DnsRecordsList,
        DnsUpdateForm,
    },
})
export default class BitchNS extends Vue {
    dnsRecords: DnsRecord[] = [];
    async mounted() {
        this.dnsRecords = await dnsApi.getDnsRecords();
    }
}
</script>
