/*
 * @Description: 
 * @Author: sky
 * @Date: 2025-01-14 16:07:01
 * @LastEditTime: 2025-01-15 14:09:11
 * @LastEditors: sky
 */
// auth.js

/**
 * 从本地存储或 Cookie 中获取用户 token
 * @returns {string|null} 用户的 token，如果不存在则返回 null
 */
export function getToken() {
    // 优先从 localStorage 获取 token
    const token = localStorage.getItem("token");
  
    // 如果 localStorage 没有 token，可改为从其他存储中获取（例如 Cookies）
    if (!token) {
      const cookieToken = getCookie("token");
      return cookieToken || null;
    }
  
    return token;
  }

  /**
 * 设置用户 token 到本地存储和 Cookie
 * @param {string} token 用户的 token
 * @param {number} [expiresInDays=7] token 的有效期（天），默认 7 天
 */
export function setToken(token, expiresInDays = 7) {
  // 设置到 localStorage
  localStorage.setItem("token", token);

  // 设置到 Cookie
  const expires = new Date();
  expires.setDate(expires.getDate() + expiresInDays);
  document.cookie = `token=${encodeURIComponent(token)}; expires=${expires.toUTCString()}; path=/`;
}

  /**
   * 从 Cookie 中获取指定键的值
   * @param {string} key Cookie 的键名
   * @returns {string|null} Cookie 中的值，如果不存在则返回 null
   */
  function getCookie(key) {
    const cookieStr = document.cookie;
    const cookies = cookieStr ? cookieStr.split("; ") : [];
    for (const cookie of cookies) {
      const [cookieKey, cookieValue] = cookie.split("=");
      if (cookieKey === key) {
        return decodeURIComponent(cookieValue);
      }
    }
    return null;
  }
  