<template>
  <main class="flex min-h-screen w-full items-stretch overflow-x-hidden text-foreground">
    <div class="flex w-full flex-col p-4 transition-all duration-300">
      <div
        v-if="!openMobile || !isDesktopDevice"
        :class="{
          'fixed top-6 z-50 ml-4 h-12 w-10 rounded-xl bg-background/70 shadow-md backdrop-blur-md transition duration-300': true,
          'left-4': isLandscape,
          'left-2': !isLandscape,
          hidden: isDesktopDevice || (openMobile && isTabletDevice),
        }"
      >
        <Button
          @click="openSidebarMobileOrTablet"
          variant="ghost"
          size="icon"
          class="h-full w-full text-foreground"
        >
          <Menu class="h-7 w-7" />
        </Button>
      </div>

      <!-- <SidebarWrapper /> -->

      <TerminalHeader class="w-4/5" @search="handleSearch" />
      <span ref="sentinelRef" class="h-[1px] w-full"></span>

      <RouterView class="h-full w-full" v-slot="{ Component }" :is-loading="jobStore.isLoading">
        <component :is="Component" />
      </RouterView>

      <div v-if="!isMobileDevice && !isTabletDevice" class="fixed right-4 top-4 mr-4">
        <ToggleMode />
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, provide, watch } from 'vue'
import { useJobStore } from '@/stores/jobStore'
import { useAuthStore } from '@/stores/authStore'
import { useSidebar } from '@/components/ui/sidebar'
import TerminalHeader from '../layout/TerminalHeader.vue'
import ToggleMode from '../layout/ToggleMode.vue'
import { Menu } from 'lucide-vue-next'
import { useDeviceDetection } from '@/utils/useDeviceDetection'

const authStore = useAuthStore()
const jobStore = useJobStore()

// search
const handleSearch = (query: string) => jobStore.setSearchQuery(query)

// Sidebar mobile
const { isMobileDevice, isLandscape, isTabletDevice, isDesktopDevice } = useDeviceDetection()

const { setOpenMobile, openMobile } = useSidebar()
const openSidebarMobileOrTablet = () => {
  if (isMobileDevice || isTabletDevice) {
    setOpenMobile(true)
  }
}

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
})

onUnmounted(() => {
  if (observer && sentinelRef.value) {
    observer.unobserve(sentinelRef.value)
  }
})

watch(
  () => authStore.currentUser?.id,
  async (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      console.log(`User changed from ${oldUserId} to ${newUserId}. Refreshing jobs and statuses...`)
      jobStore.offset = 0
      jobStore.hasMore = true
      if (!jobStore.isLoading) {
        await jobStore.fetchJobs()
      }
      await jobStore.clearAndFetchUserJobStatuses()
    }
  },
  { immediate: true },
)
</script>
