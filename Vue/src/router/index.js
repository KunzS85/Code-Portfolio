import { createRouter, createWebHistory } from "vue-router";
//import HomePage from "@/pages/HomePage.vue";
//import ShopPage from "@/pages/ShopPage.vue";
//import CreateProductPage from "@/pages/CreateProductPage.vue"
//import ReadProductPage from "@/pages/ReadProductPage.vue"
//import NotFoundPage from "@/pages/NotFoundPage.vue"

import routes from "./routes";
//import store from "../store";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...routes,
    {
      path: "/:pathMatch(.*)*",
      component: ()=>import(/*webpackChunkName: 'component-404'*/"@/pages/NotFoundPage.vue"),
      //redirect: "/"
    },
  ],
});

/*
router.beforeEach((to, from, next) => {
    if(to.meta.requiresAuth && !store.getters.isAuthenticated) {
        next("/");
    } else {
        next();
    }
});
*/

export default router;
