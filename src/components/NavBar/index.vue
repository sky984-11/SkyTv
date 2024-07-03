<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-03 13:50:15
 * @LastEditors: sky
-->
<script setup>
import { useDarkMode, useToggleDarkMode } from "@/hooks/useToggleDarkMode";
import { ref } from "vue";
import { useRouter } from 'vue-router';

const router = useRouter();

const searchKey = ref("")

const onClickRight = () => {
  useToggleDarkMode();
};

function onSearch(val) {
  router.push({ name: 'Search', query: { keyword: val } });
  if (val == "") {
    router.push({ name: 'Home' });
  }

}

function onCancel() {
  searchKey.value = ""
  router.push({ name: 'Home' });
}

</script>

<template>
  <van-nav-bar fixed placeholder @click-right="onClickRight">

    <template #left>
      <van-search v-model="searchKey" placeholder="请输入搜索关键词" @search="onSearch" @clear="onCancel" />
    </template>
    <template #right>
      <svg-icon class="text-[18px]" :name="useDarkMode() ? 'light' : 'dark'" />
    </template>
  </van-nav-bar>
</template>

<style scoped></style>
