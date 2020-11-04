<template>
    <v-row>
        <v-col cols="12" class="pa-4" sm="5" lg="5">
            <v-card class="elevation-12">
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title class="headline">JWT Token Decoder</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-card-text>
                    <v-form ref="form">
                        <v-text-field
                            v-model="token"
                            label="JWT Token"
                            @keydown="tokenChanged"
                            required
                        ></v-text-field>
                    </v-form>
                    <transition name="fade">
                        <div v-if="error" class="alert alert-danger" role="alert">{{error}}</div>
                    </transition>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" class="pa-4" sm="7" lg="7">
            <v-row>
                <v-col
                    cols="12"
                    sm="6"
                    v-for="(value, propertyName) in decoded"
                    :key="propertyName"
                >
                    <v-card class="pa-2">
                        <v-card-title>{{propertyName | narrativeText}}</v-card-title>
                        <v-card-subtitle>({{propertyName}})</v-card-subtitle>
                        <v-card-text>{{value | transformValue(propertyName)}}</v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
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
