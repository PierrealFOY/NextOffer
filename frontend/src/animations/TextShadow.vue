<template>
  <div
    ref="el"
    v-motion
    :initial="{ opacity: 0, y: 90 }"
    :enter="{ opacity: 1, y: 0, transition: { duration: 0.9 } }"
    :style="{ textShadow: currentShadow }"
    class="text-container"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useWindowScroll } from '@vueuse/core'

const el = ref(null)

const { y: scrollY } = useWindowScroll()

const makeLongShadow = (color: string, steps: number = 10): string => {
  let val = `0px 0px ${color}`
  for (let i = 1; i <= steps; i++) {
    val += `, ${i}px ${i}px ${color}`
  }
  return val
}

// Computed shadow depending on scroll
const currentShadow = computed(() => {
  const maxSteps = 30
  const minSteps = 0

  const steps = Math.min(maxSteps, Math.floor(scrollY.value / 20))
  return makeLongShadow('#8A9A5B', steps)
})
</script>

<style scoped>
.text-container {
  @apply mx-auto overflow-hidden p-10 text-left font-serif text-[3rem] font-semibold leading-[20px] text-[#EDEEE9];
  transition: text-shadow 0.3s ease;
}
</style>
