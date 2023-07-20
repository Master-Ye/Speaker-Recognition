import { createRouter, createWebHistory } from "vue-router";
import index from "~/pages/index.vue";
import Login from "~/pages/login.vue";
import NotFound from "~/pages/404.vue";
import Admin from "~/layouts/admin.vue";
import { createWebHashHistory } from "vue-router";
import compare from "~/pages/compare.vue";
import enhance from "~/pages/enhance.vue";
import denoise from "~/pages/denoise.vue";
import search from "~/pages/search.vue";
import add from  "~/pages/add.vue"
import user from "~/pages/user.vue"
const routes = [
  {
    path: "/",
    component: Admin,
    name: "admin",
    children: [
      {
        path: "/",
        component: index,
        meta: {
          title: "首页",
        },
      },
      {
        path: "/compare",
        component: compare,
        meta: {
          title: "对比",
        },
      },
      {
        path: "/enhance",
        component: enhance,
        meta: {
          title: "增强",
        },
      },
      {
        path: "/denoise",
        component: denoise,
        meta: { title: "降噪" },

      },
      {
        path:"/search",
component:search,
meta:{title:"检索"}
      },
      {
        path:"/add",
component:add,
meta:{title:"添加"}
      },
{
        path:"/user/:id?",
component:user,
name:"user",
meta:{title:"用户画像"}
}
    ],
  },

  {
    path: "/login",
    component: Login,
    meta: {
      title: "登录界面",
    },
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
export default router;
