//import store from "../../store";

const wichtelRoutes = [
    {
        path: "/wichteln",
        name: "Wichteln",
        component: () =>
          import(/*webpackChunkName: 'component-wichtelhomepage'*/ "@/pages/WichtelHomePage.vue"),
      },
      {
        path: "/wichteln/event/:id",
        name: "WichtelEvent",
        component: () =>
          import(/*webpackChunkName: 'component-wichtelevent'*/ "@/pages/WichtelEventPage.vue"),
        props: true,
        meta: {
          requiresAuth: true,
        },
      },
]

export default wichtelRoutes;