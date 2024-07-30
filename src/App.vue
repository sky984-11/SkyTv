<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-29 17:22:12
 * @LastEditors: sky
-->
<template>
  <router-view />

  <van-dialog v-model:show="show" title="更新提示">
  
  <div v-html="updateMessage"></div>
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
    if(res && res.is_show){
      show.value = true;
      updateMessage.value = `<p>当前版本为: ${res.client_version}，请更新到最新版本: ${res.latest_version}</p><p>下载链接: <a href="${res.update_url}" target="_blank">${res.update_url}</a></p>`;
    }
  } catch (error) {
    console.error('Error fetching updates:', error);
  }
}

initData()
</script>
