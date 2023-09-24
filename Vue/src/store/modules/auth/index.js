import { FIREBASE_API_KEY } from "../../../config/firebase";
import axios from "axios";

let timer;

const state = {
  userId: null,
  token: null,
};

const mutations = {
  setUser(state, payload) {
    state.userId = payload.userId;
    state.token = payload.token;
  },
};

const actions = {
  auth(context, payload) {
    let url = "";
    if (payload.mode === "signIn") {
      url = `https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${FIREBASE_API_KEY} `;
    } else if (payload.mode === "signUp") {
      url = `https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${FIREBASE_API_KEY} `;
    } else {
      return;
    }

    const authDO = {
      email: payload.email,
      password: payload.password,
      returnSecureToken: true,
    };

    return axios
      .post(url, authDO)
      .then((res) => {
        const expiresIn = Number(res.data.expiresIn) * 1000;
        const expDate = new Date().getTime() + expiresIn;

        localStorage.setItem("token", res.data.idToken);
        localStorage.setItem("userId", res.data.localId);
        localStorage.setItem("expiresIn", expDate);

        timer = setTimeout(() => {
          context.dispatch("autoSignOut");
        }, expiresIn);

        context.commit("setUser", {
          userId: res.data.localId,
          token: res.data.idToken,
        });
      })
      .catch((error) => {
        const errorMessage = new Error(
          error.response.data.error.message || "UNKNOWN_ERROR"
        );
        throw errorMessage;
      });
  },
  signUp(context, payload) {
    const signUpDO = {
      ...payload,
      mode: "signUp",
    };
    return context.dispatch("auth", signUpDO);
  },
  signIn(context, payload) {
    const signInDO = {
      ...payload,
      mode: "signIn",
    };
    return context.dispatch("auth", signInDO);
  },
  autoSignIn(context) {
    const token = localStorage.getItem("token");
    const userId = localStorage.getItem("userId");
    const expiresIn = localStorage.getItem("expiresIn");
    const timeLeft = Number(expiresIn) - new Date().getTime();

    if (timeLeft < 0) {
      return;
    }

    timer = setTimeout(() => {
      context.dispatch("autoSignOut");
    }, expiresIn);

    if (token && userId) {
      context.commit("setUser", {
        token: token,
        userId: userId,
      });
    }
  },
  signOut(context) {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("expiresIn");
    localStorage.removeItem("name");

    clearTimeout(timer);

    context.commit("setUser", {
      token: null,
      userId: null,
    });
  },
  autoSignOut(context) {
    context.dispatch("signOut");
  },
};

const getters = {
  isAuthenticated: (state) => !!state.token,
  token: (state) => state.token,
  userId: (state) => state.userId,
};

const authModule = {
  state,
  mutations,
  actions,
  getters,
};

export default authModule;
