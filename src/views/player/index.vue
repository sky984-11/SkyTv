<script setup name="Player">
import { ref, watch, onMounted } from "vue";
import Hls from 'hls.js';

const props = defineProps({
  link: String,
});
const video = ref(null);

onMounted(() => {
  setupPlayer(props.link);
  addFullScreenListeners(); // 添加全屏事件监听器
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

function addFullScreenListeners() {
  const handleFullScreenChange = () => {
    if (isFullScreen()) {
      screen.orientation.lock('landscape'); // 进入全屏时锁定横屏
    } else {
      screen.orientation.unlock(); // 退出全屏时解锁屏幕方向
    }
  };

  document.addEventListener('fullscreenchange', handleFullScreenChange);
  document.addEventListener('webkitfullscreenchange', handleFullScreenChange);
  document.addEventListener('mozfullscreenchange', handleFullScreenChange);
}

function isFullScreen() {
  return document.fullscreenElement ||
         document.webkitFullscreenElement ||
         document.mozFullScreenElement ||
         false;
}
</script>

<template>
  <div class="relative">
    <video ref="video" class="w-full h-full" controls autoplay @dblclick="video.value.requestFullscreen()">
    </video>
  </div>
</template>

<style scoped>
/* 可以在这里添加你的样式 */
</style>