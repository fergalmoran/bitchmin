<template>
    <v-card class="mx-auto">
        <v-card-title>Choose Zone</v-card-title>
        <v-card-text>
            <v-select :options="zones"
                      item-text="zone"
                      item-value="id"
            ></v-select>
        </v-card-text>
    </v-card>
</template>
<script lang="ts">
import { Component, PropSync, Vue } from 'vue-property-decorator';
import { DnsZone } from '@/models/dnsZone';

@Component({
    name: 'DnsHostsList'
})
export default class DnsZonesList extends Vue {

    @PropSync('inhosts')
    public zones!: DnsZone[];

    mounted() {
        console.log('DnsZonesList', 'mounted', this.zones);
    }
}
</script>
