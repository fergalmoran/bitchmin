<template>
  <v-footer padless>
    <v-col
      class="text-center"
      cols="12"
    >
     Brought to you with
                <i class="mdi mdi-heart text-danger"></i> by
                <a href="https://podnoms.com/" target="_blank">PodNoms</a>.
    </v-col>
  </v-footer>

</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Footer extends Vue {}
</script>
