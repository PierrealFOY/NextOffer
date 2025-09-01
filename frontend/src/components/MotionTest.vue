<template>
  <div class="flex h-screen items-center justify-center bg-black">
    <div
      v-motion
      :initial="{ opacity: 1 }"
      :animate="{ opacity: [1, 0.2, 1] }"
      :transition="{ repeat: Infinity, duration: 1 }"
      class="font-arcade text-4xl text-neonBlue"
    >
      |
    </div>
  </div>
</template>
