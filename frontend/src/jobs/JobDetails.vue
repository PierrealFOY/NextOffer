<script setup lang="ts">
import { useJobStore } from '@/stores/jobStore'
import type { Job } from '@/types/Job'
import {
  Banknote,
  BriefcaseBusiness,
  Building,
  Calendar,
  MapPin,
  NotepadText,
  Maximize2,
  ArrowLeft,
} from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { inject } from 'vue'

import DOMPurify from 'dompurify'
import { useSidebar } from '@/components/ui/sidebar'

const props = defineProps<{
  job: Job
  selectedJob?: Job | null
  fullScreen?: boolean
}>()

const route = useRoute()
const router = useRouter()
const jobId = computed(() => route.params.jobId as string)
const jobStore = useJobStore()
const jobFromStore = computed(() => jobStore.getJobById(jobId.value))
const jobData = computed(() => props.job ?? jobFromStore.value)

const sanitizedDescription = computed(() =>
  jobData.value?.description ? DOMPurify.sanitize(jobData.value.description) : '',
)
const isFullScreenRoute = computed(() => route.path === `/jobDetails/${jobData.value?.id}`)
const isFullScreen = computed(() => props.fullScreen || isFullScreenRoute.value)

const goToJobDetailsPage = () => {
  if (jobData.value?.id) {
    router.push(`/jobDetails/${jobData.value.id}`)
  }
}
const { isMobile, open } = useSidebar()
const isHeaderVisible = inject('isHeaderVisible', ref(true))

const containerClasses = computed(() => {
  if (isMobile.value) return 'mt-6 w-[90vw] justify-center -mx-1'
  if (isFullScreen.value) {
    return open.value ? 'mt-10 w-[90vw]' : 'mt-10 w-[85vw] pb-10 overflow-y-auto overflow-x-hidden'
  }
  return isHeaderVisible.value ? 'top-16 mt-16 h-[68%]' : 'top-2 mt-0 h-[90%]'
})

const cardWidthClass = computed(() => {
  if (isFullScreen.value) return open.value ? 'w-[85%] h-[90%] ' : 'w-[90%]'
  return open.value ? 'w-[95%]' : 'w-[95%]'
})

const descriptionHeightClass = computed(() => {
  if (isFullScreen.value) return 'h-full'
  return isHeaderVisible.value ? 'max-h-40' : 'max-h-80'
})
</script>

<template>
  <div
    class="mb-4 flex w-full transition-all duration-300 ease-in-out md:justify-center"
    :class="containerClasses"
  >
    <div
      :class="cardWidthClass"
      class="flex h-full flex-col space-y-4 rounded-lg border border-accentPrimary bg-baseMedium p-6 shadow-br-light dark:border-mintGreen dark:bg-neutral-800 dark:shadow-br-dark"
    >
      <header class="flex w-full">
        <Button
          type="button"
          class="ml-auto flex cursor-pointer bg-gray-300 hover:bg-gray-200 dark:bg-neutral-800 dark:hover:bg-neutral-700"
          title="Cliquez pour agrandir"
          v-if="!isFullScreen || !isFullScreenRoute"
          @click="goToJobDetailsPage"
        >
          <Maximize2 class="transition hover:text-primary" :size="24" />
        </Button>
        <Button
          type="button"
          class="justify-start bg-gray-300 hover:bg-gray-200 dark:bg-neutral-800 dark:hover:bg-neutral-700"
          title="Cliquez pour revenir en arrière"
          v-if="isFullScreen && isFullScreenRoute"
          @click="router.back()"
        >
          <ArrowLeft class="mb-1 scale-125 cursor-pointer transition" />
        </Button>
      </header>

      <h2 class="text-xl font-bold">{{ jobData?.title }}</h2>

      <div class="space-y-3 text-sm">
        <div class="flex items-center space-x-2">
          <Building :size="18" />
          <span class="italic">{{ jobData?.company }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <MapPin :size="18" />
          <span>{{ jobData?.location }}</span>
        </div>
        <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
          <div class="flex items-center space-x-2">
            <Banknote :size="18" />
            <span>{{ jobData?.salary || '-' }}</span>
          </div>
          <div class="flex items-center space-x-2">
            <BriefcaseBusiness :size="18" />
            <span>{{ jobData?.typeContrat || '-' }}</span>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <Calendar :size="18" />
          <span>{{ jobData?.dateCreation || '-' }}</span>
        </div>
      </div>

      <div class="pt-4">
        <div class="flex items-center space-x-2 pb-2">
          <NotepadText :size="18" />
          <p class="font-medium">Description du poste :</p>
        </div>
        <div
          :class="descriptionHeightClass"
          class="overflow-y-auto overflow-x-hidden break-words rounded bg-white/5 p-2 text-sm leading-relaxed transition-all duration-300 ease-in-out"
        >
          <div
            v-if="jobData?.description"
            class="whitespace-pre-line"
            v-html="sanitizedDescription"
          ></div>
          <p v-else>-</p>
        </div>
      </div>
    </div>
  </div>
</template>
