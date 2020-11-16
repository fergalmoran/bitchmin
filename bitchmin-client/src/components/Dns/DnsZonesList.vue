<template>
    <v-card class="mx-auto">
        <v-card-title>Choose Zone</v-card-title>
        <v-card-text>
            <v-select :items="zones"
                      item-text="name"
                      item-value="id"
                      v-model="selectedZone"
                      @change="selectedZoneChanged()"
            ></v-select>
        </v-card-text>
    </v-card>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DnsZone } from '@/models/dnsZone';
import { mapActions } from 'vuex';

@Component({
    name: 'DnsHostsList',
    methods: {
        ...mapActions(['changeZone'])
    },
    props: ['zones']
})
export default class DnsZonesList extends Vue {

    selectedZone: DnsZone = { id: 1, zone: 'bitchmints.com', hosts: [] };

    @Prop({ required: true })
    public zones!: DnsZone[];

    public changeZone!: (zone: DnsZone) => void;

    selectedZoneChanged() {
        this.changeZone(this.selectedZone);
    }

}
</script>
