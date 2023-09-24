import store from "../../store";

const shopRoutes = [
  {
    path: "/shophome",
    component: () =>
      import(
        /*webpackChunkName: 'component-homepage'*/ "@/pages/ShopHomePage.vue"
      ),
    beforeEnter: (to, from, next) => {
      if (store.getters.isAuthenticated) {
        next("/shop");
      } else {
        next();
      }
    },
  },
  {
    path: "/shop",
    component: () =>
      import(/*webpackChunkName: 'group-shop'*/ "@/pages/ShopPage.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/shop/create/product",
    component: () =>
      import(
        /*webpackChunkName: 'component-createProduct'*/ "@/pages/CreateProductPage.vue"
      ),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/shop/read/product/:id",
    name: "ReadProduct",
    component: () =>
      import(/*webpackChunkName: 'group-shop'*/ "@/pages/ReadProductPage.vue"),
    props: true,
    meta: {
      requiresAuth: true,
      // enterTransition: "rubberBand", // so erhält die Route dynamisch eine Transition
    },
  },
];

export default shopRoutes;
