<script setup lang="ts">
import { Button } from '@/components/ui/button';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useJobStore } from '@/stores/jobStore';
import type { Job } from '@/types/Job';

const props = defineProps<{
  job: Job
}>()

const store = useJobStore()
const handleAppliedJobUpdate = (jobId: string) => {
  store.updateAppliedJobs(jobId)
}
</script>

<template>
  <div class="border py-1 h-full w-30 rounded-sm dark:bg-neutral-800 bg-baseMedium">
    <Popover>
      <PopoverTrigger as-child>
        <Button variant="ghost">
          <p>Avez-vous candidaté<br/>à cette offre ?</p>
      </Button>
      </PopoverTrigger>
      <PopoverContent class="flex scale-90 w-full flex-col gap-1 dark:bg-neutral-800 bg-baseMedium">
        <Button class="text-black dark:bg-neutral-800 bg-baseMedium hover:bg-gray-200 dark:hover:bg-baseDark" @click="handleAppliedJobUpdate(job.id)">Oui</Button>
        <Button class="text-black dark:bg-neutral-800 bg-baseMedium hover:bg-gray-200 dark:hover:bg-baseDark" @click="console.log('Non')">Non</Button>
      </PopoverContent>
    </Popover>
  </div>
</template>
