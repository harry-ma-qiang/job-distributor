import Vue from 'vue';
import VuetifyConfirm from 'vuetify-confirm';
import Vuetify from 'vuetify/lib';
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

Vue.config.productionTip = false;

Vue.mixin({
  methods: {
    range(start, end) {
      return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
    },
  },
});

new Vue({
  store,
  render: h => h(App),
  vuetify: new Vuetify(),
}).$mount('#app');
