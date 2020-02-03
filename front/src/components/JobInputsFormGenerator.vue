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
      <v-row v-for="(rowJobs, i) in rowsJobs" v-bind:key="i">
        <v-col v-for="rowJob in rowJobs" v-bind:key="rowJob.key"
        cols="12" :sm="12/defaultNumberColumnsPerRow" :md="12/defaultNumberColumnsPerRow">
          <v-text-field
          :value="rowJob.value"
          :label="rowJob.name"
          @change="handleFormInputChange($event, rowJob.key)">
            <template v-slot:prepend v-if="rowJob.is_optional">
              <v-icon size="25px" class="mr-2" @click="handleDeleteOptionIconClick(rowJob.key)">
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

  computed: {
    rowsJobs() {
      const result = [];
      let i = 0;
      let j = 0;
      if (Object.keys(this.jobOptions).length > 0) { result[i] = []; }

      Object.keys(JSON.parse(JSON.stringify(this.jobOptions))).forEach((key) => {
        if (j >= this.defaultNumberColumnsPerRow) {
          j = 0;
          i += 1;
          result[i] = [];
        }

        const option = this.options.find(x => x.key === key);
        result[i].push({
          key, value: this.jobOptions[key], name: option ? option.name : '', is_optional: option ? option.is_optional : null,
        });
        j += 1;
      });

      return result;
    },
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

    getJobOptionsKeys() {
      return Object.keys(this.jobOptions);
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
