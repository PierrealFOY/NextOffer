<template>
  <SidebarProvider v-slot="{ open }">
    <div class="flex min-h-screen w-screen transition-all duration-300">
      <Toaster />
      <SidebarWrapper
        :class="open ? 'w-64' : 'w-16'"
        class="fixed left-0 top-0 transition-all duration-300"
      />
      <MainLayout class="flex-1 overflow-y-auto transition-all duration-300" />
    </div>
  </SidebarProvider>
</template>

<script setup lang="ts">
import SidebarProvider from './components/ui/sidebar/SidebarProvider.vue'
import Toaster from '@/components/ui/toast/Toaster.vue'
import MainLayout from './layout/MainLayout.vue'
import SidebarWrapper from './layout/SidebarWrapper.vue'
</script>
