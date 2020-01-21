<template>
    <v-card flat>
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="profiles"
          :search="search"
          :items-per-page="5"
          sort-by="name"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>Profiles</v-toolbar-title>
              <v-divider
                class="mx-4"
                inset
                vertical
              ></v-divider>
              <v-spacer></v-spacer>
              <v-btn color="primary" dark class="mb-2" @click="handleClickNewProfileButton">
                New Profile
              </v-btn>
              <v-dialog
                v-model="isNewProfileModalOpen"
                v-if="isNewProfileModalOpen"
                max-width="500px"
              >
                <CreateEditProfileForm
                  @close = "handleAddProfileFormClose"
                  @save = "handleNewProfileFormSave"
                />
              </v-dialog>
              <v-dialog
                v-model="isEditProfileModalOpen"
                v-if="isEditProfileModalOpen"
                max-width="500px">
                <CreateEditProfileForm
                  title="Edit job"
                  :default-profile="currentProfileJobSettings"
                  :profile-id="currentProfileId"
                  @close = "handleEditProfileFormClose"
                  @save = "handleEditProfileFormSave"
                />
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.default="{ item }">
            <v-checkbox
                :key="item.id"
                :value="item.id"
                v-model="defaultProfile"
                :disabled="defaultProfile.length > 0 && item.id != defaultProfile[0]"
                @change="handleDefaultProfileCheckBoxChange(item)"
            >
            </v-checkbox>
          </template>
          <template v-slot:item.action="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="handleEditProfileIconClick(item)"
            >
              edit
            </v-icon>
            <v-icon
              small
              @click="handleClickDeleteProfileButton(item)"
            >
              delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
</template>

<script>
import {
  VCard,
  VCardTitle,
  VTextField,
  VDataTable,
  VCardText,
  VIcon,
  VToolbar,
  VToolbarTitle,
  VDivider,
  VSpacer,
  VBtn,
  VCheckbox,
  VDialog,
} from 'vuetify/lib';
import { mapState } from 'vuex';
import CreateEditProfileForm from './CreateEditProfileForm.vue';

export default {
  name: 'ProfileComponent',
  components: {
    VCard,
    VCardTitle,
    VTextField,
    VDataTable,
    VCardText,
    VIcon,
    VToolbar,
    VToolbarTitle,
    VDivider,
    VDialog,
    VSpacer,
    VBtn,
    VCheckbox,
    CreateEditProfileForm,
  },

  data() {
    return {
      isNewProfileModalOpen: false,
      isEditProfileModalOpen: false,
      search: '',
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Default', value: 'default' },
        { text: 'Actions', value: 'action', sortable: false },
      ],
      defaultProfile: [],
      currentProfileJobSettings: null,
      currentProfileId: null,
      profileInterval: null,
    };
  },

  created() {
    const defaultProfileId = parseInt(window.localStorage.getItem('defaultProfileId'), 10);
    if (defaultProfileId !== 'undefined' && defaultProfileId) {
      this.defaultProfile = [defaultProfileId];
    }

    this.$store.dispatch('loadProfiles');

    this.jobInterval = setInterval(() => {
      this.$store.dispatch('loadProfiles');
    }, 10000);
  },

  computed: mapState([
    'profiles',
    'profileJobSettings',
  ]),

  methods: {
    async handleEditProfileIconClick(profile) {
      try {
        await this.$store.dispatch('fetchProfileJobSettings', profile.id);
        this.currentProfileJobSettings = { Name: profile.name, Options: this.profileJobSettings };
        this.currentProfileId = profile.id;
        this.isEditProfileModalOpen = true;
      // eslint-disable-next-line no-empty
      } catch (e) {

      }
    },

    async handleClickDeleteProfileButton(profile) {
      const res = await this.$confirm('Are you sure that you want to delete this profile?');

      if (res) {
        try {
          await this.$store.dispatch('deleteProfile', profile.id);
        // eslint-disable-next-line no-empty
        } catch (e) {
        }
      }
    },

    handleClickNewProfileButton() {
      this.isNewProfileModalOpen = true;
    },

    handleAddProfileFormClose() {
      this.isNewProfileModalOpen = false;
    },

    handleEditProfileFormClose() {
      this.isEditProfileModalOpen = false;
    },

    async handleEditProfileFormSave(profile, profileId) {
      try {
        const profileData = {
          Id: profileId,
          Name: profile.Name,
          Options: {
            Bitrate: profile.Options.Bitrate,
            Framerate: profile.Options.Framerate,
            Codec: profile.Options.Codec,
          },
        };
        await this.$store.dispatch('editProfile', profileData);
        this.isEditProfileModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async handleNewProfileFormSave(profile) {
      try {
        await this.$store.dispatch('addProfile', {
          Options: {
            Bitrate: profile.Options.Bitrate,
            Framerate: profile.Options.Framerate,
            Codec: profile.Options.Codec,
          },
          Name: profile.Name,
        });

        this.isNewProfileModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    handleDefaultProfileCheckBoxChange() {
      window.localStorage.setItem('defaultProfileId', this.defaultProfile[0]);
    },
  },
};
</script>

<style>

</style>
