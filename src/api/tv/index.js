import { http } from "@/utils/http";
//  影视列表
export function listTv(params) {
  return http.request({
    url: "/tv/list",
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

