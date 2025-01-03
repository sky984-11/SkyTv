<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-12-30 09:02:00
 * @LastEditTime: 2025-01-03 16:52:09
 * @LastEditors: sky
-->
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import Hls from "hls.js";

const props = defineProps({
  playbackInfo: Object, // PlaybackInfo 的完整数据
  serverUrl: String,    // Jellyfin 服务器 URL
});

const videoRef = ref(null); // 视频 DOM 引用
let hlsInstance = null;

onMounted(() => {
  setupPlayer();
});

onUnmounted(() => {
  if (hlsInstance) {
    hlsInstance.destroy();
    hlsInstance = null;
  }
});

function setupPlayer() {
  if(!props.playbackInfo){
    return
  }
  const mediaSource = props.playbackInfo.MediaSources[0];

  if (!mediaSource) {
    console.error("No media source available.");
    return;
  }

  const playUrl = generatePlaybackUrl(
    props.serverUrl,
    mediaSource.Id,
    props.playbackInfo.PlaySessionId,
  );

  if (Hls.isSupported() && mediaSource.Container.includes("m3u8")) {
    hlsInstance = new Hls();
    hlsInstance.loadSource(playUrl);
    hlsInstance.attachMedia(videoRef.value);
  } else {
    videoRef.value.src = playUrl;
  }

  videoRef.value.play();
}

function generatePlaybackUrl(serverUrl, mediaSourceId, playSessionId) {
  return import.meta.env.VITE_BASE_API + '/Videos/' + mediaSourceId + '/stream?Static=true&PlaySessionId=' + playSessionId

}
</script>

<template>
  <div class="player-container">
    <video ref="videoRef" class="video-player" controls autoplay></video>
  </div>
</template>

<style>
.player-container {
  width: 100%;
  height: 100%;
  position: relative;
}
.video-player {
  width: 100%;
  height: 100%;
}
</style>
