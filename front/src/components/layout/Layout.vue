<template>
  <v-app id="inspire">
    <LeftMenu :isMenuOpen="isMinUserMenu" />

    <v-app-bar
      app
      clipped-left
      color="cyan"
      dark
      flat
    >
      <v-app-bar-nav-icon @click="handleLeftMenuIconClick">
      </v-app-bar-nav-icon>

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
    </v-app-bar>
    <v-content>
      <v-tabs-items v-model="currentTab">
        <v-tab-item>
          <JobComponent />
        </v-tab-item>

        <v-tab-item>
          <ProfileComponent />
        </v-tab-item>
      </v-tabs-items>
    </v-content>
  </v-app>
</template>
<script>
import {
  VToolbarTitle, VSpacer, VBtn, VIcon, VAppBar, VContent,
  VApp, VAppBarNavIcon, VTabs, VTab, VTabsItems, VTabItem,
} from 'vuetify/lib';
import JobComponent from './content/job-components/JobComponent.vue';
import ProfileComponent from './content/profile-components/ProfileComponent.vue';
import LeftMenu from './LeftMenu.vue';

export default {
  name: 'Layout',
  components: {
    JobComponent,
    VToolbarTitle,
    VSpacer,
    VBtn,
    VIcon,
    VApp,
    VAppBarNavIcon,
    VTabs,
    VTab,
    VTabsItems,
    VTabItem,
    ProfileComponent,
    VAppBar,
    LeftMenu,
    VContent,
  },

  data: () => ({
    currentTab: 0,
    tabItems: [
      { index: 0, name: 'Job Queue' },
      { index: 1, name: 'Profiles' },
    ],
    isMinUserMenu: true,
  }),

  methods: {
    handleLeftMenuIconClick() {
      this.isMinUserMenu = !this.isMinUserMenu;
    },
  },
};
</script>

<style>

</style>
