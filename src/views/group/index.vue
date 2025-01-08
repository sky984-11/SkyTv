<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2025-01-08 14:38:29
 * @LastEditors: sky
-->

<!-- 后续增加分类过滤后去掉注释(根据评分，标签，年代)，增加后端分页 -->

<script setup name="Group">
import { ref, onMounted } from "vue";

import { useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';
import imageMap from "@/utils/imageMap.js"
import { getAnimes } from "@/api/jellyfin";

import CardList from "@/components/public/CardList.vue"

const videoList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载

const page = ref(1); // 当前页
const perPage = ref(20); // 每页数量

const router = useRouter();

async function fetchData() {
  try {
    loading.value = true;

    const res = await getAnimes();
    console.log(res)
    videoList.value = res.Items
    // const params = {
    //   page: page.value,
    //   per_page: perPage.value,
    //   active_type: activeType.value
    // };

    // if (activeType.value != '频道') {
    //   var res = await listVideo(params);
    //   if (res.length < perPage.value) {
    //     finished.value = true;
    //   }
    //   videoList.value = [...videoList.value, ...res];
    //   page.value += 1;
    // } else {
    //   videoList.value = Object.keys(imageMap).map(title => ({
    //     id: imageMap[title].match(/\/IPTV\/(\w+)\.png/)[1],
    //     vod_pic_url: imageMap[title],
    //     vod_title: title,
    //   }));
    // }
    // console.log(videoList.value )

  } catch (error) {
    console.log(error)
    loading.value = false;
  } finally {
    loading.value = false;
  }
}

function initData() {
  page.value = 1;
  videoList.value = [];
  fetchData();
}

function onLoadData() {
  // if (!finished.value) {
    fetchData();
  // }
}


onMounted(() => {
  initData();
});
</script>

<template>
 <card-list :animes="videoList" :loading="loading" @onLoadData="onLoadData"></card-list>
</template>
