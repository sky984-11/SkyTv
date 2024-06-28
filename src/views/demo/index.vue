<script setup name="Demo">
import { reactive,watch ,ref} from "vue";
import { listTv } from "@/api/tv";

// import Player from "../player/index.vue";

// const m3u8Link = ref('https://172.80.104.90:11300/vods/hls/dhz/14/13322/2404219/634050/1920/index.m3u8?appId=kkdy&sign=a61258a22cfafc7d9eefadd6d273c49d&timestamp=1719292263')




const tvList = ref([])


// const isSearch = ref(false) // 是否处于搜索模式,搜索模式下显示搜索出来的内容

// watch(searchKey, (newValue) => {
// 	if (newValue == "") {
//     isSearch.value = false
// 	}
// })

function initData(){
  // const params = {}
  // listTv(params).then((res) => {
  //     tvList.value = res
  //     console.log(res)
  //   })
}

initData()
</script>

<template>
  


</template>
