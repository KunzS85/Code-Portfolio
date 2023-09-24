//import store from "../../store";

const appRoutes = [
  {
    path: "/",
    alias: "/home",
    component: () =>
      import(/*webpackChunkName: 'component-homepage'*/ "@/pages/HomePage.vue"),
  },
  {
    path: "/auth/:name",
    name: "Auth",
    component: () =>
      import(/*webpackChunkName: 'component-auth'*/ "@/pages/AuthPage.vue"),
  },
  {
    path: "/kanban",
    component: () =>
      import(/*webpackChunkName: 'component-auth'*/ "@/pages/KanbanPage.vue"),
  },
];

export default appRoutes;
