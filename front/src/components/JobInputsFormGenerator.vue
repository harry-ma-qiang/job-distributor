<template>
    <v-container>
        <v-row v-for="i in getNumberInputRows()"
        v-bind:key="i">
            <v-col v-for="s in getColumnNumberRange(i)" v-bind:key="s"
            cols="12" sm="6" md="6">
            <v-text-field
            @change="handleTextFieldChange"
            v-if="getNumberOfJobSettings() > s"
            v-model="jobSettings[Object.keys(jobSettings)[s]]"
            :label="getNameOfSettingByKey(Object.keys(jobSettings)[s])">
            </v-text-field>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import {
  VContainer, VRow, VCol, VTextField,
} from 'vuetify/lib';

export default {
  name: 'CreateEditJobForm',
  components: {
    VContainer,
    VRow,
    VCol,
    VTextField,
  },

  props: {
    defaultSettings: {
      type: Array,
      default: () => [],
    },
    defaultJobSettings: {
      type: Object,
      default: () => ({}),
    },
    defaultNumberColumnsPerRow: {
      type: Number,
      default: 2,
    },
  },

  data() {
    return {
      jobSettings: this.defaultJobSettings,
      settings: this.defaultSettings,
      numberColumnsPerRow: this.defaultNumberColumnsPerRow,
    };
  },

  methods: {
    range(start, end) {
      return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
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

    handleTextFieldChange() {
      this.$emit('change', this.jobSettings);
    },
  },
};
</script>

<style>
</style>
