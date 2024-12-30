/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-26 15:32:37
 * @LastEditTime: 2024-07-30 14:55:16
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

// 查看某个视频的所有集数
export function listEpisodes(video_id) {
  return http.request({
    url: "/video/details/" + video_id,
    method: "get",
  });
}


// 根据id获取iptv m3u8地址
export function getIptvM3u8(id) {
  return http.request({
    url: "/iptv/" + id,
    method: "get",
  });
}
