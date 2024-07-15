/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-26 15:32:37
 * @LastEditTime: 2024-07-15 08:44:52
 * @LastEditors: sky
 */
import { http } from "@/utils/http";
//  列表
export function listVideo(params) {
  return http.request({
    url: "/video",
    method: "get",
    params
  });
}

export function listHotVideo(params) {
  return http.request({
    url: "/video/hot",
    method: "get",
    params
  });
}

//  影视搜索
export function searchVideo(params) {
  return http.request({
    url: "/video/search",
    method: "get",
    params
  });
}

// 查看某个影视的所有集数
// export function listEpisodes(data) {
//   return http.request({
//     url: "/episodes/list",
//     method: "post",
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     data
//   });
// }

