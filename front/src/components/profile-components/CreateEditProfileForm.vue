<template>
    <v-card>
        <v-card-title>
            <span class="headline">{{ title }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="profile.Name" label="Name"></v-text-field>
                </v-col>
            </v-row>
            <div class="scroll-container">
              <div v-if="!options">Loading Please wait...</div>
              <div v-else>
                <JobInputsFormGenerator
                :options="options"
                :job-options="profile.Options"
                :default-number-columns-per-row="2"
                @updateJobOption="handleUpdateJobOptionOfJobInputsFormGenerator"
                @deleteJobOption="handleDeleteJobOptionOfJobInputsFormGenerator"
                @addJobOption="handleAddJobOptionOfJobInputsFormGenerator" />
              </div>
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
  VCard, VCardTitle, VCardText, VContainer, VRow, VCol, VTextField, VCardActions, VSpacer, VBtn,
} from 'vuetify/lib';
import Vue from 'vue';
import { mapGetters, mapState } from 'vuex';
import JobInputsFormGenerator from '../JobInputsFormGenerator.vue';

export default {
  name: 'CreateEditProfileForm',
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
    JobInputsFormGenerator,
  },

  props: {
    title: {
      type: String,
      default: 'Create new profile',
    },
    defaultProfile: {
      type: Object,
      default: () => ({
        Name: '', Options: { type: Object, default: () => ({}) },
      }),
    },
    profileId: {
      type: Number,
      default: 0,
    },
  },

  computed: {
    ...mapGetters([
      'getNoneOptionalOptions',
    ]),

    ...mapState([
      'options',
    ]),
  },

  data() {
    return {
      profile: this.defaultProfile,
    };
  },

  created() {
    this.$store.dispatch('loadOptions').then(() => {
      // eslint-disable-next-line no-param-reassign
      this.options.forEach((o) => { o.is_optional = true; });
    });
  },

  methods: {
    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.profile, this.profileId);
    },

    handleUpdateJobOptionOfJobInputsFormGenerator(jobOption) {
      Object.assign(this.profile.Options, jobOption);
    },

    handleDeleteJobOptionOfJobInputsFormGenerator(jobOptionKey) {
      Vue.delete(this.profile.Options, jobOptionKey);
    },

    handleAddJobOptionOfJobInputsFormGenerator(jobOptionKey) {
      this.$set(this.profile.Options, jobOptionKey, '');
    },
  },
};
</script>

<style>

</style>
