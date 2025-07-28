<template>
  <div class="w-full">
    <JobList :jobs="store.displayedJobs" />
  </div>
</template>

<script setup lang="ts">
import JobList from '../jobs/JobList.vue'
import { onMounted } from 'vue'
import { useJobStore } from '../stores/jobStore'

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})
</script>
