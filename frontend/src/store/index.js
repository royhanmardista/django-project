import Vue from "vue";
import Vuex from "vuex";
import server from "@/api/server.js";
import router from "@/router";

Vue.use(Vuex);

function initialState() {
  return {
    isLoading: false,
    isLogin: false,
    loggedUser: {},
    locations: [{
      text: "Select Country",
      value: null
    }],
    isSearchingUser: false,
    userProfile: null,
    gettingAllUsers: false,
    allusers: [],
    gettingUserProfile: false,
    gettingCountry: false,
    countries: [],
    uploadingDate: false,
  };
}

export default new Vuex.Store({
  state: initialState(),
  mutations: {
    RESET(state) {
      const s = initialState();
      Object.keys(s).forEach(key => {
        if (key != 'allusers') {
          state[key] = s[key];
        }
      });
    },
    SET_ISLOGIN(state, payload) {
      state.isLogin = payload;
    },
    SET_LOGGED_USER(state, user) {
      state.loggedUser = user;
    },
    SET_ISLOADING(state, payload) {
      state.isLoading = payload;
    },
    SET_USER_PROFILE(state, data) {
      state.userProfile = data;
    },
    SET_SEARCHING_USER(state, payload) {
      state.isSearchingUser = payload;
    },
    SET_GETTING_ALLUSERS(state, payload) {
      state.gettingAllUsers = payload
    },
    SET_ALLUSERS(state, payload) {
      state.allusers = payload
    },
    SET_GETTING_USERPROFILE(state, payload) {
      state.gettingUserProfile = payload
    },
    SET_GETTING_COUNTRY(state, payload) {
      state.gettingCountry = payload
    },
    SET_COUNTRIES(state, payload) {
      state.countries = payload
    },
    SET_UPLOADING_DATA(state, payload) {
      state.uploadingDate = true
    }
  },
  actions: {
    async createProfile({
      commit
    }, form) {
      commit("SET_UPLOADING_DATA", true)
      try {
        let {
          data
        } = await server.post('/profiles', form , {
          headers: {
            Authorization: 'jwt ' + localStorage.getItem('token')
          }
        })
        commit('SET_USER_PROFILE', data)
        this._vm.$alertify.success(data.message);
        router.push(`/profiles/${data.profile.user}`)
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit("SET_UPLOADING_DATA", false)

      }
    },
    async deleteProfile({
      commit
    }, userId) {
      commit('SET_ISLOADING', true)
      try {
        let {
          data
        } = await server.delete(`/profiles/${userId}`, {
          headers: {
            Authorization: 'jwt ' + localStorage.getItem('token')
          }
        })
        this._vm.$alertify.success(data.message);
        router.push('/')
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit('SET_ISLOADING', false)
      }
    },
    async updateProfile({
      commit
    }, payload) {
      let {
        form,
        userId
      } = payload
      try {
        commit('SET_UPLOADING_DATA', true)
        let {
          data
        } = await server.put(`/profiles/${userId}`, form, {
          headers: {
            Authorization: 'jwt ' + localStorage.getItem('token')
          }
        })
        commit('SET_USER_PROFILE', data)
        router.push(`/profiles/${userId}`)
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit('SET_UPLOADING_DATA', false)
      }
    },
    async getCountry({
      commit
    }) {
      commit('SET_GETTING_COUNTRY', true)
      try {
        let {
          data
        } = await server.get('/countries')
        commit('SET_COUNTRIES', data.countries)
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit('SET_GETTING_COUNTRY', false)
      }
    },
    async getUserProfile({
      commit
    }, pk) {
      commit('SET_GETTING_USERPROFILE', true)
      try {
        let {
          data
        } = await server.get(`profiles/${pk}`, {
          headers: {
            Authorization: 'jwt ' + localStorage.getItem('token')
          }
        })
        commit('SET_USER_PROFILE', data)
      } catch (err) {
        commit('SET_USER_PROFILE', null)
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit('SET_GETTING_USERPROFILE', false)
      }
    },
    async getAllUsers({
      commit,
    }) {
      commit("SET_GETTING_ALLUSERS", true)
      try {
        let {
          data
        } = await server.get('/users')
        commit('SET_ALLUSERS', data.users)
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
      } finally {
        commit("SET_GETTING_ALLUSERS", false)
      }
    },
    async findUser({
      commit
    }) {
      commit('SET_SEARCHING_USER', true)
      try {
        let {
          data
        } = await server('/user', {
          headers: {
            Authorization: 'jwt ' + localStorage.getItem('token')
          }
        })
        commit('SET_LOGGED_USER', data.user)
        commit('SET_ISLOGIN', true)
      } catch (err) {
        let messages = [];
        for (let index in err.response.data) {
          messages.push(err.response.data[index]);
        }
        this._vm.$alertify.error(messages.join(', '));
        commit('SET_ISLOGIN', false)
      } finally {
        commit('SET_SEARCHING_USER', false)
      }
    }    
  },
  modules: {}
});