<template>
  <div class="w-full">
    <h1 class="my-4">MES CANDIDATURES ENVOYEES</h1>
    <JobList
      :enableInfiniteScroll="false"
      :isLoading="false"
      :jobs="appliedJobs"
      @update:applied="updateJobApplied"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
})

import JobList from '../jobs/JobList.vue'
import { onMounted, computed } from 'vue'
import { useJobStore } from '../stores/jobStore'

const emit = defineEmits<{
  (e: 'update:applied', jobId: string): void
}>()

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})

const appliedJobs = computed(() => store.jobs.filter((job) => job.applicationSent))

const updateJobApplied = (jobId: string) => {
  emit('update:applied', jobId)
}
</script>
