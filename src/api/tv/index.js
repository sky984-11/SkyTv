/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-26 15:32:37
 * @LastEditTime: 2024-06-28 17:37:14
 * @LastEditors: sky
 */
import { http } from "@/utils/http";
//  影视列表
export function listTv(params) {
  return http.request({
    url: "/tv/list",
    method: "get",
    params
  });
}

//  影视搜索
export function searchTv(params) {
  return http.request({
    url: "/tv/search",
    method: "get",
    params
  });
}

// 查看某个影视的所有集数
export function listEpisodes(data) {
  return http.request({
    url: "/episodes/list",
    method: "post",
    headers: {
      'Content-Type': 'application/json'
    },
    data
  });
}

