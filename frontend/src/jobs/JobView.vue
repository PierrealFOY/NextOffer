<template>
  <div class="w-full">
    <TerminalHeader @search="handleSearch" />
    <JobList :jobs="filteredJobs" @update:liked="updateJobLiked" @update:seen="updateJobSeen" />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
})

import TerminalHeader from '../layout/TerminalHeader.vue'
import JobList from '../jobs/JobList.vue'
import { ref, computed, onMounted } from 'vue'
import { useJobStore } from '../stores/jobStore'
import type { Job } from '@/types/Job'

const props = defineProps<{
  jobs: Job[]
}>()

const emit = defineEmits<{
  (e: 'update:liked', jobId: string): void
  (e: 'update:seen', jobId: string): void
}>()

const store = useJobStore()
const searchQuery = ref('')

const filteredJobs = computed(() => {
  return store.filteredJobs(searchQuery.value)
})

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})

const handleSearch = (query: string) => {
  searchQuery.value = query
}

const updateJobLiked = (jobId: string) => {
  emit('update:liked', jobId)
}

const updateJobSeen = (jobId: string) => {
  emit('update:seen', jobId)
}
</script>
