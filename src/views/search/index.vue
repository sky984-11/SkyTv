<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 14:32:44
 * @LastEditTime: 2025-01-08 15:30:47
 * @LastEditors: sky
-->

<template>
  <card-list :fetchFunction="searchAnimes" ref="cardRef"></card-list>
</template>


<script setup name="Group">
import { reactive, ref, onMounted, watch } from "vue";
import { searchAnimes } from "@/api/jellyfin";

import CardList from "@/components/public/CardList.vue"

import { useRoute } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';


const loading = ref(false);  //下拉加载
const cardRef = ref(null);
const route = useRoute();
const searchQuery = ref('');

// 监听路由变化，以便更新搜索关键词
watch(() => route.query.keyword, async (newKeyword) => {
  if (newKeyword) {
    console.log('路由变化，更新搜索关键词：', newKeyword);
    cardRef.value.initData(newKeyword); // 确保每次关键词变化时都重新加载数据
  }
});

</script>


