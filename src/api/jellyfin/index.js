/*
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-03 10:37:34
 * @LastEditTime: 2025-01-03 10:45:25
 * @LastEditors: sky
 */
import { http } from "@/utils/http";



//  系统活动日志
export function activityLog() {
  return http.request({
    url: "/System/ActivityLog/Entries",
    method: "get",
    headers: {
        'X-Emby-Token': '4758069e94594559b01ac47864981680',
      }
  });
}