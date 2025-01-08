<template>
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" error-text="请求失败，点击重新加载"
        @load="onLoadData">
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            <div class="relative" v-for="item in animes" :key="item.Id" @click="toDetails(item)">
                <van-image :src="loadImage(item.Id)" class="w-full h-auto" alt="视频缩略图" />
                <div
                    class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
                    {{ item.Name }}
                </div>
            </div>
        </div>
    </van-list>
</template>

<script setup>
import { ref,onMounted} from "vue";
import { useRouter,useRoute } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';

const emit = defineEmits(['onLoadData']);


// 获取 router 和 tvStore 实例
const router = useRouter();
const route = useRoute();

const tvStore = useTvStoreHook();

const page = ref(1); // 当前页
const perPage = ref(10); // 每页数量

const loading = ref(false)
const finished = ref(false)
const animes= ref([])

// props 接收传递的参数
const props = defineProps({
    fetchFunction: {
        type: Function,
        required: true,
    }
});



async function initData(newKeyword) {
    try {
        loading.value = true;
        // 调用传入的动态函数获取数据
        const res = await props.fetchFunction(newKeyword);

        animes.value = [...animes.value, ...res.Items];
        finished.value = true

    } catch (error) {
        console.error("Error fetching data:", error);
        finished.value = true
    } finally {
        loading.value = false;
    }
}

// 拼接图片 URL
function loadImage(id) {
    return `${import.meta.env.VITE_BASE_API}/Items/${id}/Images/Primary`;
}

// 跳转到详情页面，并存储当前 TV 信息
function toDetails(tv) {
    tvStore.setTvDetails(tv);
    router.push({ name: 'Details', params: { id: tv.Id } });
}

function onLoadData() {
    emit('onLoadData')
}

// 添加初始加载逻辑
onMounted(() => {
  initData();
});

defineExpose({
    initData,
});
</script>

<style scoped>
/* 如果有其他样式需求可以放在这里 */
</style>