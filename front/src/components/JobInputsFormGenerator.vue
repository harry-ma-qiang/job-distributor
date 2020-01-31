<template>
    <v-container>
      <v-row>
        <v-combobox
          v-model="selectedOptions"
          :items="getOptionalOptions(options)"
          item-text="name"
          label="Select additional options"
          multiple
          outlined
          dense
          chips
          :small-chips="true"
          @input="handleComboboxOptionsInput"
        ></v-combobox>
      </v-row>
      <v-row v-for="i in getNumberInputRows()"
      v-bind:key="i">
        <v-col v-for="s in getColumnNumberRange(i)" v-bind:key="s"
        cols="12" :sm="12/defaultNumberColumnsPerRow" :md="12/defaultNumberColumnsPerRow">
          <v-text-field
          v-if="getNumberOfJobOptions() > s"
          :value="jobOptions[getJobOptionsKeys()[s]]"
          :label="getNameOfOptionByKey(getJobOptionsKeys()[s])"
          @change="handleFormInputChange($event, getJobOptionsKeys()[s])">
            <template v-slot:prepend v-if="getIsOptionalOfOptionByKey(getJobOptionsKeys()[s])">
              <v-icon
                size="25px"
                class="mr-2"
                @click="handleDeleteOptionIconClick(getJobOptionsKeys()[s])"
              >
                close
              </v-icon>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import {
  VContainer, VRow, VCol, VTextField, VIcon, VCombobox,
} from 'vuetify/lib';
import Vue from 'vue';

export default {
  name: 'CreateEditJobForm',
  components: {
    VContainer,
    VRow,
    VCol,
    VIcon,
    VTextField,
    VCombobox,
  },

  props: {
    options: {
      type: Array,
      default: () => ([]),
    },
    jobOptions: {
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
    jobOptions(newVal) {
      this.selectedOptions = this.getOptionsFromJobOptions(
        this.getOptionalOptions(this.options), newVal,
      );
    },
  },

  data() {
    return {
      numberColumnsPerRow: this.defaultNumberColumnsPerRow,
      selectedOptions: [],
    };
  },

  created() {
    this.selectedOptions = this.getOptionsFromJobOptions(
      this.getOptionalOptions(this.options), this.jobOptions,
    );
  },

  methods: {
    getOptionsFromJobOptions(options, jobOptions) {
      return options.filter(x => Object.keys(jobOptions).find(k => k === x.key));
    },

    getOptionalOptions: options => options.filter(s => s.is_optional),

    setJobOptions(options) {
      options.forEach((s) => { this.$set(this.jobOptions, s.key, ''); });
    },

    deleteJobOptions(options) {
      options.forEach((s) => { Vue.delete(this.jobOptions, s.key); });
    },

    getJobOptionsObject() {
      return JSON.parse(JSON.stringify(this.jobOptions));
    },

    getJobOptionsKeys() {
      return Object.keys(this.getJobOptionsObject());
    },

    getOptionalOptionsKeys() {
      return Object.keys(this.options).filter(s => s.is_optional);
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

    getIsOptionalOfOptionByKey(key) {
      const option = this.options.find(x => x.key === key);

      return option ? option.is_optional : null;
    },

    getJobOptionByOrderNumber(number) {
      return this.jobOptions[Object.keys(this.jobOptions)[number]];
    },

    async handleDeleteOptionIconClick(jobOptionKey) {
      const res = await this.$confirm('Are you sure that you want to delete this option?');

      if (res) {
        this.$emit('deleteJobOption', jobOptionKey);
      }
    },

    handleComboboxOptionsInput(options) {
      options.forEach((o) => {
        if (!this.getJobOptionsKeys().includes(o.key)) {
          this.$emit('addJobOption', o.key);
        }
      });

      const optionalOptions = this.getOptionalOptions(this.options);
      this.getJobOptionsKeys().forEach((k) => {
        if (!options.filter(s => s.key === k).length
        && optionalOptions.filter(s => s.key === k).length) {
          this.$emit('deleteJobOption', k);
        }
      });
    },

    handleFormInputChange(jobOptionValue, jobOptionKey) {
      const updatedJobOption = {};
      updatedJobOption[jobOptionKey] = jobOptionValue;

      this.$emit('updateJobOption', updatedJobOption);
    },
  },
};
</script>

<style>
</style>
