<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 14:32:44
 * @LastEditTime: 2024-07-03 14:22:43
 * @LastEditors: sky
-->
<script setup name="Group">
import { reactive, ref, onMounted ,watch} from "vue";
import { searchTv } from "@/api/tv";

import { useRoute,useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';

const tvList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载

const route = useRoute();
const router = useRouter();
const searchQuery = ref('');

// 监听路由变化，以便更新搜索关键词
watch(() => route.query.keyword, async (newKeyword) => {
  if (newKeyword) {
    console.log('路由变化，更新搜索关键词：', newKeyword);
    searchQuery.value = newKeyword;
    await initData(); // 确保每次关键词变化时都重新加载数据
  }
});

async function fetchData() {
    try {
        loading.value = true;
        const params = {
            keyword:searchQuery.value,
        };
        console.log(params)


        const res = await searchTv(params);

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

// 添加初始加载逻辑
onMounted(async () => {
  // 检查是否有初始关键词，如果有则加载数据
  if (route.query.keyword) {
    searchQuery.value = route.query.keyword;
  }
  await initData();
});
</script>

<template>
    <van-list >
        <div class="flex flex-wrap gap-4">
          <div class="relative w-[calc(50%-8px)]" v-for="item in tvList" :key="item.id" @click="toDetails(item)">
            <van-image :src="item.image" class="w-full h-auto" alt="视频缩略图" />
            <div
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
              {{ item.title }}
            </div>
          </div>
        </div>

      </van-list>
</template>
