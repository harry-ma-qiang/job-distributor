<template>
  <v-app>
    <div id="app">
      <Layout />
    </div>
  </v-app>
</template>

<script>
import {
  VApp,
} from 'vuetify/lib';
import Layout from './components/Layout.vue';

export default {
  name: 'app',
  components: {
    Layout,
    VApp,
  },
};
</script>

<style>

</style>
