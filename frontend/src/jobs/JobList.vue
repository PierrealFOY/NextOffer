<template>
  <div v-if="store.isLoading && store.jobs.length === 0" class="w-full items-center self-center">
    <SkeletonJobs />
  </div>

  <div class="mt-2 flex h-[calc(100vh-80px)] w-full gap-4 pt-4">
    <div
      :class="{
        'w-[80%]': !selectedJob && !isMobile,
        'w-full': isMobile,
      }"
      class="flex flex-col transition-all duration-300 ease-in-out"
    >
      <div v-for="job in props.jobs" :key="job.id" class="flex items-start space-x-4">
        <div
          :class="{
            'rounded-sm border-2 border-accentPrimary dark:border-mintGreen':
              job.id === selectedJob?.id,
            'mx-1': isMobile,
            'w-3/4': open,
          }"
          class="m-4 mb-4 w-full max-w-full transition-all duration-300 ease-in-out hover:scale-[102%]"
        >
          <JobCard
            :allowCardDetails="props.allowCardDetails"
            @select="handleSelectJob"
            :key="job.id + '-' + job.liked"
            :job="job"
            :applyOpacity="props.applyOpacity"
          />
        </div>
        <div v-if="job.seen && !job.applicationSent" class="pt-20">
          <AskIfApplied :job="job" />
        </div>
      </div>

      <div class="my-6 flex h-12 items-center justify-center pb-10 text-gray-400">
        <Button
          class="bg-accentPrimary dark:bg-mintGreen dark:text-black"
          v-if="props.enableClickScroll && store.hasMore && !store.isLoading"
          @click="loadMore"
        >
          Charger plus d'offres
        </Button>
        <span
          v-if="store.isLoading && store.jobs.length > 0"
          class="space-x-2 text-accentPrimary dark:text-mintGreen"
        >
          <p>Chargement...</p>
        </span>
        <span v-else-if="!store.hasMore">Pas d'autres offres disponibles</span>
      </div>
    </div>

    <div
      v-if="selectedJob && !isMobile"
      :class="[open ? 'w-[100%]' : 'w-[60%]', 'transition-all duration-300', 'mt-2']"
    >
      <JobDetails
        class="fixed"
        :job="selectedJob"
        @close="selectedJob = null"
        :selected-job="selectedJob"
      />
    </div>

    <div v-else-if="selectedJob && isMobile" class="right-4 top-16 mt-2 w-1/2 justify-end pl-2">
      <JobDetails
        :fullScreen="true"
        class="space-y-0"
        :job="selectedJob"
        @close="selectedJob = null"
        :selected-job="selectedJob"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import JobCard from './JobCard.vue'
import type { Job } from '../types/Job'
import { useJobStore } from '@/stores/jobStore'
import SkeletonJobs from '@/layout/SkeletonJobs.vue'
import AskIfApplied from './AskIfApplied.vue'
import { ref, onMounted } from 'vue'
import JobDetails from './JobDetails.vue'
import { Button } from '@/components/ui/button'
import { nextTick } from 'vue'
import { useSidebar } from '@/components/ui/sidebar'

const props = withDefaults(
  defineProps<{
    enableClickScroll?: boolean
    applyOpacity?: boolean
    jobs: Job[]
    allowCardDetails?: boolean
  }>(),
  {
    enableClickScroll: true,
    applyOpacity: true,
    allowCardDetails: true,
  },
)
const store = useJobStore()
const selectedJob = ref<Job | null>(null)
const loadMoreTrigger = ref<HTMLElement | null>(null)
const { isMobile, open } = useSidebar()

const handleSelectJob = (job: Job) => {
  if (props.allowCardDetails) selectedJob.value = job
}

const loadMore = async () => {
  if (store.isLoading || !store.hasMore) return
  const currentPosition = window.scrollY
  store.offset += store.limit
  await store.fetchJobs(store.offset, store.limit)
  await nextTick()
  await nextTick()
  window.scrollTo({
    top: currentPosition,
    behavior: 'auto',
  })
}

onMounted(() => {
  if (!props.enableClickScroll) return
  const observer = new IntersectionObserver(
    (entries) => {
      const [entry] = entries
      if (entry.isIntersecting && store.hasMore && !store.isLoading) {
        loadMore()
      }
    },
    {
      rootMargin: '0px 0px 100px 0px',
    },
  )

  if (loadMoreTrigger.value) {
    observer.observe(loadMoreTrigger.value)
  }
})
</script>
