<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { toast } from '@/components/ui/toast'
import { useJobStore } from '@/stores/jobStore'
import type { Job } from '@/types/Job'

const props = defineProps<{
  job: Job
}>()

const store = useJobStore()
const handleAppliedJobUpdate = async (jobId: number) => {
  if (!jobId) {
    console.log('Job ID is missing')
  }
  await store.applyJob(jobId)
  toast({
    title: 'Candidature envoyée ! 📨',
    description: `Vous avez envoyé une candidature pour le poste ${props.job.title}.`,
    class: 'dark:bg-gray-300 bg-neutral-500 text-green-300 dark:text-green-700',
    duration: 7000,
  })
}
</script>

<template>
  <div class="h-full rounded-sm border bg-baseMedium py-1 dark:bg-neutral-800">
    <Popover>
      <PopoverTrigger as-child>
        <Button variant="ghost">
          <p>Avez-vous candidaté<br />à cette offre ?</p>
        </Button>
      </PopoverTrigger>
      <PopoverContent
        side="right"
        class="ml-4 flex w-full scale-90 flex-col gap-1 border border-gray-400 bg-baseMedium dark:bg-neutral-800"
      >
        <Button
          class="bg-blue-500 text-black dark:text-white dark:hover:bg-baseDark"
          @click="handleAppliedJobUpdate(job.id)"
          >Oui</Button
        >
        <Button class="bg-red-500 text-black dark:text-white dark:hover:bg-baseDark">Non</Button>
      </PopoverContent>
    </Popover>
  </div>
</template>
