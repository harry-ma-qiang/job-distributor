<template>
  <v-app id="inspire">
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title> {{ title }} </v-toolbar-title>

                <template v-slot:extension>
                  <v-tabs
                    v-model="currentTab"
                    centered
                    slider-color="yellow"
                    background-color="transparent"
                    @change = "handleTabChange"
                  >
                    <v-tab
                      v-for="tabItem in tabItems"
                      :key="tabItem.index"
                    >
                      {{ tabItem.name }}
                    </v-tab>
                  </v-tabs>
                </template>
                <v-spacer />
              </v-toolbar>

              <v-tabs-items v-model="currentTab">
                <v-tab-item>
                  <v-card-text>
                    <v-form>
                      <v-text-field
                        label="Login"
                        name="login"
                        prepend-icon="person"
                        type="text"
                      />

                      <v-text-field
                        id="password"
                        label="Password"
                        name="password"
                        prepend-icon="lock"
                        type="password"
                      />
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer />
                    <v-btn color="primary">Log in</v-btn>
                  </v-card-actions>
                </v-tab-item>

                <v-tab-item>
                  <v-card-text>
                    <v-form>
                      <v-text-field
                        label="Login"
                        name="login"
                        prepend-icon="person"
                        type="text"
                      />

                      <v-text-field
                        id="password2"
                        label="Password"
                        name="password"
                        prepend-icon="lock"
                        type="password"
                      />

                      <v-text-field
                        id="confirmPassword"
                        label="Confirm password"
                        name="confirmPassword"
                        prepend-icon="lock"
                        type="password"
                      />

                      <v-menu
                        v-model="datePickerMenu"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on }">
                          <v-text-field
                            v-model="date"
                            label="Date of Birth"
                            prepend-icon="event"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker v-model="date" @input="datePickerMenu = false">
                        </v-date-picker>
                      </v-menu>

                      <v-text-field
                        label="Email"
                        name="email"
                        prepend-icon="email"
                        type="text"
                      />

                      <v-file-input
                        label="Avatar"
                        accept="image/*"
                        prepend-icon="mdi-camera"
                      ></v-file-input>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer />
                    <v-btn color="primary">Sign up</v-btn>
                  </v-card-actions>
                </v-tab-item>
              </v-tabs-items>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import {
  VCard, VCardText, VContainer, VRow, VCol, VTextField,
  VCardActions, VSpacer, VBtn, VApp, VContent, VToolbar,
  VToolbarTitle, VForm, VTabs, VTab, VTabsItems, VTabItem,
  VMenu, VDatePicker, VFileInput,
} from 'vuetify/lib';

export default {
  name: 'LoginSignup',
  components: {
    VCard,
    VCardText,
    VContainer,
    VRow,
    VCol,
    VTextField,
    VCardActions,
    VSpacer,
    VBtn,
    VApp,
    VContent,
    VToolbar,
    VToolbarTitle,
    VForm,
    VTabs,
    VTab,
    VTabsItems,
    VTabItem,
    VMenu,
    VDatePicker,
    VFileInput,
  },

  props: {

  },

  data() {
    return {
      title: 'Log in',
      currentTab: 0,
      date: new Date().toISOString().substr(0, 10),
      datePickerMenu: false,
      tabItems: [
        { index: 0, name: 'Log in' },
        { index: 1, name: 'Sign up' },
      ],
    };
  },

  methods: {
    handleTabChange() {
      this.title = this.tabItems.find(tab => tab.index === this.currentTab).name;
    },
  },
};
</script>

<style>

</style>
