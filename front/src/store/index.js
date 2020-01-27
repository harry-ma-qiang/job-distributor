import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import config from 'config';
import VueAxios from 'vue-axios';

const { baseUrl } = config.api;

Vue.use(Vuex);
Vue.use(VueAxios, axios);

export default new Vuex.Store({
  state: {
    jobs: [],
    jobSettings: null,

    profiles: [],
    profileJobSettings: null,

    settings: [],
  },

  getters: {
    getProfileById: state => id => state.profiles.find(profile => profile.id === id),
    getOptionalSettings: state => state.settings.filter(s => s.is_optional),
    getNoneOptionalSettings: state => state.settings.filter(s => !s.is_optional),
  },

  mutations: {
    SET_JOBS(state, jobs) {
      state.jobs = jobs;
    },

    SET_JOB_SETTINGS(state, jobSettings) {
      state.jobSettings = jobSettings;
    },

    DELETE_JOB(state, id) {
      const index = state.jobs.findIndex(job => job.id === id);
      state.jobs.splice(index, 1);
    },

    SET_PROFILES(state, profiles) {
      state.profiles = profiles;
    },

    DELETE_PROFILE(state, id) {
      const index = state.profiles.findIndex(profile => profile.id === id);
      state.profiles.splice(index, 1);
    },

    SET_PROFILE_JOB_SETTINGS(state, profileJobSettings) {
      state.profileJobSettings = profileJobSettings;
    },

    SET_SETTINGS(state, settings) {
      state.settings = settings;
    },
  },

  actions: {
    // work with job Start
    async loadJobs() {
      try {
        const response = await axios.get(`${baseUrl}/api/getJobs`);

        if (response) {
          this.commit('SET_JOBS', response.data);
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch jobs list');
      }
    },

    async fetchJobSettings({ commit }, id) {
      try {
        const response = await axios.get(`${baseUrl}/api/getOptions/${id}`);
        if (response) {
          commit('SET_JOB_SETTINGS', response.data);
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch job settings');
      }
    },

    async deleteJob({ commit }, id) {
      try {
        await axios.delete(`${baseUrl}/api/job/${id}`);
        commit('DELETE_JOB', id);
      } catch (e) {
        throw new Error(`Can not delete job ${id}`);
      }
    },

    async editJob({ dispatch }, payload) {
      try {
        await axios.post(`${baseUrl}/api/updateJob/${payload.id}`, payload.data);
        dispatch('loadJobs');
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async addJob({ dispatch }, job) {
      try {
        await axios.post(`${baseUrl}/api/job`, job);
        dispatch('loadJobs');
      } catch (e) {
        throw new Error(e.message);
      }
    },
    // work with job End

    // work with profile Start
    async loadProfiles() {
      try {
        const response = await axios.get(`${baseUrl}/api/getProfiles`);

        if (response) {
          this.commit('SET_PROFILES', response.data);
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch profiles list');
      }
    },

    async deleteProfile({ commit }, id) {
      try {
        await axios.delete(`${baseUrl}/api/profile/${id}`);
        commit('DELETE_PROFILE', id);
      } catch (e) {
        throw new Error(`Can not delete profile ${id}`);
      }
    },

    async addProfile({ dispatch }, profile) {
      try {
        await axios.post(`${baseUrl}/api/profile/${profile.Name}`, profile.Options);
        dispatch('loadProfiles');
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async fetchProfileJobSettings({ commit }, id) {
      try {
        const response = await axios.get(`${baseUrl}/api/getProfileOptions/${id}`);
        if (response) {
          commit('SET_PROFILE_JOB_SETTINGS', response.data);
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch job settings');
      }
    },

    async editProfile({ dispatch }, profile) {
      try {
        await axios.post(`${baseUrl}/api/updateProfile`, profile);
        dispatch('loadProfiles');
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async loadSettings() {
      try {
        const response = await axios.get(`${baseUrl}/api/getOptions`);

        if (response) {
          this.commit('SET_SETTINGS', response.data);
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch options list');
      }
    },
  },
});
