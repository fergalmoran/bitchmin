<template>
    <div id="container">
        <video id="video" width="640" height="480" autoplay></video>
        <button id="snap"></button>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
    components: {},
})
export default class VideoTest extends Vue {
    async mounted() {
        console.log('VideoTest', 'mounted');
        const video = document.getElementById('video') as HTMLVideoElement;
        if (video !== null) {
            if (navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices
                    .getUserMedia({ video: true })
                    .then(function (stream) {
                        video.srcObject = stream;
                    })
                    .catch(function (err0r) {
                        console.log('Something went wrong!');
                    });
            }
        }
    }
}
</script>

<style scoped=true>
#container {
    margin: 0px auto;
    width: 500px;
    height: 375px;
    border: 10px #333 solid;
}
#videoElement {
    width: 500px;
    height: 375px;
    background-color: #666;
}
</style>
