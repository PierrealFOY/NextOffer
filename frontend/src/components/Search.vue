<template>
  <div
    @click="activateSearch"
    v-motion
    :initial="{ opacity: 1 }"
    :animate="{ opacity: [1, 0.2, 1] }"
    :transition="{ repeat: Infinity, duration: 1 }"
    :class="{ 'mt-8': isMobile }"
    class="relative flex w-3/5 cursor-pointer items-center rounded border-2 border-accentPrimary dark:border-mintGreen md:w-2/5"
  >
    <span
      v-if="!isSearchActive"
      class="animate-pulseSlow pl-1 text-accentPrimary dark:text-mintGreen"
    >
      _
    </span>

    <div class="flex items-center space-x-1">
      <input
        ref="searchInput"
        v-model="searchQuery"
        type="text"
        class="w-3/4 border-b border-accentPrimary bg-transparent p-1 px-1 text-sm text-accentPrimary focus:w-full focus:outline-none"
        placeholder="Rechercher..."
        @keyup.enter="handleSearch"
        @blur="deactivateSearch"
      />
      <button
        @click="handleSearch"
        class="justify-end text-accentPrimary transition-colors hover:text-[#FFD700]"
      >
        <Search />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from 'lucide-vue-next'
import { useSidebar } from './ui/sidebar'
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

const deactivateSearch = () => {
  if (searchQuery.value.trim() === '') {
    isSearchActive.value = false
  }
}

const handleSearch = () => {
  emit('search', searchQuery.value)
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
  animation: pulseSlow 1s infinite;
}
</style>
