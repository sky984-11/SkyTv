<script setup>
import { useDarkMode, useToggleDarkMode } from "@/hooks/useToggleDarkMode";
import { ref } from "vue";


const searchKey = ref("")


const onClickRight = () => {
  useToggleDarkMode();
};

function onSearch(val){
  console.log(val)

  isSearch.value = true

}

</script>

<template>
  <van-nav-bar fixed placeholder @click-right="onClickRight">
    
    <template #left>
      <van-search v-model="searchKey" placeholder="请输入搜索关键词" @search="onSearch" />
    </template>
    <template #right>
      <svg-icon class="text-[18px]" :name="useDarkMode() ? 'light' : 'dark'" />
    </template>
  </van-nav-bar>
</template>

<style scoped></style>
