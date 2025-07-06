<template>
  <div
    ref="dot flex flex-row"
    class="h-2 w-2 rounded-full bg-accentPrimary dark:bg-mintGreen"
  ></div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMotion } from '@vueuse/motion'

const props = defineProps<{ delay: number }>()

const dot = ref(null)

onMounted(() => {
  if (dot.value) {
    useMotion(dot, {
      initial: { opacity: 0, scale: 0.5 },
      animate: {
        opacity: 1,
        scale: 1,
        transition: {
          duration: 0.6,
          repeat: Infinity,
          repeatType: 'loop',
          ease: 'easeInOut',
          delay: props.delay,
        },
      },
    })
  }
})
</script>
