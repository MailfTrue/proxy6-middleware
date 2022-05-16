import Vue from 'vue'
import Vuex from 'vuex'

import {auth} from "./auth.module"
import {proxy} from "./proxy.module"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    auth,
    proxy
  }
})
