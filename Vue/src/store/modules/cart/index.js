const state = {
    cartItems: [],

};

const mutations = {
    addCartItem(state, payload){
        state.cartItems.push(payload)
    },
}

// context = {commit, dispatch, state, rootState, getters, rootGetters} 
const actions = {
    addItemToCart({commit}, payload){
        commit("addCartItem", {
            productId: payload.productId,
        });
    }
}

const getters = {
    cartItems: (state) => state.cartItems,
    // (state, getters, rootState, rootGetters)
    cartTotal: (_, getters, __, rootGetters) => {
        const cartItems = getters.cartItems;
        return cartItems.reduce((sum, cartItem) => {
            const product = rootGetters.product(cartItem.productId);
            return sum + product.price;
        }, 0)
    }
}

const cartModule = {
    state,
    mutations,
    actions,
    getters,
}

export default cartModule;