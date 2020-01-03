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
            <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="profile.Bitrate" label="Bit rate"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="profile.Framerate" label="Frame rate"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field v-model="profile.Codec" label="Codec"></v-text-field>
                </v-col>
            </v-row>
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
  },

  props: {
    title: {
      type: String,
      default: 'Create new profile',
    },
    defaultProfile: {
      type: Object,
      default: () => ({
        Name: '', Bitrate: '', Framerate: '', Codec: '',
      }),
    },
    profileId: {
      type: Number,
      default: 0,
    },
  },

  data() {
    return {
      profile: this.defaultProfile,
    };
  },

  methods: {
    closeForm() {
      this.$emit('close');
    },

    saveForm() {
      this.$emit('save', this.profile, this.profileId);
    },
  },
};
</script>

<style>

</style>
