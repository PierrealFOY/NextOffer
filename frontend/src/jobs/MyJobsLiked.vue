<template>
  <div class="w-full">
    <h1 class="my-4">MES OFFRES LIKÉES: {{ store.likedJobs.length }}</h1>
    <JobList
      :enableInfiniteScroll="false"
      :isLoading="false"
      :jobs="store.likedJobs"
      :applyOpacity="false"
      :allowCardDetails="false"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
})

import JobList from '../jobs/JobList.vue'
import { onMounted } from 'vue'
import { useJobStore } from '../stores/jobStore'

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0 && !store.isLoading) store.fetchJobs()
})
</script>
