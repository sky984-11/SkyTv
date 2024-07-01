<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-01 17:52:27
 * @LastEditors: sky
-->
<template>
  <van-tabbar v-model="active" :placeholder="true" :route="true" fixed>
    <van-tabbar-item
      v-for="(item, index) in tabbarData"
      :key="index"
      :icon="item.icon"
      :to="item.to"
    >
      {{ item.title }}
    </van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { ref, reactive } from "vue";

const active = ref(0);
const tabbarData = reactive([
  {
    icon: "wap-home-o",
    title: "主页",
    to: {
      name: "Home"
    }
  },
  {
    icon: "gem-o",
    title: "分类",
    to: {
      name: "Group"
    }
  },
  {
    icon: "user-o",
    title: "我的",
    to: {
      name: "About"
    }
  }
]);
</script>
