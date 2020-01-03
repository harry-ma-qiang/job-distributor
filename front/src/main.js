import Vue from 'vue';
import VuetifyConfirm from 'vuetify-confirm';
import Vuetify from 'vuetify/lib';
import App from './App.vue';

const vuetify = new Vuetify();
Vue.use(VuetifyConfirm, {
  vuetify,
  color: 'warning',
  title: 'Warning',
  width: 350,
  property: '$confirm',
});
Vue.use(Vuetify);

Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
  vuetify: new Vuetify(),
}).$mount('#app');
