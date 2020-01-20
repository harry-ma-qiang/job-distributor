<template>
    <v-navigation-drawer
      :mini-variant="isMenuOpen"
      app
      clipped
      permanent
    >
      <template v-slot:prepend>
        <v-list>
          <v-list-item>
            <v-list-item-avatar>
              <v-img src="https://randomuser.me/api/portraits/women/85.jpg"></v-img>
            </v-list-item-avatar>
          </v-list-item>
          <v-list-item
            link
            two-line
          >
            <v-list-item-content>
              <v-list-item-title class="title">Sandra Adams</v-list-item-title>
              <v-list-item-subtitle>sandra_a88@gmail.com</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon>mdi-menu-down</v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </template>

      <v-divider></v-divider>

      <v-list
        nav
        dense
      >
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-information</v-icon>
          </v-list-item-icon>
          <v-list-item-title>User Information</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-settings</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-login</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Log in</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
</template>
<script>
import {
  VNavigationDrawer, VList, VListItem, VListItemAvatar,
  VImg, VListItemContent, VListItemTitle, VListItemSubtitle,
  VListItemAction, VDivider, VListItemIcon, VIcon,
} from 'vuetify/lib';

export default {
  name: 'Layout',
  components: {
    VNavigationDrawer,
    VList,
    VListItem,
    VListItemAvatar,
    VImg,
    VListItemContent,
    VListItemTitle,
    VListItemSubtitle,
    VListItemAction,
    VDivider,
    VListItemIcon,
    VIcon,
  },

  props: {
    isMenuOpen: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
  },
};
</script>

<style>

</style>
