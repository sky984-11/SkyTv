<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-25 14:18:22
 * @LastEditTime: 2024-07-23 17:34:40
 * @LastEditors: sky
-->
<script setup name="Player">
import { ref, watch, onMounted } from "vue";
import Hls from 'hls.js';

const props = defineProps({
  link: String,
});
const video = ref(null);
const progress = ref(0); // 存储播放进度，实时更新播放记录中的数据

onMounted(() => {
  setupPlayer(props.link);
  addFullScreenListeners(); // 添加全屏事件监听器
  addTimeUpdateListener();
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

// 监听 timeupdate 事件以获取播放进度
function addTimeUpdateListener() {
  video.value.addEventListener('timeupdate', () => {
    const currentTime = video.value.currentTime;
    const duration = video.value.duration;
    if (!isNaN(duration)) {
      progress.value = (currentTime / duration) * 100;
    }
  });
}

// 根据播放进度百分比跳转到视频的特定位置
function seekTo(percentage) {
  const duration = video.value.duration;
  if (!isNaN(duration)) {
    const time = (percentage / 100) * duration;
    video.value.currentTime = time;
  }
}
</script>

<template>
  <div class="relative">
    <video ref="video" class="w-full h-full" controls autoplay @dblclick="video.value.requestFullscreen()">
    </video>
  </div>
</template>