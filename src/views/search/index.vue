<!--
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 14:32:44
 * @LastEditTime: 2024-06-28 21:09:50
 * @LastEditors: sky
-->
<script setup name="Group">
import { reactive, ref, onMounted } from "vue";
import { searchTv } from "@/api/tv";
import { useRouter } from 'vue-router';
import { useTvStoreHook } from '@/store/modules/tvStore';

const tvList = ref([])   // 视频列表数据
const loading = ref(false);  //下拉加载
const finished = ref(false); //是否加载完成
const page = ref(1); // 当前页
const perPage = ref(20); // 每页数量
const router = useRouter();

async function fetchData() {
    try {
        loading.value = true;
        const params = {
            keyword: page.value,
        };


        var res = await searchTv(params);

        // console.log(res)
        if (res.length < perPage.value) {
            finished.value = true;
        }
        tvList.value = [...tvList.value, ...res];
        page.value += 1;
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false;
    }
}

function initData() {
    page.value = 1;
    tvList.value = [];
    finished.value = false;
    fetchData();
}

function onLoadData() {
    if (!finished.value) {
        fetchData();
    }
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
</script>

<template>
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoadData"
        error-text="请求失败，点击重新加载">
        <div class="flex flex-wrap gap-4">
            <div class="relative w-[calc(50%-8px)]" v-for="item in tvList" :key="item.id" @click="toDetails(item)">
                <van-image :src="item.image" class="w-full h-auto" alt="视频缩略图" />
                <div
                    class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full text-center bg-black bg-opacity-50 text-white py-1 box-border overflow-hidden text-ellipsis whitespace-nowrap">
                    {{ item.title }}
                </div>
            </div>
        </div>
    </van-list>
</template>
