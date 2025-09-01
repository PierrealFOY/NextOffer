<template>
  <div
    @click="activateSearch"
    v-motion
    :initial="{ opacity: 1 }"
    :animate="{ opacity: [1, 0.2, 1] }"
    :transition="{ repeat: Infinity, duration: 1 }"
    :class="{ 'mt-8 w-3/5': isMobile }"
    class="relative mt-2 flex w-1/3 cursor-pointer rounded border-2 border-accentPrimary dark:border-mintGreen"
  >
    <div class="flex items-center space-x-1">
      <input
        ref="searchInput"
        v-model="searchQuery"
        type="text"
        class="w-3/4 bg-transparent p-1 px-1 pl-2 text-sm text-accentPrimary placeholder:text-accentPrimary focus:w-full focus:outline-none dark:border-mintGreen dark:text-mintGreen dark:placeholder:text-mintGreen"
        :class="{ 'animate-pulseSlow': !isSearchActive }"
        :placeholder="isSearchActive ? '' : 'Rechercher _'"
        @keyup.enter="handleSearch"
        @blur="deactivateSearch"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useSidebar } from './ui/sidebar'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isSearchActive = ref(false)
const searchQuery = ref('')
const searchInput = ref<HTMLInputElement | null>(null)
const emit = defineEmits(['search'])
const { isMobile } = useSidebar()

const activateSearch = () => {
  isSearchActive.value = true
  setTimeout(() => {
    searchInput.value?.focus()
  }, 0)
}
const isJobViewRoute = computed(() => route.path != 'jobview')

const deactivateSearch = () => {
  if (searchQuery.value.trim() === '' || isJobViewRoute.value) {
    isSearchActive.value = false
    searchQuery.value = ''
  }
}

const handleSearch = () => {
  emit('search', searchQuery.value)
  router.push({ name: 'jobview', query: { searchQuery: searchQuery.value } })
}
</script>

<style scoped>
@keyframes pulseSlow {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.2;
  }
}

.animate-pulseSlow {
  animation: pulseSlow 2s infinite;
}
</style>
