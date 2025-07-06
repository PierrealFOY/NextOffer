<template>
  <div class="h-screen flex justify-center items-center bg-black">
    <div
      v-motion
      :initial="{ opacity: 1 }"
      :animate="{ opacity: [1, 0.2, 1] }"
      :transition="{ repeat: Infinity, duration: 1 }"
      class="text-neonBlue text-4xl font-arcade"
    >
      |
    </div>
  </div>
</template>

<script setup lang="ts">
// Rien à importer ici si MotionPlugin est bien installé
</script>
