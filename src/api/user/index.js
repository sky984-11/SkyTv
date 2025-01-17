/*
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-15 15:49:52
 * @LastEditTime: 2025-01-15 15:50:36
 * @LastEditors: sky
 */
import { Http } from "@/utils/http";

// 实例
const userHttp = new Http({ baseURL: 'http://127.0.0.1:5000' });


export function login(data) {
    return userHttp.request({
      url: "/api/v1/user/login",
      method: "post",
        data
    });
  }