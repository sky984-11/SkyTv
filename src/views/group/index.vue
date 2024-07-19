<script setup name="Group">
import { ref, onMounted } from "vue";
import { listVideo } from "@/api/video";
import { useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';

const activeType = ref('剧集')  // 默认tab为剧集
const videoList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载
const finished = ref(false); //是否加载完成
const page = ref(1); // 当前页
const perPage = ref(20); // 每页数量
const tabList = ref(['剧集', '电影', '动漫'])
const router = useRouter();

async function fetchData() {
  try {
    loading.value = true;
    const params = {
      page: page.value,
      per_page: perPage.value,
      active_type: activeType.value
    };
    const res = await listVideo(params);

    if (res.length < perPage.value) {
      finished.value = true;
    }
    videoList.value = [...videoList.value, ...res];
    page.value += 1;
  } catch (error) {
    console.log(error)
  } finally {
    loading.value = false;
  }
}

function initData() {
  page.value = 1;
  videoList.value = [];
  finished.value = false;
  fetchData();
}

function onLoadData() {
  if (!finished.value) {
    fetchData();
  }
}

function onClickTab() {
  initData()
}

function toDetails(tv) {
  // 将详情数据写入store
  const tvStore = useTvStoreHook();
  tvStore.setTvDetails(tv);

  router.push({ name: 'Details' });

}

onMounted(() => {
  initData();
});
</script>

<template>
  <van-tabs v-model:active="activeType" @click-tab="onClickTab">
    <van-tab v-for="item in tabList" :key="item" :title="item" :name="item">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoadData"
        error-text="请求失败，点击重新加载">
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <div class="relative" v-for="item in videoList" :key="item.id" @click="toDetails(item)">
            <van-image :src="item.vod_pic_url" class="w-full h-auto" alt="视频缩略图" />
            <div
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
              {{ item.vod_title }}
            </div>
          </div>
        </div>
      </van-list>
    </van-tab>
  </van-tabs>
</template>
