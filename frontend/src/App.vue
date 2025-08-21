<template>
  <SidebarProvider v-slot="{ open, isMobile, openMobile, isTablet }">
    <div class="flex h-screen w-screen gap-x-2 transition-all duration-300">
      <Toaster />
      <SidebarWrapper
        :class="{
          'w-48': isTablet && openMobile,
          'w-56': open && isDesktopDevice,
          'w-16': !open,
          hidden: !openMobile && (isMobile || isTablet),
        }"
        class="fixed left-0 top-0 z-30 h-full transition-all duration-300"
      />
      <MainLayout class="flex-1 transition-all duration-300" />
    </div>
  </SidebarProvider>
</template>

<script setup lang="ts">
import SidebarProvider from './components/ui/sidebar/SidebarProvider.vue'
import Toaster from '@/components/ui/toast/Toaster.vue'
import MainLayout from './layout/MainLayout.vue'
import SidebarWrapper from './layout/SidebarWrapper.vue'
import { useDeviceDetection } from './utils/useDeviceDetection'

const { isDesktopDevice } = useDeviceDetection()
</script>
