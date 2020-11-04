<template>
    <v-container id="dashboard" fluid tag="section">
        <v-row>
            <v-col cols="12" sm="4" lg="4">
                <DnsUpdateForm :inrecords="dnsRecords" />
            </v-col>
            <v-col cols="12" sm="8" lg="8">
                <DnsRecordsList :inrecords="dnsRecords" />
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import DnsRecordsList from '@/components/Dns/DnsRecordsList.vue';
import DnsUpdateForm from '@/components/Dns/DnsUpdateForm.vue';
import { DnsRecord } from '@/models';
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
