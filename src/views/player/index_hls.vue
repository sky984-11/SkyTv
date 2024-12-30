<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-25 14:18:22
 * @LastEditTime: 2024-12-27 08:43:58
 * @LastEditors: sky
-->
<script setup name="Player">
import { ref, watch, onMounted } from "vue";
import Hls from 'hls.js';

const props = defineProps({
  link: String,
});
const video = ref(null);

onMounted(() => {
  setupPlayer(props.link);
});

watch(() => props.link, (newLink) => {
  setupPlayer(newLink);
});

function setupPlayer(link) {
  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(link); 
    hls.attachMedia(video.value);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      video.value.play();
    });
  } else if (video.value.canPlayType('application/vnd.apple.mpegURL')) {
    video.value.src = link; 
    video.value.load();
    video.value.play();
  }
}
</script>

<template>
  <video ref="video" controls autoplay></video>
</template>

<style scoped></style>
