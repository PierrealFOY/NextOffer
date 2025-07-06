<template>
  <div class="relative flex h-4 w-4 items-center justify-center">
    <Heart class="absolute h-full w-full text-red-500" :style="heartOutlineStyle" />

    <Heart class="absolute h-full w-full text-red-500" :style="heartFillStyle" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Heart } from 'lucide-vue-next'

const strokeDashoffset = ref(100)
const heartOutlineStyle = computed(() => ({
  strokeDasharray: '100%',
  strokeDashoffset: `${strokeDashoffset.value}%`,
  stroke: 'currentColor',
  fill: 'none',
  strokeWidth: '2',
  transition: 'stroke-dashoffset 1s ease-out',
}))

const fillOpacity = ref(0)
const heartFillStyle = computed(() => ({
  fill: 'currentColor',
  opacity: fillOpacity.value,
  transition: 'opacity 0.8s ease-in',
}))

onMounted(() => {
  setTimeout(() => {
    strokeDashoffset.value = 0
  }, 100)

  setTimeout(() => {
    fillOpacity.value = 1
  }, 900)
})
</script>
