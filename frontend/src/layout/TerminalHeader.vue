<template>
  <div
    :class="{ 'pl-6': isMobile }"
    class="flex items-baseline justify-center gap-2 text-xl text-accentPrimary dark:text-mintGreen"
  >
    <Search @search="handleSearch" />
  </div>
</template>

<script setup lang="ts">
import { useSidebar } from '@/components/ui/sidebar'
import Search from '../components/Search.vue'
const { isMobile } = useSidebar()

const emit = defineEmits(['search'])
const handleSearch = (query: string) => {
  emit('search', query)
}
</script>
