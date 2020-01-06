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
import axios from 'axios';
import config from 'config';
import CreateEditProfileForm from './CreateEditProfileForm.vue';

const { baseUrl } = config.api;

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
      profiles: [{ id: 0, name: 'First profile' }, { id: 1, name: 'Second profile' }],
      defaultProfile: [],
      currentProfileJobSettings: null,
      currentProfileId: null,
    };
  },

  created() {
    this.fetchProfiles();
  },

  methods: {
    async handleEditProfileIconClick(profile) {
      try {
        const jobSettings = await this.fetchProfileJobSettings(profile.id);
        this.currentProfileJobSettings = { Name: profile.name, Options: jobSettings.data };
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
          await this.deleteProfile(profile.id);
          await this.fetchProfiles();
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
        await this.editProfile(profileData);
        this.isEditProfileModalOpen = false;
        await this.fetchProfiles();
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async handleNewProfileFormSave(profile) {
      try {
        await this.addProfile({
          Bitrate: profile.Options.Bitrate,
          Framerate: profile.Options.Framerate,
          Codec: profile.Options.Codec,
        }, profile.Name);

        this.isNewProfileModalOpen = false;
        await this.fetchProfiles();
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async fetchProfiles() {
      try {
        const response = await axios.get(`${baseUrl}/api/getProfiles`);

        if (response) {
          this.profiles = response.data;
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch profiles list');
      }
    },

    async addProfile(jobOptions, name) {
      try {
        await axios.post(`${baseUrl}/api/profile/${name}`, jobOptions);
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async deleteProfile(id) {
      try {
        await axios.delete(`${baseUrl}/api/profile/${id}`);
      } catch (e) {
        throw new Error(`Can not delete profile ${id}`);
      }
    },

    async editProfile(profile) {
      try {
        await axios.post(`${baseUrl}/api/updateProfile`, profile);
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async fetchProfileJobSettings(id) {
      try {
        const response = await axios.get(`${baseUrl}/api/getProfileOptions/${id}`);
        if (response) {
          return response;
        }
        throw new Error('Resoponse is empty');
      } catch (e) {
        throw new Error('Can not fetch job settings');
      }
    },

    async getProfile(id) {
      try {
        const response = await axios.get(`${baseUrl}/api/getProfile/${id}`);
        if (response) {
          return response;
        }
        throw new Error('Response is empty');
      } catch (e) {
        throw new Error('Cannot fetch profile');
      }
    },
  },
};
</script>

<style>

</style>
