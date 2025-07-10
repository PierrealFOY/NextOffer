<template>
  <div class="relative">
    <SidebarApp
      v-if="!isMobile"
      class="fixed left-0 top-0 z-40 min-h-screen shrink-0 md:block"
      :class="{ 'w-56': open, 'w-16': !open }"
      :open="open"
      :open-mobile="openMobile"
      ref="sidebarAppRef"
      @toggle="toggleSidebar"
    />

    <SidebarApp
      v-if="isMobile"
      :class="{ 'hidden w-0': !openMobile, 'w-64': openMobile }"
      class="fixed inset-y-0 left-0 z-40 h-full overflow-y-auto md:hidden"
      :open="open"
      :open-mobile="openMobile"
      ref="sidebarAppRef"
      @toggle="toggleSidebar"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSidebar } from '@/components/ui/sidebar'
import SidebarApp from '@/layout/SidebarApp.vue'

const sidebarAppRef = ref()
const { open, openMobile, setOpen, setOpenMobile, isMobile } = useSidebar()

onMounted(() => {
  if (isMobile.value) {
    setOpen(false)
  } else {
    setOpenMobile(false)
  }
  openMobile.value = false
})

const toggleSidebar = () => {
  if (isMobile.value) {
    setOpenMobile(!openMobile.value)
    setOpen(false)
  } else {
    setOpen(!open.value)
    setOpenMobile(false)
  }
}

defineExpose({ sidebarAppRef })
</script>
