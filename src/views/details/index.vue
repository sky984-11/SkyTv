<!--
 * @Author: liupeng 1269861316@qq.com
 * @Date: 2024-06-27 13:35:22
 * @LastEditors: sky
 * @LastEditTime: 2025-01-07 08:53:53
 * @FilePath: /vue3-h5-template/src/views/details/index.vue
 * @Description: 详情页
-->
<script setup name="Details">
import { ref, onMounted } from "vue";
import { useTvStoreHook } from '@/store/modules/tvStore';
import { getIptvM3u8 } from "@/api/video";
import Player from "@/views/player/index.vue";
import cache from "@/utils/cache";
import { getAnimeDetails, getAnimeEpisodes, playEpisodeInfo } from "@/api/jellyfin";
import { useRoute } from 'vue-router';


const route = useRoute();


const tvStore = useTvStoreHook();
// 在组件创建时获取 tvDetails
const tvDetails = ref({})

const activeTab = ref('视频')
const tabs = ref(['视频', '讨论'])

const episodes = ref([])
const activeEpisode = ref(null);  // 选择的集数


const playbackInfo = ref(null)

async function initData() {
  tvDetails.value = await getAnimeDetails(route.params.id)
  const { Items } = await getAnimeEpisodes(route.params.id)
  episodes.value = Items
  console.log(episodes.value)
}

const setActiveEpisode = async (episode) => {
  activeEpisode.value = episode.Id;
  playbackInfo.value = await playEpisodeInfo(episode.Id)

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
            <h2 class="text-xl font-semibold truncate" :title="tvDetails.Name">{{ tvDetails.Name }}</h2>

            <span class="flex items-center">
              <span class="text-gray-500">{{ tvDetails.ProductionYear }}</span>
              <span class="text-green-500 ml-4 flex items-center">
                {{ tvDetails.CommunityRating }}
                <svg-icon name="rank" class="ml-1" />
              </span>
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