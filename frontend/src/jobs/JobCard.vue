<template>
  <div
    class="rounded border bg-card p-4 shadow-br-light hover:bg-muted hover:shadow-md dark:bg-neutral-800 dark:shadow-br-dark"
  >
    <div
      :class="{
        'opacity-[40%]': job.seen && applyOpacity,
      }"
      @click="goToJobDetails(job)"
      class="flex cursor-pointer"
    >
      <div class="flex w-full flex-col items-baseline gap-4 pb-2 text-foreground">
        <h2 class="flex items-baseline space-x-2 text-sm text-foreground">
          <span><BriefcaseBusiness /></span>
          <strong>{{ job?.title }}</strong>
        </h2>
        <div class="flex items-baseline space-x-2 text-sm">
          <span><Building2 /></span>
          <p class="italic">{{ job?.company }}</p>
        </div>
        <div class="flex items-baseline space-x-2 text-sm" @click.stop>
          <span><MapPin /></span>
          <p class="italic">{{ job?.location }}</p>
        </div>
        <div class="flex items-baseline space-x-2 text-sm" @click.stop>
          <span><Calendar /></span>
          <p class="italic">{{ dateCreationFormatted }}</p>
        </div>
        <div>
          <a
            type="button"
            :href="job.url"
            target="_blank"
            rel="noopener noreferrer"
            class="cursor-pointer text-base text-accentSecondary underline transition hover:text-primary"
            @click.stop="(event) => markJobSeen(job.id)"
          >
            Voir l'offre
          </a>
        </div>
      </div>

      <div class="ml-8 flex items-center justify-center space-x-4">
        <div typeof="button" class="cursor-pointer justify-end" @click.stop="handletoggleLikeJob">
          <Heart
            :class="{
              'fill-green-700 text-green-700': job.liked,
              'text-green-700': !job.liked,
              'dark:fill-mintGreen dark:text-mintGreen': job.liked,
              'dark:text-mintGreen': !job.liked,
            }"
            type="button"
          />
        </div>
        <div v-if="job.seen">
          <Eye class="text-accentPrimary dark:text-mintGreen" />
        </div>
        <div v-if="job.applicationSent">
          <Send class="text-accentPrimary dark:text-mintGreen" />
        </div>
      </div>
    </div>
    <div v-if="job.seen && !job.applicationSent" class="pt-4 text-center">
      <AskIfApplied
        class="mx-auto mb-4 w-2/3 rounded border-t border-accentPrimary text-center dark:border-mintGreen"
        :job="job"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Building2, BriefcaseBusiness, MapPin, Heart, Eye, Send, Calendar } from 'lucide-vue-next'
import type { Job } from '../types/Job'
import { useToast } from '@/components/ui/toast/use-toast'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useJobStore } from '@/stores/jobStore'
import { useRouter } from 'vue-router'
import AskIfApplied from './AskIfApplied.vue'

const authStore = useAuthStore()

const props = defineProps<{
  job: Job
  selectedJob?: Job | null
  applyOpacity?: boolean
}>()

const emit = defineEmits<{
  (e: 'select', job: Job): void
}>()

const { toast } = useToast()

const handletoggleLikeJob = async () => {
  if (!authStore.isLoggedIn) {
    toast({
      title: 'Impossible de liker le job !',
      description: 'Il faut être connecté pour liker un job',
      class: 'bg-gray-300 text-red-700',
    })
    return
  }

  await jobStore.toggleLikeWithFeedback(props.job.id)
}

const markJobSeen = async (jobId: number) => {
  await jobStore.seeJob(jobId)
  if (props.job.url) {
    window.open(props.job.url, '_blank')
  } else {
    goToJobDetails(props.job)
  }
}

const dateCreationFormatted = computed(() => {
  return new Date(props.job?.dateCreation ?? new Date()).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
})

// const route = useRoute()
const router = useRouter()
// const jobId = computed(() => route.params.jobId)
const jobStore = useJobStore()
// const jobFromStore = computed(() => jobStore.getJobById(Number(jobId.value)))
// const jobData = computed(() => props.job ?? jobFromStore.value)
const goToJobDetails = (job: Job) => {
  if (job.id) {
    router.push(`/jobDetails/${job.id}`)
  }
}
</script>
