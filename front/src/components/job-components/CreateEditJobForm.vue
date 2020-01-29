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
            <v-btn color="blue darken-1" text @click="handleClickCloseFormButton">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="handleClickSaveFormButton">Save</v-btn>
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
      'getDefaultProfile',
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
    this.$store.dispatch('loadOptions').then(() => {
      if (!this.job.id) {
        this.$store.dispatch('loadProfiles').then(() => {
          this.setDefaultJobOptions();
          this.setJobOptionsFromDefaultProfile();
        });
      }
    });
  },

  methods: {
    setJobOptionsFromDefaultProfile() {
      const defaultProfile = this.getDefaultProfile;

      if (defaultProfile) {
        this.selectedProfile = defaultProfile;
        this.setJobOptionsFromProfile(defaultProfile.id);
      }
    },

    setDefaultJobOptions() {
      this.getNoneOptionalOptions.forEach((s) => { this.$set(this.jobOptions, s.key, ''); });
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

    handleClickCloseFormButton() {
      this.$emit('close');
    },

    handleClickSaveFormButton() {
      this.$emit('save', this.jobOptions, this.jobName, this.job.id);
    },

    handleJobInputsFormGeneratorChange(jobOptions) {
      this.jobOptions = jobOptions;
    },

    async handleChangeProfileComboboxValue(profile) {
      this.jobOptions = {};

      try {
        if (profile) {
          await this.setJobOptionsFromProfile(profile.id);
        } else {
          await this.$store.dispatch('loadOptions');
          this.setDefaultJobOptions();
        }
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
