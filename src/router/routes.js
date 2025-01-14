/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2025-01-14 17:45:57
 * @LastEditors: sky
 */
import Layout from "@/layout/index.vue";
import Home from "@/views/home/index.vue";

const routes = [
  {
    path: "/",
    name: "root",
    component: Layout,
    redirect: { name: "Home" },
    children: [
      {
        path: "home",
        name: "Home",
        component: Home,
        meta: {
          title: "主页",
          noCache: false,
          hideTabbar:false
        }
      },
      {
        path: "group",
        name: "Group",
        component: () => import("@/views/group/index.vue"),
        meta: {
          title: "分类",
          noCache: false,
          hideTabbar:false
        }
      },
      {
        path: "about",
        name: "About",
        component: () => import("@/views/about/index.vue"),
        meta: {
          title: "关于",
          noCache: true,
          hideTabbar:false
        }
      },
      {
        path: "search",
        name: "Search",
        component: () => import("@/views/search/index.vue"),
        meta: {
          title: "搜索",
          noCache: true,
          hideTabbar:false
        }
      },
      {
        path: "history",
        name: "History",
        component: () => import("@/views/history/index.vue"),
        meta: {
          title: "播放历史",
          noCache: true,
          hideTabbar:false
        }
      },
      {
        path: "details/:id",
        name: "Details",
        component: () => import("@/views/details/index.vue"),
        meta: {
          title: "详情",
          noCache: true,
          hideTabbar:false
        }
      },
      {
        path: '/login',
        name: 'login',
        component: () => import('@/views/auth/Login.vue'),
        meta: {
          title: "登陆",
          noCache: true,
          hideTabbar:true
        }
    },
    ]
  }
];

export default routes;
