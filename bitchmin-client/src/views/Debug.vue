<template>
    <div class="about">
        <h1>This is the debug page</h1>
    </div>
</template>
<script>
import { Component, Vue } from 'vue-property-decorator';
import { debugApi } from '@/api';

@Component({
    components: {},
})
export default class Lights extends Vue {
    async mounted() {
        this.lights = await debugApi.getDebug();
        this.currentLight = this.lights[0];
        console.log('Lights', 'mounted', 'lights', this.lights);
    }
}
</script>
