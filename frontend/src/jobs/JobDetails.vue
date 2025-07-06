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
console.log('isFullScreenRoute', isFullScreenRoute.value)
const isFullScreen = computed(() => props.fullScreen || isFullScreenRoute.value)

const goToJobDetailsPage = () => {
  if (jobData.value?.id) {
    router.push(`/jobDetails/${jobData.value.id}`)
  }
}
const { isMobile, open } = useSidebar()

const isHeaderVisible = inject('isHeaderVisible', ref(true))
console.log('isHeaderVisible', isHeaderVisible.value)
</script>

<template>
  <div
    class="flex transition-all duration-300 ease-in-out"
    :class="[
      {
        'mt-10 w-[85vw] self-start overflow-y-auto overflow-x-hidden pb-10':
          isFullScreen && !isMobile && !open,
        'w-[85vw] mt-6': isMobile,
        'mt-10': isFullScreen && open && !isMobile,
        'top-16 mt-16 h-[70%]': isHeaderVisible && !isFullScreen,
        'top-0 mt-0 h-[85vh]': !isHeaderVisible && !isFullScreen,
      },
    ]"
  >
    <div
      :class="{ 'w-[80%] self-center': isFullScreen && open, 'w-[90%]': isFullScreen && !open }"
      class="flex flex-col space-y-4 rounded-lg border border-accentPrimary bg-baseMedium p-6 shadow-br-light dark:border-mintGreen dark:bg-neutral-800 dark:shadow-br-dark"
    >
      <header :class="{ 'justify-end': !isFullScreen }" class="flex w-full">
        <Button
          type="button"
          class="sticky flex cursor-pointer justify-end bg-neutral-800 hover:bg-neutral-700"
          title="Cliquez pour agrandir"
          v-if="!isFullScreen"
          @click="goToJobDetailsPage"
        >
          <Maximize2 class="transition hover:text-primary" :size="24" />
        </Button>
        <Button
          type="button"
          class="bg-neutral-800 p-0 hover:bg-neutral-700"
          title="Cliquez pour revenir en arrière"
          v-if="isFullScreen"
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
          :class="{
            'h-40': !isFullScreen && isHeaderVisible,
            'h-[12%]': !isFullScreen && !isHeaderVisible,
            'h-full': isFullScreen,
          }"
          class="overflow-y-auto rounded bg-white/5 p-2 text-sm leading-relaxed transition-all duration-200 ease-in-out"
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
