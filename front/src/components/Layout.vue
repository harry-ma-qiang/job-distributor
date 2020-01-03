/* eslint-disable import/no-unresolved */
/* eslint-disable import/extensions */
/* eslint-disable no-param-reassign */
<template>
  <v-card>
    <v-toolbar
      color="cyan"
      dark
      flat
    >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title>VOD Transcoding system</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

      <template v-slot:extension>
        <v-tabs
          v-model="currentTab"
          centered
          slider-color="yellow"
          background-color="transparent"
        >
          <v-tab
            v-for="tabItem in tabItems"
            :key="tabItem.index"
          >
            {{ tabItem.name }}
          </v-tab>
        </v-tabs>
      </template>
    </v-toolbar>
    <v-tabs-items v-model="currentTab">
      <v-tab-item>
        <JobComponent />
      </v-tab-item>

      <v-tab-item>
        <ProfileComponent />
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>
<script>
import {
  VToolbar, VToolbarTitle, VSpacer, VBtn, VIcon,
  VCard, VAppBarNavIcon, VTabs, VTab, VTabsItems, VTabItem,
} from 'vuetify/lib';
import JobComponent from './job-components/JobComponent.vue';
import ProfileComponent from './profile-components/ProfileComponent.vue';

export default {
  name: 'Layout',
  components: {
    JobComponent,
    VToolbar,
    VToolbarTitle,
    VSpacer,
    VBtn,
    VIcon,
    VCard,
    VAppBarNavIcon,
    VTabs,
    VTab,
    VTabsItems,
    VTabItem,
    ProfileComponent,
  },

  data: () => ({
    currentTab: 0,
    tabItems: [
      { index: 0, name: 'Job Queue' },
      { index: 1, name: 'Profiles' },
    ],
  }),

  methods: {

  },
};
</script>

<style>

</style>
