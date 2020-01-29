<template>
    <v-card flat>
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="jobs"
          :search="search"
          :items-per-page="5"
          sort-by="jobId"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>Job Queue</v-toolbar-title>
              <v-divider
                class="mx-4"
                inset
                vertical
              ></v-divider>
              <v-spacer></v-spacer>
              <v-btn color="primary" dark class="mb-2" @click="handleAddNewJobClick">
                New Job
              </v-btn>
              <v-dialog v-model="isNewJobModalOpen" v-if="isNewJobModalOpen" max-width="500px">
                <CreateEditJobForm
                  @close = "handleCloseAddJobForm"
                  @save = "handleNewJobFormSave"
                />
              </v-dialog>
              <v-dialog
                v-model="isEditJobModalOpen"
                v-if="isEditJobModalOpen"
                max-width="500px">
                <CreateEditJobForm
                  title="Edit job"
                  :default-job-options="currentJobOptions"
                  :job="currentJob"
                  @close = "handleEditJobFormClose"
                  @save = "handleEditJobFormSave"
                />
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.action="{ item }">
              <v-icon
                  small
                  class="mr-2"
                  @click="handleEditJobIconClick(item)"
                >
                  edit
                </v-icon>
            <v-icon
              small
              @click="handleDeleteJobButtonClick(item)"
            >
              delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
</template>

<script>
import {
  VCard,
  VCardTitle,
  VTextField,
  VDataTable,
  VCardText,
  VIcon,
  VToolbar,
  VToolbarTitle,
  VDivider,
  VSpacer,
  VBtn,
  VDialog,
} from 'vuetify/lib';
import { mapState } from 'vuex';
import CreateEditJobForm from './CreateEditJobForm.vue';

export default {
  name: 'JobComponent',
  components: {
    CreateEditJobForm,
    VCard,
    VCardTitle,
    VTextField,
    VDataTable,
    VCardText,
    VIcon,
    VToolbar,
    VToolbarTitle,
    VDivider,
    VSpacer,
    VBtn,
    VDialog,
  },

  data() {
    return {
      isNewJobModalOpen: false,
      isEditJobModalOpen: false,
      search: '',
      headers: [
        { text: 'Id', value: 'id' },
        { text: 'Name', value: 'name' },
        { text: 'Status', value: 'status' },
        { text: 'Last Update', value: 'lastUpdate' },
        { text: 'Actions', value: 'action', sortable: false },
      ],
      currentJobOptions: null,
      currentJob: null,
      jobInterval: null,
    };
  },

  created() {
    this.$store.dispatch('loadJobs');

    this.jobInterval = setInterval(() => {
      this.$store.dispatch('loadJobs');
    }, 10000);
  },

  computed: mapState([
    'jobs',
    'jobOptions',
  ]),

  methods: {
    async handleEditJobIconClick(job) {
      try {
        await this.$store.dispatch('fetchJobOptions', job.id);
        this.currentJobOptions = this.jobOptions;
        this.currentJob = job;
        this.isEditJobModalOpen = true;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async handleDeleteJobButtonClick(job) {
      const res = await this.$confirm('Are you sure that you want to delete this job?');

      if (res) {
        try {
          await this.$store.dispatch('deleteJob', job.id);
        // eslint-disable-next-line no-empty
        } catch (e) {
        }
      }
    },

    handleAddNewJobClick() {
      this.isNewJobModalOpen = true;
    },

    handleCloseAddJobForm() {
      this.isNewJobModalOpen = false;
    },

    async handleNewJobFormSave(jobOptions, jobName) {
      try {
        await this.$store.dispatch('addJob', {
          Options: jobOptions,
          Name: jobName,
        });

        this.isNewJobModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    handleEditJobFormClose() {
      this.isEditJobModalOpen = false;
    },

    async handleEditJobFormSave(jobOptions, jobName, id) {
      try {
        await this.$store.dispatch('editJob', {
          id,
          data: {
            Options: jobOptions,
            Name: jobName,
          },
        });

        this.isEditJobModalOpen = false;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },
  },
};
</script>

<style>

</style>
