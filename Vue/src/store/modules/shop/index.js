import axios from "axios";

const state = {
  products: [],
};

const mutations = {
  addProduct(state, payload) {
    state.products.push(payload);
  },
  setProducts(state, payload) {
    state.products = payload;
  },
};

const actions = {
  fetchProducts(context) {
    const token = context.rootState.auth.token;
    axios
      .get(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/products.json?auth=${token}`
      )
      .then((res) => {
        const productsDO = [];
        for (const id in res.data) {
          productsDO.push({
            id: id,
            ...res.data[id],
          });
        }
        context.commit("setProducts", productsDO);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  storeProduct(context, payload) {
    const productItem = {
      title: payload.title,
      description: payload.description,
      price: payload.price,
    };
    const token = context.rootState.auth.token;
    axios
      .post(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/products.json?auth=${token}`,
        productItem
      )
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        throw new Error(error);
      });
  },
};

const getters = {
  products: (state) => state.products,
  product: (state) => (id) => state.products.find((product) => product.id === id),
};

const shopModule = {
  state,
  mutations,
  actions,
  getters,
};
export default shopModule;
