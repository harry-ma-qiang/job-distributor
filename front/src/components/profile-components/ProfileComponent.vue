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
                  title="Edit Profile"
                  :default-profile="currentProfileJobOptions"
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
import { mapState, mapGetters } from 'vuex';
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

  computed: {
    ...mapState([
      'profiles',
      'profileJobOptions',
    ]),

    ...mapGetters([
      'getDefaultProfile',
    ]),
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
      currentProfileJobOptions: null,
      currentProfileId: null,
      profileInterval: null,
    };
  },

  created() {
    this.$store.dispatch('loadProfiles').then(() => {
      const defaultProfile = this.getDefaultProfile;
      if (defaultProfile !== 'undefined' && defaultProfile) {
        this.defaultProfile = [defaultProfile.id];
      }
    });

    this.jobInterval = setInterval(() => {
      this.$store.dispatch('loadProfiles');
    }, 10000);
  },

  methods: {
    async handleEditProfileIconClick(profile) {
      try {
        await this.$store.dispatch('fetchProfileJobOptions', profile.id);
        this.currentProfileJobOptions = { Name: profile.name, Options: this.profileJobOptions };
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
          Options: profile.Options,
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
          Options: profile.Options,
          Name: profile.Name,
        });

        this.isNewProfileModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    handleDefaultProfileCheckBoxChange() {
      this.$store.dispatch('setDefaultProfileId', this.defaultProfile[0]);
    },
  },
};
</script>

<style>

</style>
