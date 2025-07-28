<template>
  <SidebarProvider v-slot="{ open, isMobile, openMobile }">
    <div class="flex h-screen w-screen transition-all duration-300">
      <Toaster />

      <SidebarWrapper
        :class="{ 'w-64': open, 'w-16': !open, hidden: isMobile && !openMobile }"
        class="fixed left-0 top-0 z-30 h-full transition-all duration-300"
      />

      <MainLayout
        :class="{ 'p-2': isMobile && !openMobile }"
        class="flex-1 transition-all duration-300"
      />
    </div>
  </SidebarProvider>
</template>

<script setup lang="ts">
import SidebarProvider from './components/ui/sidebar/SidebarProvider.vue'
import Toaster from '@/components/ui/toast/Toaster.vue'
import MainLayout from './layout/MainLayout.vue'
import SidebarWrapper from './layout/SidebarWrapper.vue'
</script>
