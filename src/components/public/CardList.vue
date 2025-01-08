<template>
    <van-list v-model:loading="loading" :finished="!loading" finished-text="没有更多了" error-text="请求失败，点击重新加载" @load="onLoadData">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        <div
          class="relative"
          v-for="item in animes"
          :key="item.Id"
          @click="toDetails(item)"
        >
          <van-image
            :src="loadImage(item.Id)"
            class="w-full h-auto"
            alt="视频缩略图"
          />
          <div
            class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap"
          >
            {{ item.Name }}
          </div>
        </div>
      </div>
    </van-list>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { useTvStoreHook } from '@/store/modules/tvStore';

  const emit = defineEmits(['onLoadData']);


  // 获取 router 和 tvStore 实例
  const router = useRouter();
  const tvStore = useTvStoreHook();
  
  // props 接收传递的参数
  const props = defineProps({
    animes: {
      type: Array,  // 更改为 Array 类型
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  });
  
  // 使用 computed 获取当前的 loading 状态
  const { loading } = props;
  
  // 拼接图片 URL
  function loadImage(id) {
    return `${import.meta.env.VITE_BASE_API}/Items/${id}/Images/Primary`;
  }
  
  // 跳转到详情页面，并存储当前 TV 信息
  function toDetails(tv) {
    tvStore.setTvDetails(tv);
    router.push({ name: 'Details', params: { id: tv.Id } });
  }

  function onLoadData(){
    emit('onLoadData')
  }
  </script>
  
  <style scoped>
  /* 如果有其他样式需求可以放在这里 */
  </style>
  