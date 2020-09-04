<template>
    <v-row>
        <v-col cols="12" sm="4" lg="4" v-if="lights.length !== 0 && currentLight">
            <v-select
                label="name"
                item-text="name"
                item-value="id"
                :items="lights"
                v-model="currentLight"
            />
            <v-slider
                @change="light => changeBrightness(currentLight)"
                :max="254"
                v-model="currentLight.brightness"
                label="Brightness"
            ></v-slider>
            <v-row justify="space-around">
                <v-color-picker
                    @input="changeColour"
                    v-model="currentLight.rgbColour"
                    class="ma-2"
                    :swatches="swatches"
                    show-swatches
                    hide-mode-switch
                ></v-color-picker>
            </v-row>
        </v-col>
    </v-row>
</template>

<script lang="ts">
/* eslint-disable no-var */
declare var require: (moduleId: string) => any;
/* eslint-disable @typescript-eslint/no-var-requires */
var colors = require('vue-color');

import { Component, Vue } from 'vue-property-decorator';
import { lightsApi } from '@/api';
import { Light } from '@/models/interfaces';
import { debounce } from 'decko';

@Component({
    components: {
        'compact-picker': colors.Compact,
    },
})
export default class Lights extends Vue {
    lights: Light[] = [];
    currentLight: Light | null = null;
    swatches = [
        ['#FF0000', '#AA0000', '#550000'],
        ['#FFFF00', '#AAAA00', '#555500'],
        ['#00FF00', '#00AA00', '#005500'],
        ['#00FFFF', '#00AAAA', '#005555'],
        ['#0000FF', '#0000AA', '#000055'],
    ];
    async mounted() {
        this.lights = await lightsApi.getLights();
        this.currentLight = this.lights[0];
        console.log('Lights', 'mounted', 'lights', this.lights);
    }

    async changeBrightness(light: Light): Promise<void> {
        console.log('Lights', 'changeBrightness', light);
        const result = await lightsApi.changeBrightness(
            light.id,
            parseInt(light.brightness.toString())
        );
        if (!result) {
            Vue.toasted.error('Failed to set the brightness');
        }
    }

    @debounce(1000)
    async changeColour(value: any) {
        console.log('Lights', 'changeColour', value);
        if (this.currentLight != null) {
            this.currentLight.rgbColour = value;
            const result = await lightsApi.changeColour(
                this.currentLight.id,
                this.currentLight.rgbColour
            );
            if (!result) {
                Vue.toasted.error('Failed to set the colour');
            }
        }
    }

    onLightChange(light: any): void {
        console.log('Lights', 'onLightChange', light, this.currentLight);
        this.currentLight = light;
    }
}
</script>
