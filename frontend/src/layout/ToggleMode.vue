<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import { MoonIcon, SunIcon } from 'lucide-vue-next'
import { useGlobalColorMode } from '@/utils/useGlobalColorMode'
import { useSidebar } from '@/components/ui/sidebar'

const mode = useGlobalColorMode()

if (mode.value === 'auto') {
  const isDarkSystem = window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark', isDarkSystem)
}
const { isMobile } = useSidebar()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button
        :class="{ 'border-none bg-gray-300 dark:bg-neutral-900': isMobile }"
        class="dark:border-mintGreen"
        variant="outline"
      >
        <Transition name="icon-fade" mode="out-in">
          <MoonIcon
            v-if="mode === 'light'"
            key="moon"
            class="h-[1.2rem] w-[1.2rem] text-accentPrimary dark:text-mintGreen"
          />
          <SunIcon
            v-else
            key="sun"
            class="-m-2 h-[1.2rem] w-[1.2rem] text-mintGreen dark:text-mintGreen"
          />
        </Transition>
        <span class="sr-only">Toggle theme</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="mode = 'light'"> Light </DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'dark'"> Dark </DropdownMenuItem>
      <DropdownMenuItem @click="mode = 'auto'"> System </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<style>
.icon-fade-enter-active,
.icon-fade-leave-active {
  transition:
    transform 0.3s ease-in-out,
    opacity 0.3s ease-in-out;
}

.icon-fade-enter-from {
  opacity: 0;
  transform: rotate(-90deg) scale(0);
}
.icon-fade-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0);
}

.icon-fade-enter-to,
.icon-fade-leave-from {
  opacity: 1;
  transform: rotate(0deg) scale(1);
}
</style>
