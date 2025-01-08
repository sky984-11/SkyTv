/*
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-03 10:37:34
 * @LastEditTime: 2025-01-08 15:28:49
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


export function getAnimes() {
    return http.request({
      url: "/Users/8739f7a384ed43388bb7f8b0a542c672/Items?SortBy=SortName&SortOrder=Ascending&IncludeItemTypes=Series&Recursive=true&Fields=PrimaryImageAspectRatio&ImageTypeLimit=1&EnableImageTypes=Primary%2CBackdrop%2CBanner%2CThumb&StartIndex=0&Limit=100&ParentId=0c41907140d802bb58430fed7e2cd79e",
      method: "get",
      headers: {
          'X-Emby-Token': '4758069e94594559b01ac47864981680',
        }
    });
}


export function searchAnimes(anime) {
  console.log(anime)
  return http.request({
    url: `/Items?userId=8739f7a384ed43388bb7f8b0a542c672&limit=100&recursive=true&searchTerm=${anime}&fields=PrimaryImageAspectRatio&fields=CanDelete&fields=MediaSourceCount&includeItemTypes=Series&imageTypeLimit=1&enableTotalRecordCount=false`,
    method: "get",
    headers: {
        'X-Emby-Token': '4758069e94594559b01ac47864981680',
      }
  });
}




export function getAnimeDetails(itemId) {
    return http.request({
      url: "/Items/" + itemId + '?userId=8739f7a384ed43388bb7f8b0a542c672',
      method: "get",
      headers: {
          'X-Emby-Token': '4758069e94594559b01ac47864981680',
        }
    });
}

export function getAnimeEpisodes(itemId) {
    return http.request({
      url: "/Shows/" + itemId + '/Episodes?IsVirtualUnaired=false&IsMissing=false&UserId=8739f7a384ed43388bb7f8b0a542c672&Fields=Chapters%2CTrickplay',
      method: "get",
      headers: {
          'X-Emby-Token': '4758069e94594559b01ac47864981680',
        }
    });
}


export function playEpisodeInfo(episodeId) {
    return http.request({
      url: "/Items/" + episodeId + '/PlaybackInfo',
      method: "get",
      headers: {
          'X-Emby-Token': '4758069e94594559b01ac47864981680',
        }
    });
}