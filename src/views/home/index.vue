<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-12-30 15:43:49
 * @LastEditors: sky
-->
<script setup name="Home"> 
import { ref, onMounted ,computed} from "vue";
import { listHotVideo } from "@/api/video";
import { useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';


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


function toDetails(tv) {
  // 将详情数据写入store
  const tvStore = useTvStoreHook();
  tvStore.setTvDetails(tv);
  router.push({ name: 'Details' });

}

onMounted(() => {
  initData();
});

const groupedTvKeys = computed(() => Object.keys(tvObj.value));

</script>

<template>
  <div>
    <div v-for="label in groupedTvKeys" :key="label">
      <van-divider :style="{ color: '#1989fa', borderColor: '#1989fa', padding: '0 16px', fontSize: '35px' }">
        {{ label }}
      </van-divider>
      <van-list>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <div class="relative" v-for="item in tvObj[label]" :key="item.id" @click="toDetails(item)">
            <van-image :src="item.vod_pic_url" class="w-full h-auto" alt="视频缩略图" />
            <div
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
              {{ item.vod_title }}
            </div>
          </div>
        </div>
      </van-list>
    </div>
  </div>
</template>