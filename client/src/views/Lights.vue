
<template>
    <div>
        <div class="page-header">
            <h3 class="page-title">
                <span class="page-title-icon bg-gradient-primary text-white mr-2">
                    <i class="mdi mdi-home"></i>
                </span> Lights
            </h3>
        </div>
        <div class="row">
            <div class="col-md-6 grid-margin stretch-card">
                <div class="card">
                    <div class="card-body" v-if="currentLight && currentLight.supportsColour">
                        <form class="forms-sample" @submit.prevent="processUpdate">
                            <div class="form-group">
                                <label for="light-list">Choose light</label>

                                <v-select
                                    label="name"
                                    :options="lights"
                                    :value="currentLight"
                                    @input="light => onLightChange(light)"
                                />
                            </div>
                            <div class="form-group">
                                <label for="brightness">Brightness</label>
                                <input
                                    type="range"
                                    max="254"
                                    class="form-control-range"
                                    id="brightness"
                                    @change="light => changeBrightness(currentLight)"
                                    v-model="currentLight.brightness"
                                />
                            </div>
                            <div class="form-group">
                                <label for="colour">Colour</label>
                                <compact-picker
                                    v-model="currentLight.rgbColour"
                                    @input="changeColour"
                                ></compact-picker>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
/* eslint-disable no-var */
declare var require: (moduleId: string) => any;
/* eslint-disable @typescript-eslint/no-var-requires */
var colors = require('vue-color');

import { Component, Vue } from 'vue-property-decorator';
import { lightsApi } from '@/api';
import { Light } from '@/models/interfaces';

@Component({
    components: {
        'compact-picker': colors.Compact,
    },
})
export default class Lights extends Vue {
    lights: Light[] = [];
    currentLight: Light | null = null;
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
        if (result) {
            Vue.toasted.success('Brightness changed');
        } else {
            Vue.toasted.error('Failed to set the brightness');
        }
    }
    async changeColour(value: any) {
        if (this.currentLight != null) {
            this.currentLight.rgbColour = value.hex;
            const result = await lightsApi.changeColour(
                this.currentLight.id,
                this.currentLight.rgbColour
            );
            if (result) {
                Vue.toasted.success('Colour changed');
            } else {
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
