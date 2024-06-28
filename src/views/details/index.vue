<!--
 * @Author: liupeng 1269861316@qq.com
 * @Date: 2024-06-27 13:35:22
 * @LastEditors: sky
 * @LastEditTime: 2024-06-28 17:43:32
 * @FilePath: /vue3-h5-template/src/views/details/index.vue
 * @Description: 详情页
-->
<script setup name="Details">
import { ref, onMounted } from "vue";
import { useTvStoreHook } from '@/store/modules/tvStore';
import { listEpisodes } from "@/api/tv";
import Player from "@/views/player/index.vue";

const tvStore = useTvStoreHook();
// 在组件创建时获取 tvDetails
const tvDetails = tvStore.tvDetails;
// console.log(tvDetails)


const activeTab = ref('视频')
const tabs = ref(['视频', '讨论'])
const videoTitle = ref(tvDetails.title)
const videoDesc = ref(tvDetails.description)
const videoRating = ref(tvDetails.rating)
const episodes = ref([])
const m3u8Link = ref("")  // 播放link
const activeEpisode = ref(null);  // 选择的集数

async function initData() {
  const params = {
    tv_title: tvDetails.title,
  };

  const res = await listEpisodes(params);
  console.log(res)
  m3u8Link.value = res[0].link
  episodes.value = res
  activeEpisode.value = res[0].id;

}

const setActiveEpisode = (episode) => {
  m3u8Link.value = episode.link;
  activeEpisode.value = episode.id;
};

onMounted(() => {
  initData();
});

</script>

<template>
  <div class="flex flex-col">
    <!-- 视频部分 -->
    <Player :link="m3u8Link"></Player>

    <!-- 选项卡部分 -->
    <van-tabs v-model:active="activeTab" class="mt-2">
      <van-tab v-for="tab in tabs" :key="tab" :title="tab" :disabled="tab !== '视频'">
        <div v-if="tab === '视频'" class="p-4">
          <!-- 视频详情 -->
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold truncate" :title="videoTitle">{{ videoTitle }}</h2>
            <span class="ml-4 text-green-500">{{ videoRating }}</span>
          </div>
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
              {{ item.episode }}
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