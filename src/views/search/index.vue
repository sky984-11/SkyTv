<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 14:32:44
 * @LastEditTime: 2025-01-08 14:31:33
 * @LastEditors: sky
-->
<script setup name="Group">
import { reactive, ref, onMounted, watch } from "vue";
import { searchAnimes } from "@/api/jellyfin";

import CardList from "@/components/public/CardList.vue"

import { useRoute } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';

const videoList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载

const route = useRoute();
const searchQuery = ref('');

// 监听路由变化，以便更新搜索关键词
watch(() => route.query.keyword, async (newKeyword) => {
  if (newKeyword) {
    console.log('路由变化，更新搜索关键词：', newKeyword);
    searchQuery.value = newKeyword;
    initData(); // 确保每次关键词变化时都重新加载数据
  }
});

async function fetchData() {
  try {
    loading.value = true;
    const res = await searchAnimes(searchQuery.value);
    console.log(res)

    videoList.value = res.Items;
  } catch (error) {
    console.log(error)
  } finally {
    loading.value = false;
  }
}

function initData() {
  fetchData();
}

// 添加初始加载逻辑
onMounted(async () => {
  // 检查是否有初始关键词，如果有则加载数据
  if (route.query.keyword) {
    searchQuery.value = route.query.keyword;
  }
  initData();
});
</script>

<template>
  <card-list :animes="videoList" :loading="loading"></card-list>
</template>
