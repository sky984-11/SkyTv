<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 14:32:44
 * @LastEditTime: 2024-07-29 13:30:06
 * @LastEditors: sky
-->
<script setup name="Group">
import { ref, onMounted} from "vue";

import { useRoute,useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';
import cache from "@/utils/cache";

const tvList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载

const route = useRoute();
const router = useRouter();
const searchQuery = ref('');


async function fetchData() {
    try {
        loading.value = true;
        const res = cache.getAllItems()
        console.log(res)

        tvList.value = res;
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false;
    }
}

function initData() {
  fetchData();
}

function toDetails(tv) {
    // 将详情数据写入store
    const tvStore = useTvStoreHook();
    tvStore.setTvDetails(tv);

    router.push({ name: 'Details' });

}

initData()
</script>

<template>
    <van-list >
        123
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <div class="relative" v-for="item in tvList" :key="item.id" @click="toDetails(item)">
            <van-image :src="item.vod_pic_url" class="w-full h-auto" alt="视频缩略图" />
            <div
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
              {{ item.vod_title }}
            </div>
          </div>
        </div>

      </van-list>
</template>
