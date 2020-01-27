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
                <v-flex xs12>
                  <v-text-field v-model="jobName" label="Name"></v-text-field>
                </v-flex>
              </v-row>
              <div class="scroll-container">
                <JobInputsFormGenerator
                :default-settings="settings"
                :default-job-settings="jobSettings"
                :default-number-columns-per-row="2"
                @change="handleJobInputsFormGeneratorChange" />
              </div>
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
  VCard, VCardTitle, VCardText, VContainer, VRow, VTextField,
  VCardActions, VSpacer, VBtn, VFlex, VCombobox,
} from 'vuetify/lib';
import { mapState, mapGetters } from 'vuex';
import JobInputsFormGenerator from '../JobInputsFormGenerator.vue';

export default {
  name: 'CreateEditJobForm',
  components: {
    VCard,
    VCardTitle,
    VCardText,
    VContainer,
    VRow,
    VTextField,
    VCardActions,
    VSpacer,
    VBtn,
    VFlex,
    VCombobox,
    JobInputsFormGenerator,
  },

  props: {
    title: {
      type: String,
      default: 'Create new job',
    },
    job: {
      type: Object,
      default: () => ({ id: 0, name: '' }),
    },
    defaultJobSettings: {
      type: Object,
      default: () => ({}),
    },
  },

  computed: {
    ...mapGetters([
      'getNoneOptionalSettings',
      'getProfileById',
    ]),

    ...mapState([
      'profiles',
      'settings',
      'profileJobSettings',
    ]),
  },

  data() {
    return {
      jobName: this.job.name,
      jobSettings: this.defaultJobSettings,
      selectedProfile: null,
      numberColumnsPerRow: 2,
    };
  },

  created() {
    if (!this.job.id) {
      this.$store.dispatch('loadProfiles').then(() => {
        const defaultProfileId = parseInt(window.localStorage.getItem('defaultProfileId'), 10);

        if (defaultProfileId !== 'undefined' && defaultProfileId) {
          this.selectedProfile = this.getProfileById(defaultProfileId);
          if (this.selectedProfile) {
            this.setJobSettingsFromProfile(this.selectedProfile.id);
          }
        }
      });

      this.$store.dispatch('loadSettings').then(() => {
        this.getNoneOptionalSettings.forEach((s) => { this.$set(this.jobSettings, s.key, ''); });
      });
    } else {
      this.$store.dispatch('loadSettings');
    }
  },

  methods: {
    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.jobSettings, this.jobName, this.job.id);
    },

    handleJobInputsFormGeneratorChange(jobSettings) {
      this.jobSettings = jobSettings;
    },

    async setJobSettingsFromProfile(profileId) {
      try {
        await this.$store.dispatch('fetchProfileJobSettings', profileId);
        if (this.profileJobSettings) {
          this.jobSettings = Object.assign({}, this.jobSettings, this.profileJobSettings);
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
.scroll-container {
  height: 25vh;
  overflow-y: auto;
}
</style>
