<template>
    <v-container>
        <div v-if="!options">Loading Please wait...</div>
        <div v-else>
          <v-row v-for="i in getNumberInputRows()"
          v-bind:key="i">
            <v-col v-for="s in getColumnNumberRange(i)" v-bind:key="s"
            cols="12" :sm="12/defaultNumberColumnsPerRow" :md="12/defaultNumberColumnsPerRow">
            <v-text-field
            @change="handleTextFieldChange"
            v-if="getNumberOfJobOptions() > s"
            v-model="jobOptions[getJobOptionsKeys()[s]]"
            :label="getNameOfOptionByKey(getJobOptionsKeys()[s])">
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
    defaultJobOptions: {
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
    defaultJobOptions(newVal) {
      this.jobOptions = newVal;
    },
  },

  computed: {
    ...mapState([
      'options',
    ]),
  },

  created() {
    this.$store.dispatch('loadOptions');
  },

  data() {
    return {
      jobOptions: this.defaultJobOptions,
      numberColumnsPerRow: this.defaultNumberColumnsPerRow,
    };
  },

  methods: {
    getJobOptionsObject() {
      return JSON.parse(JSON.stringify(this.jobOptions));
    },

    getJobOptionsKeys() {
      return Object.keys(this.getJobOptionsObject());
    },

    getNumberInputRows() {
      return Array.from(Array(
        Math.ceil(this.getNumberOfJobOptions() / this.numberColumnsPerRow),
      ).keys());
    },

    getColumnNumberRange(number) {
      return this.range(number * this.numberColumnsPerRow, number
       * this.numberColumnsPerRow + this.numberColumnsPerRow - 1);
    },

    getNumberOfJobOptions() {
      return Object.keys(this.getJobOptionsObject()).length;
    },

    getNameOfOptionByKey(key) {
      const option = this.options.find(x => x.key === key);

      return option ? option.name : '';
    },

    getJobOptionByOrderNumber(number) {
      return this.jobOptions[Object.keys(this.jobOptions)[number]];
    },

    handleTextFieldChange() {
      this.$emit('change', this.jobOptions);
    },
  },
};
</script>

<style>
</style>
