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
              <JobInputsFormGenerator
              :default-job-options="profile.Options"
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
  VCard, VCardTitle, VCardText, VContainer, VRow, VCol, VTextField, VCardActions, VSpacer, VBtn,
} from 'vuetify/lib';
import { mapGetters } from 'vuex';
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
  },

  data() {
    return {
      profile: this.defaultProfile,
    };
  },

  created() {
    if (!this.profile.Name) {
      this.$store.dispatch('loadOptions').then(() => {
        this.setDefaultProfileOptions(this.getNoneOptionalOptions);
      });
    } else {
      this.$store.dispatch('loadOptions');
    }
  },

  methods: {
    setDefaultProfileOptions(options) {
      options.forEach((s) => { this.$set(this.profile.Options, s.key, ''); });
    },

    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.profile, this.profileId);
    },

    handleJobInputsFormGeneratorChange(jobOptions) {
      this.profile.Options = jobOptions;
    },
  },
};
</script>

<style>

</style>
