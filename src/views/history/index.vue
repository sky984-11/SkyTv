<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2025-01-14 13:56:02
 * @LastEditors: sky
-->

<!-- 后续增加分类过滤后去掉注释(根据评分，标签，年代)，增加后端分页 -->
<template>
  <card-list :fetchFunction="getAnimeHistory"></card-list>
</template>


<script setup name="Group">
import { getAnimeHistory } from "@/api/jellyfin";

import CardList from "@/components/public/CardList.vue"


</script>
