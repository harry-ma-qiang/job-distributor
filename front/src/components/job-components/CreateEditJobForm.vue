<template>
    <v-card>
        <v-card-title>
            <span class="headline">{{ title }}</span>
        </v-card-title>

        <v-card-text>
            <v-container>
            <v-row>
              <v-flex xs12>
                <v-combobox
                  v-model="selectedProfile"
                  :items="profiles"
                  item-text="name"
                  label="Select profile to fill out fields automatically"
                  v-on:change="handleChangeProfileComboboxValue"
                ></v-combobox>
              </v-flex>
            </v-row>
            <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="job.Bitrate" label="Bit rate"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="job.Framerate" label="Frame rate"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="job.Codec" label="Codec"></v-text-field>
                </v-col>
            </v-row>
            </v-container>
        </v-card-text>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeForm">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="saveForm">Save</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import {
  VCard, VCardTitle, VCardText, VContainer, VRow, VCol, VTextField,
  VCardActions, VSpacer, VBtn, VFlex, VCombobox,
} from 'vuetify/lib';
import { mapState, mapGetters } from 'vuex';

export default {
  name: 'CreateEditJobForm',
  components: {
    VCard,
    VCardTitle,
    VCardText,
    VContainer,
    VRow,
    VCol,
    VTextField,
    VCardActions,
    VSpacer,
    VBtn,
    VFlex,
    VCombobox,
  },

  props: {
    title: {
      type: String,
      default: 'Create new job',
    },
    defaultJob: {
      type: Object,
      default: () => ({ Bitrate: '', Framerate: '', Codec: '' }),
    },
    jobId: {
      type: Number,
      default: 0,
    },
  },

  computed: {
    ...mapGetters([
      'getProfileById',
    ]),

    ...mapState([
      'profiles',
      'profileJobSettings',
    ]),
  },

  data() {
    return {
      job: this.defaultJob,
      selectedProfile: null,
    };
  },

  created() {
    this.$store.dispatch('loadProfiles').then(() => {
      const defaultProfileId = parseInt(window.localStorage.getItem('defaultProfileId'), 10);

      if (defaultProfileId !== 'undefined' && defaultProfileId) {
        this.selectedProfile = this.getProfileById(defaultProfileId);
        if (this.selectedProfile) {
          this.setJobSettingsFromProfile(this.selectedProfile.id);
        }
      }
    });
  },

  methods: {
    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.job, this.jobId);
    },

    async setJobSettingsFromProfile(profileId) {
      try {
        await this.$store.dispatch('fetchProfileJobSettings', profileId);
        if (this.profileJobSettings) {
          this.job = this.profileJobSettings;
        }
        // eslint-disable-next-line no-empty
      } catch (e) {

      }
    },

    async handleChangeProfileComboboxValue(profile) {
      try {
        await this.setJobSettingsFromProfile(profile.id);
        // eslint-disable-next-line no-empty
      } catch (e) {

      }
    },
  },
};
</script>

<style>

</style>
