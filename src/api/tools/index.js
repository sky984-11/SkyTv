/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-26 15:32:37
 * @LastEditTime: 2024-07-25 16:47:26
 * @LastEditors: sky
 */
import { http } from "@/utils/http";
//  检查是否是最新版本
export function checkForUpdates(params) {
  return http.request({
    url: "/tools/check-for-updates",
    method: "get",
    params
  });
}
