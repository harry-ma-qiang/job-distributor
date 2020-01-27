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
                <v-container>
                  <v-row v-for="i in getNumberInputRows()"
                  v-bind:key="i">
                      <v-col v-for="s in getColumnNumberRange(i)" v-bind:key="s"
                      cols="12" sm="6" md="6">
                        <v-text-field
                        v-if="getNumberOfJobSettings() > s"
                        v-model="jobSettings[Object.keys(jobSettings)[s]]"
                        :label="getNameOfSettingByKey(Object.keys(jobSettings)[s])">
                        </v-text-field>
                      </v-col>
                  </v-row>
                </v-container>
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
    range(start, end) {
      return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
    },

    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.jobSettings, this.jobName, this.job.id);
    },

    async setJobSettingsFromProfile(profileId) {
      try {
        await this.$store.dispatch('fetchProfileJobSettings', profileId);
        if (this.profileJobSettings) {
          this.jobSettings = Object.assign({}, this.jobSettings, this.profileJobSettings);
          console.log(this.jobSettings);
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

    getNumberInputRows() {
      return Array.from(Array(
        Math.ceil(Object.keys(this.jobSettings).length / this.numberColumnsPerRow),
      ).keys());
    },

    getColumnNumberRange(number) {
      return this.range(number * this.numberColumnsPerRow, number * this.numberColumnsPerRow + 1);
    },

    getNumberOfJobSettings() {
      return Object.keys(this.jobSettings).length;
    },

    getNameOfSettingByKey(key) {
      const setting = this.settings.find(x => x.key === key);
      return setting ? setting.name : '';
    },

    getJobSettingByOrderNumber(number) {
      return this.jobSettings[Object.keys(this.jobSettings)[number]];
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
