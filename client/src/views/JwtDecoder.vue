<template>
    <div>
        <div class="page-header">
            <h3 class="page-title">JWT Token Decoder</h3>
        </div>
        <div class="row">
            <div class="col-md-12 grid-margin stretch-card">
                <div class="card">
                    <div class="card-body">
                        <form class="forms-sample">
                            <div class="form-group">
                                <label for="exampleInputUsername1">Enter JWT Token</label>
                                <input
                                    type="text"
                                    class="form-control"
                                    v-model="token"
                                    @keydown="tokenChanged"
                                    placeholder="JWT Token"
                                />
                            </div>
                            <transition name="fade">
                                <div v-if="error" class="alert alert-danger" role="alert">{{error}}</div>
                            </transition>
                        </form>
                        <!-- <table class="table table-bordered" v-if="decoded.iat"> -->
                        <div class="row" v-if="decoded">
                            <div
                                class="col-md-6"
                                v-for="(value, propertyName) in decoded"
                                :key="propertyName"
                            >
                                <div class="wrapper ml-3">
                                    <dl>
                                        <dt>
                                            {{propertyName | narrativeText}}
                                            <small>({{propertyName}})</small>
                                        </dt>
                                        <dd>{{value | transformValue(propertyName)}}</dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import dayjs from 'dayjs';

import { decodeJwtToken, titleCase } from '@/utils';

@Component({
    components: {},
    filters: {
        narrativeText(value: string) {
            switch (value) {
                case 'iat':
                    return 'Issued At';
                case 'nbf':
                    return 'Not valid before';
                case 'jti':
                    return 'JWT Id';
                case 'exp':
                    return 'Expires at';
                default:
                    return titleCase(value);
            }
        },
        transformValue(value: string, propertyName: string) {
            if (isNaN(Number(value)) || propertyName === 'identity') {
                return value;
            }
            const d = dayjs(new Date(Number(value) * 1000));
            return `${value} : ${d.format('DD/MM/YYYY HH:mm')}`;
        },
    },
})
export default class JwtDecoder extends Vue {
    token = '';
    error = '';
    decoded: any = null;
    tokenChanged() {
        this.error = '';
        this.decoded = null;
        try {
            const token = decodeJwtToken(this.token);
            console.log('JwtDecoder', 'tokenChanged', token);
            this.decoded = token;
        } catch (e) {
            this.error = 'Invalid JWT Token';
            this.decoded = null;
        }
    }
}
</script>
<style scoped="true">
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>
