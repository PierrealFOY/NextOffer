<template>
  <div class="w-full">
    <h1 class="my-4">MES OFFRES LIKÉES</h1>
    <JobList
      :enableInfiniteScroll="false"
      :isLoading="false"
      :jobs="likedJobs"
      @update:liked="updateJobLiked"
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
  (e: 'update:liked', jobId: string): void
}>()

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})

const likedJobs = computed(() => store.likedJobs)

const updateJobLiked = (jobId: string) => {
  console.log('MyJobsView received liked update for ID:', jobId)
  emit('update:liked', jobId)
}
</script>
