<template>
  <div class="relative">
    <SidebarApp
      class="fixed left-0 top-0 z-40 min-h-screen shrink-0"
      :class="{
        // Desktop
        'w-56 md:block': !isMobileDevice && !isTabletDevice && open,
        'w-16 md:block': !isMobileDevice && !isTabletDevice && !open,
        // Mobile & tablet
        'w-56': (isMobileDevice || isTabletDevice) && openMobile,
        hidden: (isMobileDevice || isTabletDevice) && !openMobile,
      }"
      :open="open"
      :open-mobile="openMobile"
      :is-mobile-device="isMobileDevice"
      :is-tablet-device="isTabletDevice"
      :is-landscape="isLandscape"
      ref="sidebarAppRef"
      @toggle="toggleSidebar"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useSidebar } from '@/components/ui/sidebar'
import SidebarApp from '@/layout/SidebarApp.vue'
import { useDeviceDetection } from '@/utils/useDeviceDetection'

const sidebarAppRef = ref()
const { open, openMobile, setOpen, setOpenMobile } = useSidebar()
const { isMobileDevice, isTabletDevice, isLandscape } = useDeviceDetection()

watch(
  [isMobileDevice, isTabletDevice],
  ([newIsMobile, newIsTablet]) => {
    if (newIsMobile || newIsTablet) {
      setOpen(false)
      setOpenMobile(false)
    } else {
      setOpen(true)
      setOpenMobile(false)
    }
  },
  { immediate: true },
)

const toggleSidebar = () => {
  if (isMobileDevice.value || isTabletDevice.value) {
    setOpenMobile(!openMobile.value)
    setOpen(false)
  } else {
    setOpen(!open.value)
    setOpenMobile(false)
  }
}

defineExpose({ sidebarAppRef })
</script>
