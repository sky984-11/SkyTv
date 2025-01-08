<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2025-01-08 15:36:28
 * @LastEditors: sky
-->
<script setup name="Home"> 
import { ref, onMounted ,computed} from "vue";
import { listHotVideo } from "@/api/video";
import { useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';
import CardList from "@/components/public/CardList.vue"

const tvObj = ref({
    "热播剧集":  [], 
    "热播电影":  [],
    "热播动漫":  [],
  })

const loading = ref(false);  //下拉加载

const router = useRouter();

// 分组函数，提高可维护性
function groupTvByType(videoList) {
  return videoList.reduce((acc, item) => {
    if (!acc[item.vod_type]) {
      acc[item.vod_type] = [];
    }
    acc[item.vod_type].push(item);
    return acc;
  }, {});
}

// 优化后的fetchData，包含异常处理和数据校验
async function fetchData() {
  try {
    const res = await listHotVideo();
    if (!Array.isArray(res)) {
      throw new Error("API返回的数据不是一个数组");
    }
    const groupedByType = groupTvByType(res);
    // 检查是否有预期的3种类别
    if (groupedByType.length < 3) {
      throw new Error("API返回的类型数组长度不足");
    }
    // 更新数据对象
    tvObj.value["热播剧集"] = groupedByType['剧集']
    tvObj.value["热播电影"] = groupedByType['电影']
    tvObj.value["热播动漫"] = groupedByType['动漫']
  } catch (error) {
    console.error("数据获取失败:", error);
    // 可以在这里添加用户友好的错误提示
  } finally {
    loading.value = false;
  }
}



function initData() {
  fetchData();
}



onMounted(() => {
  // initData();
});

const groupedTvKeys = computed(() => Object.keys(tvObj.value));

</script>

<template>
  <div>
    <div v-for="label in groupedTvKeys" :key="label">
      <van-divider :style="{ color: '#1989fa', borderColor: '#1989fa', padding: '0 16px', fontSize: '35px' }">
        {{ label }}
      </van-divider>

      <!-- <card-list :animes="tvObj[label]" :loading="loading"></card-list> -->
    </div>
  </div>
</template>