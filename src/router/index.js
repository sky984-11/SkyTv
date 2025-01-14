import { createRouter, createWebHashHistory } from "vue-router";
import routes from "./routes";
import { useCachedViewStoreHook } from "@/store/modules/cachedView";
import NProgress from "@/utils/progress";
import setPageTitle from "@/utils/set-page-title";
import { getToken } from "@/utils/auth";


const router = createRouter({
  history: createWebHashHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  NProgress.start();

  const token = getToken(); // 获取用户的 token
  const requiresAuth = to.meta.requiresAuth !== false; // 判断路由是否需要认证

  if (requiresAuth && !token) {
    // 避免在 /login 页面重复跳转
    if (to.path === "/login") {
      next(); // 直接放行到登录页
    } else {
      // 跳转到登录页，并保存目标路由以便登录后跳转回来
      next({ path: "/login", query: { redirect: to.fullPath } });
    }
  } else {
    // 设置页面标题
    setPageTitle(to.meta.title);
    next(); // 正常放行
  }
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
