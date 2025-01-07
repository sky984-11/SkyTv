/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-07-23 17:20:19
 * @LastEditTime: 2025-01-07 08:44:46
 * @LastEditors: sky
 */
// cache.js
class LocalCache {
    constructor(prefix = '') {
      this.prefix = prefix;
    }
  
    setItem(key, value) {
      try {
        const serializedValue = JSON.stringify(value);
        localStorage.setItem(this.prefix + key, serializedValue);
      } catch (error) {
        console.error('Error setting item in local storage:', error);
      }
    }
  
    getItem(key) {
      try {
        const serializedValue = localStorage.getItem(this.prefix + key);
        if (serializedValue === null) {
          return null;
        }
        return JSON.parse(serializedValue);
      } catch (error) {
        console.error('Error getting item from local storage:', error);
        return null;
      }
    }
  
    removeItem(key) {
      localStorage.removeItem(this.prefix + key);
    }
  
    clear() {
      const keys = Object.keys(localStorage)
                        .filter(k => k.startsWith(this.prefix))
                        .forEach(k => localStorage.removeItem(k));
    }

    // 获取所有缓存数据
    getAllItems() {
          const allItems = [];
          Object.keys(localStorage).forEach(key => {
            if (key.startsWith(this.prefix)) {
              const value = this.getItem(key.replace(this.prefix, ''));
              allItems.push(value);
            }
          });
          return allItems;
    }
  }
  

  const cache = new LocalCache('SkyAnime-');
  export default cache;

// 使用示例
//   cache.setItem('user', { name: 'John Doe', age: 30 });
//   const user = cache.getItem('user');
//   console.log(user); // 输出: { name: 'John Doe', age: 30 }
  
//   cache.removeItem('user');
//   cache.clear();