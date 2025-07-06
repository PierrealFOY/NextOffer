<template>
  <div :class="{ 'ml-24': open }" class="w-full transition-all duration-300">
    <h1 class="my-4">MES OFFRES</h1>

    <div class="mb-4 flex space-x-4 border-b">
      <RouterLink
        :jobs="likedJobs"
        to="/myJobs/liked"
        class="pb-2 text-accentPrimary dark:text-mintGreen"
        :class="{
          'border-b-2 border-accentPrimary font-semibold dark:border-mintGreen':
            $route.name === 'myJobsLiked',
        }"
      >
        Likées
      </RouterLink>
      <RouterLink
        to="/myJobs/seen"
        class="pb-2 text-accentPrimary dark:text-mintGreen"
        :class="{
          'border-b-2 border-accentPrimary font-semibold dark:border-mintGreen':
            $route.name === 'myJobsSeen',
        }"
      >
        Consultées
      </RouterLink>
      <RouterLink
        to="/myJobs/applied"
        class="pb-2 text-accentPrimary dark:text-mintGreen"
        :class="{
          'border-b-2 border-accentPrimary font-semibold dark:border-mintGreen':
            $route.name === 'myJobsApplied',
        }"
      >
        Candidatures envoyées
      </RouterLink>
    </div>

    <router-view />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
})

import { onMounted, computed } from 'vue'
import { useJobStore } from '../stores/jobStore'
import { useSidebar } from '@/components/ui/sidebar';

const emit = defineEmits<{
  (e: 'update:liked', jobId: string): void
}>()

const store = useJobStore()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})

const likedJobs = computed(() => store.likedJobs)
const { isMobile, open } = useSidebar()
</script>
