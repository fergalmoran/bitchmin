<template>
    <v-container id="dashboard" fluid tag="section">
        <v-row>
            <v-col cols="12" sm="4" lg="4">
                <DnsZonesList :inhosts="dnsZones" />
            </v-col>
            <v-col cols="12" sm="8" lg="8">
                <DnsUpdateForm :inrecords="dnsRecords" />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" sm="12" lg="12">
                <DnsRecordsList :inrecords="dnsRecords" />
            </v-col>
        </v-row>

    </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import DnsZonesList from '@/components/Dns/DnsZonesList.vue';
import DnsRecordsList from '@/components/Dns/DnsRecordsList.vue';
import DnsUpdateForm from '@/components/Dns/DnsUpdateForm.vue';
import { DnsHost } from '@/models';
import { dnsApi } from '@/api';
import { DnsZone } from '@/models/dnsZone';

@Component({
    components: {
        HelloWorld,
        DnsZonesList,
        DnsRecordsList,
        DnsUpdateForm
    }
})
export default class BitchNS extends Vue {
    dnsZones: DnsZone[] = [];
    dnsRecords: DnsHost[] = [];

    async mounted() {
        this.dnsZones = [
            { id: 1, zone: 'bitchmints.com' },
            { id: 2, zone: 'fergl.ie' }
        ];
        // this.dnsHosts = await dnsApi.getHosts();
        // this.dnsRecords = await dnsApi.getDnsRecords();
    }
}
</script>
