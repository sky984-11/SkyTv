<!--
 * @Author: liupeng 1269861316@qq.com
 * @Date: 2024-06-27 13:35:22
 * @LastEditors: sky
 * @LastEditTime: 2025-01-03 16:34:10
 * @FilePath: /vue3-h5-template/src/views/details/index.vue
 * @Description: 详情页
-->
<script setup name="Details">
import { ref, onMounted } from "vue";
import { useTvStoreHook } from '@/store/modules/tvStore';
import { listEpisodes, getIptvM3u8 } from "@/api/video";
import Player from "@/views/player/index.vue";
import cache from "@/utils/cache";
import { getAnimeDetails, getAnimeEpisodes,playEpisodeInfo } from "@/api/jellyfin";
import { useRoute } from 'vue-router';


const route = useRoute();


const tvStore = useTvStoreHook();
// 在组件创建时获取 tvDetails
const tvDetails = ref({})



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

const playbackInfo = ref(null)

// /Videos/3d3a7b43-f612-c552-f7e6-0868d24d4b46/3d3a7b43f612c552f7e60868d24d4b46/Subtitles/2/0/Stream.js?api_key=e2582452814a465e8e87e8d68287a024

async function initData() {
  tvDetails.value = await getAnimeDetails(route.params.id)
  const { Items } = await getAnimeEpisodes(route.params.id)
  episodes.value = Items
  console.log(episodes.value)

  // if (tvDetails.type == '频道') {
  //   const res = await getIptvM3u8(tvDetails.id);
  //   m3u8Link.value = res

  // } else {
  //   const res = await listEpisodes(tvDetails.id);
  //   res.sort((a, b) => a.vod_episodes_index - b.vod_episodes_index);
  //   m3u8Link.value = res[0].play_urls.play_url
  //   videoDesc.value = res[0].vod_content
  //   videoTag.value = res[0].vod_tag
  //   episodes.value = res
  //   history.value.vod_episodes_index = res[0].vod_episodes_index
  //   history.value.vod_episodes = res[0].vod_episodes
  //   history.value.vod_tag = res[0].vod_tag
  //   history.value.play_url_id = res[0].id;
  //   activeEpisode.value = res[0].id;
  // }


}

const setActiveEpisode = async(episode) => {
  // console.log(episode)
  activeEpisode.value = episode.Id;
  playbackInfo.value = await playEpisodeInfo(episode.Id)
  
    // m3u8Link.value = episode.play_urls.play_url;
};

onMounted(() => {
  initData();
});

</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 视频部分 -->
    <Player :playbackInfo="playbackInfo" class="flex-grow"></Player>

    <!-- 选项卡部分 -->
    <van-tabs v-model:active="activeTab" class="mt-2">
      <van-tab v-for="tab in tabs" :key="tab" :title="tab" :disabled="tab !== '视频'">
        <div v-if="tab === '视频'" class="p-4">
          <!-- 视频详情 -->
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold truncate" :title="videoTitle">{{ tvDetails.Name }}</h2>

            <span class="ml-4">
              <span class=" text-gray-500">{{ tvDetails.ProductionYear }}</span>
              <span class="text-green-500 ml-4">{{ tvDetails.CommunityRating }}</span>
            </span>

          </div>
          <p class="mt-2 text-blue-500">{{ tvDetails.Tags?.join('，') }}</p>
          <p class="mt-2 text-gray-500">{{ tvDetails.Overview }}</p>

          <!-- Play Button Section -->
          <div class="flex justify-around mt-6  p-4 rounded-md">
            <van-icon name="play-circle-o" size="24px" />
          </div>
          <!-- 集数列表 -->
          <div class="flex overflow-x-auto whitespace-nowrap px-4 py-2">
            <button color="#7232dd" plain v-for="item in episodes" :key="item.Id" :class="[
              'px-4 py-2 mx-2 rounded-md transition-colors duration-300',
              item.Id === activeEpisode ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]" @click="setActiveEpisode(item)">
              {{ item.Name }}
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