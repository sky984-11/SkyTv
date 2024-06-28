import Layout from "@/layout/index.vue";
import Demo from "@/views/demo/index.vue";

const routes = [
  {
    path: "/",
    name: "root",
    component: Layout,
    redirect: { name: "Demo" },
    children: [
      {
        path: "demo",
        name: "Demo",
        component: Demo,
        meta: {
          title: "主页"
        }
      },
      {
        path: "group",
        name: "Group",
        component: () => import("@/views/group/index.vue"),
        meta: {
          title: "分类"
        }
      },
      {
        path: "about",
        name: "About",
        component: () => import("@/views/about/index.vue"),
        meta: {
          title: "关于",
          noCache: true
        }
      },
      {
        path: "search",
        name: "Search",
        component: () => import("@/views/search/index.vue"),
        meta: {
          title: "搜索",
          noCache: true
        }
      },
      {
        path: "details",
        name: "Details",
        component: () => import("@/views/details/index.vue"),
        meta: {
          title: "详情",
          noCache: true
        }
      },
    ]
  }
];

export default routes;
