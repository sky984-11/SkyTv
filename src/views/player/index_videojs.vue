<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-08-21 15:46:33
 * @LastEditTime: 2024-12-27 14:10:39
 * @LastEditors: sky
-->
<template>
  <video-player
    class="video-js"
    controls
    :options="playerOptions"
    :style="{ width: '640px', height: '360px' }"
  />
</template>

<script setup>
import { defineComponent ,ref} from 'vue';
import { VideoPlayer } from '@videojs-player/vue';
import 'video.js/dist/video-js.css';


const props = defineProps({
  src: {
      type: String,
      required: true, // Ensure the src is provided when the component is used
    },
})

const playerOptions = ref({
        autoplay: false,  // 如果true,浏览器准备好时开始回放。
        controls: true,
        loop: false, // 导致视频一结束就重新开始。
        preload: 'auto',
        volume: 0.6,
        techOrder: ['html5'], // Ensure proper tech order
        sources: [
          {
            src: props.src, // URL to your HLS stream
            type: 'application/x-mpegURL', // HLS MIME type
          },
        ],
      })
</script>