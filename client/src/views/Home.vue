<template>
  <section>
    <v-parallax src="/images/bitchmints.jpg" height="1100">
      <v-layout column align-center justify-center class="white--text">
        <h1 class="white--text mb-2 display-1 text-xs-center"
            style="font-weight: 900; text-shadow: 3px 2px #000000">
          BitchMints Admin
        </h1>
      </v-layout>
    </v-parallax>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

@Component({
  components: {
    HelloWorld,
  },
})
export default class Home extends Vue {
}
</script>
