<template>
    <v-container id="dashboard" fluid tag="section">
        <v-row>
            <v-col cols="12" sm="4" lg="4">
                <DnsZonesList :zones="dnsZones" />
            </v-col>
            <v-col cols="12" sm="8" lg="8">
                <DnsUpdateForm :zone="selectedZone" @hostAdded="onHostAdded" />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" sm="12" lg="12">
                <DnsRecordsList :inrecords="this.selectedZone.hosts" />
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
    selectedZone!: DnsZone;

    dnsRecords: DnsHost[] = [];

    onHostAdded(host: DnsHost) {
        this.selectedZone.hosts.unshift(host);
    }

    async mounted() {
        this.dnsZones = await dnsApi.getZones();
        if (this.dnsZones.length !== 0) {
            this.selectedZone = this.dnsZones[0];
            console.log('Setting hosts: ', this.dnsZones[0].hosts);
            this.dnsRecords = this.dnsZones[0].hosts;
        }
    }
}
</script>
