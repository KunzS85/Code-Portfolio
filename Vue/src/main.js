import { createApp } from 'vue'
import App from './App.vue'
import store from "./store/index"
import router from "./router/index"
import logger from "./mixins/logger";
import focus from "./directives/focus";

const app = createApp(App);
app.use(store);
app.use(router);
app.mixin(logger)
app.directive("focus", focus)
app.mount('#app');
