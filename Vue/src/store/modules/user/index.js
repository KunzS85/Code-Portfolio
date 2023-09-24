import axios from "axios";

const state = {
  uInfo: [],
};

const mutations = {
  addUser(state, payload) {
    state.uInfo.push(payload);
  },
  setUsers(state, payload) {
    const uInfoDO = [];
    for (const info in payload) {
      uInfoDO.push(payload[info])
    }
    state.uInfo = uInfoDO;
  },
};

const actions = {
  fetchUInfos(context) {
    const token = context.rootState.auth.token;

    axios
      .get(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/uInfo.json?auth=${token}`
      )
      .then((res) => {
        const uInfoDO = [];
        for (const info in res.data) {
          const uInfo = res.data[info]
          uInfo.uInfoId = info
          uInfoDO.push(uInfo);
        }
        context.commit("setUsers", uInfoDO);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  storeUser(context, payload) {
    const token = context.rootState.auth.token;
    const usId = context.rootState.auth.userId;
    const name = payload.name;
    const email = payload.email;

    axios
      .post(
        `https://vue-shop-backend-9f2af-default-rtdb.europe-west1.firebasedatabase.app/uInfo.json?auth=${token}`,
        {
          userId: usId,
          name: name,
          email: email,
        }
      )
      .then(() => {
        localStorage.setItem("name", name);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  setUserLocal(context) {
    const userId = context.getters.userId;
    const user = this.getters.getUserById(userId)
    localStorage.setItem("name", user.name);
  },
};

const getters = {
  getUserByMail: (state) => (email) =>
    state.uInfo.find((user) => user.email === email),
  getUserByName: (state) => (name) =>
    state.uInfo.find((user) => user.name === name),
  getUserById: (state) => (id) => state.uInfo.find((user) => user.userId === id),
};

const userModule = {
  state,
  mutations,
  actions,
  getters,
};

export default userModule;
