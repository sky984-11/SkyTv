/*
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-03 10:37:34
 * @LastEditTime: 2025-01-15 15:47:57
 * @LastEditors: sky
 */
import { http } from "@/utils/http";

const token = '4758069e94594559b01ac47864981680'
const userId = '8739f7a384ed43388bb7f8b0a542c672'

//  系统活动日志
export function activityLog() {
  return http.request({
    url: "/System/ActivityLog/Entries",
    method: "get",
    headers: {
        'X-Emby-Token': token,
      }
  });
}

// 用户登陆并返回token
export function login(data) {
  return http.request({
    url: "/Users/AuthenticateByName",
    method: "post",
    headers: {
      "Content-Type": "application/json",
      },
      data
  });
}

// 获取动漫列表
export function getAnimes(startIndex,limit) {
    return http.request({
      url: `/Users/${userId}/Items?SortBy=SortName&SortOrder=Ascending&IncludeItemTypes=Series&Recursive=true&Fields=PrimaryImageAspectRatio&ImageTypeLimit=1&EnableImageTypes=Primary%2CBackdrop%2CBanner%2CThumb&StartIndex=${startIndex}&Limit=${limit}&ParentId=0c41907140d802bb58430fed7e2cd79e`,
      method: "get",
      headers: {
          'X-Emby-Token': token,
        }
    });
}

// 暂时去掉startIndex,limit控制
// 动漫搜索
export function searchAnimes(startIndex,limit,anime) {
  // console.log(startIndex,limit,anime)
  return http.request({
    url: `/Items?userId=${userId}&limit=100&recursive=true&searchTerm=${anime}&fields=PrimaryImageAspectRatio&fields=CanDelete&fields=MediaSourceCount&includeItemTypes=Series&imageTypeLimit=1&enableTotalRecordCount=false`,
    method: "get",
    headers: {
        'X-Emby-Token': token,
      }
  });
}



// 获取动漫详情
export function getAnimeDetails(itemId) {
    return http.request({
      url: "/Items/" + itemId + `?userId=${userId}`,
      method: "get",
      headers: {
          'X-Emby-Token': token,
        }
    });
}

// 获取动漫历史记录
export function getAnimeHistory() {
  return http.request({
    url: `Users/${userId}/Items/` + `?IncludeItemTypes=Episode&SortBy=DatePlayed&SortOrder=Descending`,
    method: "get",
    headers: {
        'X-Emby-Token': token,
      }
  });
}

export function getAnimeEpisodes(itemId) {
    return http.request({
      url: "/Shows/" + itemId + `/Episodes?IsVirtualUnaired=false&IsMissing=false&UserId=${userId}&Fields=Chapters%2CTrickplay`,
      method: "get",
      headers: {
          'X-Emby-Token': token,
        }
    });
}


export function playEpisodeInfo(episodeId) {
    return http.request({
      url: "/Items/" + episodeId + '/PlaybackInfo',
      method: "get",
      headers: {
          'X-Emby-Token': token,
        }
    });
}