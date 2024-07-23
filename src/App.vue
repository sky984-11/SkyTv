<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-23 16:04:28
 * @LastEditors: sky
-->
<template>
  <router-view v-touch:swipe.left="SwipeLeft('left')" v-touch:swipe.right="SwipeRight('right')" />
</template>

<script setup name="App">

import { useRouter } from 'vue-router';
const router = useRouter();


function SwipeLeft(action){
  console.log(action)
}
function SwipeRight(action){
  console.log(action)
  router.go(-1);
}

</script>
