<template>
  <div class="w-full">
    <h1 class="my-4">MES OFFRES CONSULTEES</h1>
    <JobList
      :enableInfiniteScroll="false"
      :isLoading="false"
      :jobs="seenJobs"
      :applyOpacity="false"
      @update:seen="updateJobSeen"
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
  (e: 'update:seen', jobId: string): void
}>()

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})

const seenJobs = computed(() => store.seenJobs)

const updateJobSeen = (jobId: string) => {
  emit('update:seen', jobId)
}
</script>
