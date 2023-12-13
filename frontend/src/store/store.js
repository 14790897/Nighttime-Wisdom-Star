import { createStore } from "vuex";

export default createStore({
  state: {
    csrfToken: "",
    username: localStorage.getItem("username") || "",
  },
  mutations: {
    updateCsrfToken(state, csrfToken) {
      state.csrfToken = csrfToken;
    },
    setUsername(state, username) {
      state.username = username;
      localStorage.setItem("username", username);
    },
  },
  getters: {
    getUsername(state) {
      return state.username;
    },
  },
  actions: {},
  modules: {},
});
