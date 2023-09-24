import { createStore } from "vuex";

import authModule from "./modules/auth";
import shopModule from "./modules/shop";
import cartModule from "./modules/cart";
import kanbanModule from "./modules/kanban";
import wichtelModule from "./modules/wichtel";
import userModule from "./modules/user"

const store = createStore({
  modules: {
    auth: authModule,
    shop: shopModule,
    cart: cartModule,
    kanban: kanbanModule,
    wichtel: wichtelModule,
    user: userModule,
  }
});

export default store;
