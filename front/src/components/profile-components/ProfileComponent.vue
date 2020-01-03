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
                  @close = "closeAddProfileForm"
                  @save = "handleNewProfileFormSave"
                />
              </v-dialog>
              <!-- <v-dialog
                v-model="isEditJobModalOpen"
                v-if="isEditJobModalOpen"
                max-width="500px">
                <CreateEditProfileForm
                  title="Edit job"
                  :default-job="currentJobSettings"
                  :job-id="currentJobId"
                  @close = "handleEditJobFormClose"
                  @save = "handleEditJobFormSave"
                />
              </v-dialog> -->
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
      isEditJobModalOpen: false,
      search: '',
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Default', value: 'default' },
        { text: 'Actions', value: 'action', sortable: false },
      ],
      profiles: [{ id: 0, name: 'First profile' }, { id: 1, name: 'Second profile' }],
      defaultProfile: [],
      currentProfileSettings: null,
      currentProfileId: null,
    };
  },

  methods: {
    async handleClickDeleteProfileButton(profile) {
      const res = await this.$confirm('Are you sure that you want to delete this profile?');

      if (res) {
        try {
          console.log(profile);
        // eslint-disable-next-line no-empty
        } catch (e) {
        }
      }
    },

    handleClickNewProfileButton() {
      this.isNewProfileModalOpen = true;
    },

    closeAddProfileForm() {
      this.isNewProfileModalOpen = false;
    },

    async handleNewProfileFormSave(profile) {
      try {
        console.log(profile);
        this.isNewProfileModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },
  },
};
</script>

<style>

</style>
