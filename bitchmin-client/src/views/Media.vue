<template>
  <div class="about">
    <h1>Media Stuff</h1>
    <VideoTest />
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import VideoTest from '@/components/Media/VideoTest';
@Component({
    components: {
        VideoTest
    }
})
export default class Media extends Vue{}
</script>
