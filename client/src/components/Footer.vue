<template>
    <footer class="footer">
        <div class="d-sm-flex justify-content-center justify-content-sm-between">
            <span class="text-muted text-center text-sm-left d-block d-sm-inline-block">
                Brought to you with
                <i class="mdi mdi-heart text-danger"></i> by
                <a href="https://podnoms.com/" target="_blank">PodNoms</a>.
            </span>
        </div>
    </footer>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Footer extends Vue {}
</script>
