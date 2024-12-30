/*
 * @Description: 
 * @Author: sky
 * @Date: 2024-06-24 09:34:10
 * @LastEditTime: 2024-07-25 17:56:54
 * @LastEditors: sky
 */
import { createApp } from "vue";
import { store } from "./store";
// normalize.css
import "normalize.css/normalize.css";
// 全局样式
import "./styles/index.less";
// tailwindcss
import "./styles/tailwind.css";
// svg icon
import "virtual:svg-icons-register";

import App from "./App.vue";
import router from "./router";

import { Search, Swipe, SwipeItem, Image as VanImage, List, Cell, CellGroup, Tab, Tabs,Dialog } from 'vant';

import Vue3TouchEvents from "vue3-touch-events"

const app = createApp(App);
app.use(Vue3TouchEvents);
app.use(store);
app.use(router);
app.use(Search);
app.use(Swipe);
app.use(SwipeItem);
app.use(VanImage);
app.use(List);
app.use(Cell);
app.use(CellGroup);
app.use(Tab);
app.use(Tabs);
app.use(Dialog);
app.mount("#app");
