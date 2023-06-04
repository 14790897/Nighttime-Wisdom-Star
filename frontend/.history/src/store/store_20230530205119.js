import { createStore } from 'vuex';

export default createStore({
  state: {
    csrfToken: '',
    username: null,
  },
  mutations: {
    updateCsrfToken(state, csrfToken) {
      state.csrfToken = csrfToken;
    },
    setUsername(state, username) {
      state.username = username;
    },
  },
  actions: {},
  modules: {}
});
