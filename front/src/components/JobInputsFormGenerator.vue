<template>
    <v-container>
        <div v-if="!settings">Loading Please wait...</div>
        <div v-else>
          <v-row v-for="i in getNumberInputRows()"
          v-bind:key="i">
            <v-col v-for="s in getColumnNumberRange(i)" v-bind:key="s"
            cols="12" :sm="12/defaultNumberColumnsPerRow" :md="12/defaultNumberColumnsPerRow">
            <v-text-field
            @change="handleTextFieldChange"
            v-if="getNumberOfJobSettings() > s"
            v-model="jobSettings[getJobSettingsKeys()[s]]"
            :label="getNameOfSettingByKey(getJobSettingsKeys()[s])">
            </v-text-field>
            </v-col>
        </v-row>
        </div>
    </v-container>
</template>

<script>
import {
  VContainer, VRow, VCol, VTextField,
} from 'vuetify/lib';
import { mapState } from 'vuex';

export default {
  name: 'CreateEditJobForm',
  components: {
    VContainer,
    VRow,
    VCol,
    VTextField,
  },

  props: {
    defaultJobSettings: {
      type: Object,
      default: () => ({}),
    },
    defaultNumberColumnsPerRow: {
      type: Number,
      default: 2,
      validator(value) {
        return value <= 4 && value > 0;
      },
    },
  },

  watch: {
    defaultJobSettings(newVal) {
      this.jobSettings = newVal;
    },
  },

  computed: {
    ...mapState([
      'settings',
    ]),
  },

  created() {
    this.$store.dispatch('loadSettings');
  },

  data() {
    return {
      jobSettings: this.defaultJobSettings,
      numberColumnsPerRow: this.defaultNumberColumnsPerRow,
    };
  },

  methods: {
    getJobSettingsObject() {
      return JSON.parse(JSON.stringify(this.jobSettings));
    },

    getJobSettingsKeys() {
      return Object.keys(this.getJobSettingsObject());
    },

    getNumberInputRows() {
      return Array.from(Array(
        Math.ceil(this.getNumberOfJobSettings() / this.numberColumnsPerRow),
      ).keys());
    },

    getColumnNumberRange(number) {
      return this.range(number * this.numberColumnsPerRow, number
       * this.numberColumnsPerRow + this.numberColumnsPerRow - 1);
    },

    getNumberOfJobSettings() {
      return Object.keys(this.getJobSettingsObject()).length;
    },

    getNameOfSettingByKey(key) {
      const setting = this.settings.find(x => x.key === key);

      return setting ? setting.name : '';
    },

    getJobSettingByOrderNumber(number) {
      return this.jobSettings[Object.keys(this.jobSettings)[number]];
    },

    handleTextFieldChange() {
      this.$emit('change', this.jobSettings);
    },
  },
};
</script>

<style>
</style>
