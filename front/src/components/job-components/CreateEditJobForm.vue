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
                :default-job-options="jobOptions"
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
    defaultJobOptions: {
      type: Object,
      default: () => ({}),
    },
  },

  computed: {
    ...mapGetters([
      'getNoneOptionalOptions',
      'getProfileById',
    ]),

    ...mapState([
      'profiles',
      'profileJobOptions',
    ]),
  },

  data() {
    return {
      jobName: this.job.name,
      jobOptions: this.defaultJobOptions,
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
            this.setJobOptionsFromProfile(this.selectedProfile.id);
          }
        }
      });

      this.setDefaultJobOptions();
    } else {
      this.$store.dispatch('loadOptions');
    }
  },

  methods: {
    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.jobOptions, this.jobName, this.job.id);
    },

    setDefaultJobOptions() {
      this.$store.dispatch('loadOptions').then(() => {
        this.getNoneOptionalOptions.forEach((s) => { this.$set(this.jobOptions, s.key, ''); });
      });
    },

    handleJobInputsFormGeneratorChange(jobOptions) {
      this.jobOptions = jobOptions;
    },

    async setJobOptionsFromProfile(profileId) {
      try {
        await this.$store.dispatch('fetchProfileJobOptions', profileId);
        if (this.profileJobOptions) {
          this.jobOptions = Object.assign({}, this.jobOptions, this.profileJobOptions);
        }
        // eslint-disable-next-line no-empty
      } catch (e) {

      }
    },

    async handleChangeProfileComboboxValue(profile) {
      if (profile) {
        try {
          await this.setJobOptionsFromProfile(profile.id);
        // eslint-disable-next-line no-empty
        } catch (e) {

        }
      } else {
        this.jobOptions = {};
        this.setDefaultJobOptions();
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
