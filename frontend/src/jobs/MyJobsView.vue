<template>
  <div :class="{ 'ml-24': open }" class="w-full transition-all duration-300">
    <h1 class="my-4">MES OFFRES</h1>

    <div class="mb-4 flex space-x-4 border-b">
      <RouterLink
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
import { onMounted } from 'vue'
import { useJobStore } from '../stores/jobStore'
import { useSidebar } from '@/components/ui/sidebar'

const store = useJobStore()
const { open } = useSidebar()

onMounted(() => {
  if (store.jobs.length === 0) store.fetchJobs()
})
</script>
