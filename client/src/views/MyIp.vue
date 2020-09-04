<template>
    <div>
        <div class="page-header">
            <h3 class="page-title">
                <span class="page-title-icon bg-gradient-primary text-white mr-2">
                    <i class="mdi mdi-ip"></i>
                </span> Your Network details Address is
            </h3>
        </div>

        <div class="row">
            <div class="col-md-4 stretch-card grid-margin">
                <div class="card">
                    <div class="card-body">{{ ip }}</div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 stretch-card grid-margin">
                <div class="card">
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover table-bordered ">
                                <thead class="thead-dark">
                                    <tr>
                                        <th scope="col">Name</th>
                                        <th scope="col">Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="(value, propertyName) in headers"
                                        :key="propertyName"
                                    >
                                        <th scope="row">{{propertyName}}</th>
                                        <td>{{value}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
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
