<template>
  <div>
    <video ref="player" class="plyr" :poster="poster" controls></video>
  </div>
</template>

<script setup name="Player">
import { onMounted, onBeforeUnmount, ref } from 'vue';
import Plyr from 'plyr';
import 'plyr/dist/plyr.css';
import Hls from 'hls.js';

// 定义 props
const props = defineProps({
  source: { type: String, required: true }, // 视频地址 (支持 m3u8)
  poster: { type: String, default: '' }, // 视频封面图
  controls: { type: Array, default: () => ['play', 'progress', 'volume', 'fullscreen'] }, // 控件配置
});

// 定义播放器 DOM 和实例
const player = ref(null);
let plyrInstance = null;

// 初始化 Plyr 和 HLS.js
const initPlayer = () => {
  if (Hls.isSupported() && props.source.endsWith('.m3u8')) {
    const hls = new Hls();
    hls.loadSource(props.source);
    hls.attachMedia(player.value);

    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      plyrInstance = new Plyr(player.value, {
        controls: props.controls,
      });
    });

    // 销毁 HLS.js 实例
    onBeforeUnmount(() => {
      hls.destroy();
    });
  } else {
    // 如果是普通视频格式，直接初始化 Plyr
    plyrInstance = new Plyr(player.value, {
      controls: props.controls,
    });
  }
};

// 生命周期：挂载时初始化播放器
onMounted(() => {
  initPlayer();
});

// 生命周期：卸载时销毁 Plyr 实例
onBeforeUnmount(() => {
  if (plyrInstance) {
    plyrInstance.destroy();
    plyrInstance = null;
  }
});
</script>

<style scoped>
/* 添加自定义样式 */
</style>
