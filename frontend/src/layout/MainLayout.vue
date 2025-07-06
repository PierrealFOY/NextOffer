<template>
  <main
    class="flex min-h-screen w-full items-center justify-center overflow-y-auto overflow-x-hidden text-foreground"
  >
    <div class="flex w-full flex-col p-4 transition-all duration-300">
      <div
        v-show="!openMobile && isMobile"
        class="fixed top-6 z-50 h-12 w-10 rounded-xl bg-background/70 shadow-md backdrop-blur-md transition duration-300"
      >
        <Button
          @click="openSidebarMobile"
          variant="ghost"
          size="icon"
          class="h-full w-full text-foreground"
        >
          <Menu class="h-7 w-7" />
        </Button>
      </div>

      <TerminalHeader @search="handleSearch" />
      <span ref="sentinelRef" class="h-[1px] w-full"></span>

      <RouterView
        class="h-full w-full"
        v-slot="{ Component }"
        :jobs="filteredJobs"
        :is-loading="store.isLoading"
        @update:liked="handleLikedUpdate"
        @update:seen="handleSeenJobUpdate"
        @update:applied="handleAppliedJobUpdate"
      >
        <component :is="Component" />
      </RouterView>

      <div v-if="!isMobile" class="fixed right-4 top-4">
        <ToggleMode />
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, provide } from 'vue'
import { useJobStore } from '@/stores/jobStore'
import { useAuthStore } from '@/stores/authStore'
import { useSidebar } from '@/components/ui/sidebar'
import TerminalHeader from '../layout/TerminalHeader.vue'
import ToggleMode from '../layout/ToggleMode.vue'
import { Menu } from 'lucide-vue-next'

const authStore = useAuthStore()
const store = useJobStore()

// search
const searchQuery = ref('')
const filteredJobs = computed(() => store.filteredJobs(searchQuery.value))
const handleSearch = (query: string) => (searchQuery.value = query)

// Liked / Seen / Applied
const handleLikedUpdate = (jobId: string) => {
  const isAlreadyLiked = store.isJobAlreadyLiked(jobId)
  store.toggleLikeJob(jobId, isAlreadyLiked)
}
const handleSeenJobUpdate = (jobId: string) => store.updateSeenJobs(jobId)
const handleAppliedJobUpdate = (jobId: string) => store.updateAppliedJobs(jobId)

// Sidebar mobile
const { isMobile, setOpenMobile, openMobile } = useSidebar()
const openSidebarMobile = () => setOpenMobile(true)

// IntersectionObserver
const isHeaderVisible = ref(true)
provide('isHeaderVisible', isHeaderVisible)

const sentinelRef = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

onMounted(() => {
  observer = new IntersectionObserver(
    ([entry]) => {
      isHeaderVisible.value = entry.isIntersecting
    },
    { threshold: 0.1 },
  )

  if (sentinelRef.value) {
    observer.observe(sentinelRef.value)
  }
})

onMounted(async () => {
  await authStore.initializeAuth()
  if (store.jobs.length === 0 && !store.isLoading) {
    store.fetchJobs()
  }
})

onUnmounted(() => {
  if (observer && sentinelRef.value) {
    observer.unobserve(sentinelRef.value)
  }
})
</script>
