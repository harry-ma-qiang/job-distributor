import Vue from 'vue';
import VuetifyConfirm from 'vuetify-confirm';
import Vuetify from 'vuetify/lib';
import VueRouter from 'vue-router';
import LoginSignup from './components/LoginSignup.vue';
import Layout from './components/layout/Layout.vue';
import App from './App.vue';
// eslint-disable-next-line import/no-unresolved
import store from './store';

const vuetify = new Vuetify();
Vue.use(VuetifyConfirm, {
  vuetify,
  color: 'warning',
  title: 'Warning',
  width: 350,
  property: '$confirm',
});
Vue.use(Vuetify);
Vue.use(VueRouter);

const routes = [
  { path: '/', component: Layout },
  { path: '/login-signup', component: LoginSignup },
];

const router = new VueRouter({
  routes,
});

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  render: h => h(App),
  vuetify: new Vuetify(),
}).$mount('#app');
