<template>
  <v-card class="mx-auto" outlined>
    <template slot="progress">
      <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
    </template>
    <v-card-title>Your Network details are</v-card-title>
    <v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Value</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(value, propertyName) in headers" :key="propertyName">
            <th scope="row">{{ propertyName }}</th>
            <td>{{ value }}</td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>

</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { dnsApi } from '@/api';

@Component({
  components: {},
})
export default class MyIp extends Vue {
  ip: any = 'Unknown';

  headers: any = {};

  async mounted() {
    this.ip = await dnsApi.getMyIP();
    this.headers = await dnsApi.getHeaders();
    console.log('MyIp', '', this.headers);
  }
}
</script>
