<!--
 * @Author: liupeng 1269861316@qq.com
 * @Date: 2024-06-27 13:35:22
 * @LastEditors: sky
 * @LastEditTime: 2024-08-02 10:25:24
 * @FilePath: /vue3-h5-template/src/views/details/index.vue
 * @Description: 详情页
-->
<script setup name="Details">
import { ref, onMounted } from "vue";
import { useTvStoreHook } from '@/store/modules/tvStore';
import { listEpisodes,getIptvM3u8 } from "@/api/video";
import Player from "@/views/player/index.vue";
import cache from "@/utils/cache";
// 观看超过5%缓存记录


const tvStore = useTvStoreHook();
// 在组件创建时获取 tvDetails
const tvDetails = tvStore.tvDetails;
// console.log(tvDetails)


const activeTab = ref('视频')
const tabs = ref(['视频', '讨论'])
const videoTitle = ref(tvDetails.vod_title)
const videoDesc = ref("")
const videoTag = ref(tvDetails.vod_tag)
const videoRating = ref(tvDetails.rating)
const episodes = ref([])
const m3u8Link = ref("")  // 播放link
const activeEpisode = ref(null);  // 选择的集数
const history = ref(tvDetails)  // 播放历史缓存


async function initData() {
  if (tvDetails.type == '频道') {
    const res = await getIptvM3u8(tvDetails.id);
    m3u8Link.value = res

  } else {
    const res = await listEpisodes(tvDetails.id);
    res.sort((a, b) => a.vod_episodes_index - b.vod_episodes_index);
    m3u8Link.value = res[0].play_urls.play_url
    videoDesc.value = res[0].vod_content
    videoTag.value = res[0].vod_tag
    episodes.value = res
    history.value.vod_episodes_index = res[0].vod_episodes_index
    history.value.vod_episodes = res[0].vod_episodes
    history.value.vod_tag = res[0].vod_tag
    history.value.play_url_id = res[0].id;
    activeEpisode.value = res[0].id;
  }


}

const setActiveEpisode = (episode) => {
  m3u8Link.value = episode.play_urls.play_url;
  activeEpisode.value = episode.id;
};

onMounted(() => {
  initData();
});

</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 视频部分 -->
    <Player :link="m3u8Link" :history="history" class="flex-grow"></Player>

    <!-- 选项卡部分 -->
    <van-tabs v-model:active="activeTab" class="mt-2" v-if="tvDetails.type != '频道'">
      <van-tab v-for="tab in tabs" :key="tab" :title="tab" :disabled="tab !== '视频'">
        <div v-if="tab === '视频'" class="p-4">
          <!-- 视频详情 -->
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold truncate" :title="videoTitle">{{ videoTitle }}</h2>
            <span class="ml-4 text-green-500">{{ videoRating }}</span>
          </div>
          <p class="mt-2 text-blue-500">{{ videoTag }}</p>
          <p class="mt-2 text-gray-500">{{ videoDesc }}</p>

          <!-- Play Button Section -->
          <div class="flex justify-around mt-6  p-4 rounded-md">
            <van-icon name="play-circle-o" size="24px" />
          </div>
          <!-- 集数列表 -->
          <div class="flex mt-4 overflow-x-auto">
            <button color="#7232dd" plain v-for="item in episodes" :key="item.id"
              :class="['px-4 py-2 mx-1 rounded-md', item.id === activeEpisode ? 'bg-blue-500 ' : '']"
              @click="setActiveEpisode(item)">
              {{ item.vod_episodes }}
            </button>
          </div>
        </div>
        <div v-else class="p-4">
          <!-- 其他选项卡内容 -->
          <p>暂无内容</p>
        </div>
      </van-tab>
    </van-tabs>
  </div>
</template>