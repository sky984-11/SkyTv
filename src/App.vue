<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-25 18:07:17
 * @LastEditors: sky
-->
<template>
  <router-view v-touch:swipe.left="SwipeLeft('left')" v-touch:swipe.right="SwipeRight('right')" />

  <van-dialog v-model:show="show" title="更新提示" show-cancel-button>
  {{ updateMessage }}
</van-dialog>
</template>

<script setup name="App">

import { useRouter } from 'vue-router';
import { checkForUpdates } from "@/api/tools";
import { ref, onMounted } from "vue";

const show = ref(false);
const updateMessage = ref("");
const router = useRouter();

async function initData() {
  try {
    const client_version = import.meta.env.VITE_APP_VERSION;
    let params = {
      client_version: client_version,
    };
    const res = await checkForUpdates(params);
    if(res){
      show.value = true;
      updateMessage.value = `当前版本为:${res.client_version},请更新到最新版本:${res.latest_version},下载链接:${res.update_url}`;
    }
  } catch (error) {
    console.error('Error fetching updates:', error);
  }
}

function SwipeLeft(action) {
  console.log(action)
}
function SwipeRight(action) {
  console.log(action)
  router.go(-1);
}
initData()
</script>
