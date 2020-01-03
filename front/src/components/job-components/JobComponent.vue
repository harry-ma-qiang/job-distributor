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
          :items="jobQueue"
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
                  @close = "closeAddJobForm"
                  @save = "handleNewJobFormSave"
                />
              </v-dialog>
              <v-dialog
                v-model="isEditJobModalOpen"
                v-if="isEditJobModalOpen"
                max-width="500px">
                <CreateEditJobForm
                  title="Edit job"
                  :default-job="currentJobSettings"
                  :job-id="currentJobId"
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
              @click="deleteJobButton(item)"
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
import config from 'config';
import axios from 'axios';
import CreateEditJobForm from './CreateEditJobForm.vue';

const { baseUrl } = config.api;

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
        { text: 'Job Id', value: 'id' },
        { text: 'Status', value: 'status' },
        { text: 'Last Update', value: 'lastUpdate' },
        { text: 'Actions', value: 'action', sortable: false },
      ],
      jobQueue: [{ id: '12', status: 'todo', lastUpdate: '23/12/19' }],
      currentJobSettings: null,
      currentJobId: null,
      jobInterval: null,
    };
  },

  created() {
    this.fetchJobs().catch(() => {});

    this.jobInterval = setInterval(() => {
      this.fetchJobs();
    }, 10000);
  },

  methods: {
    async handleEditJobIconClick(job) {
      try {
        const jobSettings = await this.fetchJobSettings(job.id);
        this.currentJobSettings = jobSettings.data;
        this.currentJobId = job.id;
        this.isEditJobModalOpen = true;
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async deleteJobButton(job) {
      const res = await this.$confirm('Are you sure that you want to delete this job?');

      if (res) {
        try {
          await this.deleteJob(job.id);
          await this.fetchJobs();
        // eslint-disable-next-line no-empty
        } catch (e) {
        }
      }
    },

    handleAddNewJobClick() {
      this.isNewJobModalOpen = true;
    },

    closeAddJobForm() {
      this.isNewJobModalOpen = false;
    },

    async handleNewJobFormSave(job) {
      try {
        await this.addJob({
          Bitrate: job.Bitrate,
          Framerate: job.Framerate,
          Codec: job.Codec,
        });

        this.isNewJobModalOpen = false;
        await this.fetchJobs();
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    handleEditJobFormClose() {
      this.isEditJobModalOpen = false;
    },

    async handleEditJobFormSave(attributes, id) {
      try {
        await this.editJob(id, {
          Bitrate: attributes.Bitrate,
          Framerate: attributes.Framerate,
          Codec: attributes.Codec,
        });

        this.isEditJobModalOpen = false;
        await this.fetchJobs();
      // eslint-disable-next-line no-empty
      } catch (e) {
      }
    },

    async fetchJobs() {
      try {
        const response = await axios.get(`${baseUrl}/api/getJobs`);

        if (response) {
          this.jobQueue = response.data;
        } else {
          throw new Error('Resoponse is empty');
        }
      } catch (e) {
        throw new Error('Can not fetch jobs list');
      }
    },

    async fetchJobSettings(id) {
      try {
        const response = await axios.get(`${baseUrl}/api/getAttributes/${id}`);
        if (response) {
          return response;
        }
        throw new Error('Resoponse is empty');
      } catch (e) {
        throw new Error('Can not fetch job settings');
      }
    },

    async addJob(job) {
      try {
        await axios.post(`${baseUrl}/api/job`, job);
      } catch (e) {
        throw new Error(e.message);
      }
    },

    async deleteJob(id) {
      try {
        await axios.delete(`${baseUrl}/api/job/${id}`);
      } catch (e) {
        throw new Error(`Can not delete job ${id}`);
      }
    },

    async editJob(id, attributes) {
      try {
        await axios.post(`${baseUrl}/api/updateJob/${id}`, attributes);
      } catch (e) {
        throw new Error(e.message);
      }
    },
  },
};
</script>

<style>

</style>
