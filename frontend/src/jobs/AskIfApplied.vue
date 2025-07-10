<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { useJobStore } from '@/stores/jobStore'
import type { Job } from '@/types/Job'

const props = defineProps<{
  job: Job
}>()

const store = useJobStore()
const handleAppliedJobUpdate = (jobId: string) => {
  store.updateAppliedJobs(jobId)
}
</script>

<template>
  <div class="w-30 h-full rounded-sm border bg-baseMedium py-1 dark:bg-neutral-800">
    <Popover>
      <PopoverTrigger as-child>
        <Button variant="ghost">
          <p>Avez-vous candidaté<br />à cette offre ?</p>
        </Button>
      </PopoverTrigger>
      <PopoverContent class="flex w-full scale-90 flex-col gap-1 bg-baseMedium dark:bg-neutral-800">
        <Button
          class="bg-baseMedium text-black hover:bg-gray-200 dark:bg-neutral-800 dark:hover:bg-baseDark"
          @click="handleAppliedJobUpdate(job.id)"
          >Oui</Button
        >
        <Button
          class="bg-baseMedium text-black hover:bg-gray-200 dark:bg-neutral-800 dark:hover:bg-baseDark"
          >Non</Button
        >
      </PopoverContent>
    </Popover>
  </div>
</template>
