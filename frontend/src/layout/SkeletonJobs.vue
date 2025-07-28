<template>
  <div class="flex w-full flex-col space-y-5">
    <Skeleton class="animate-pulse-slow mt-20 h-40 w-2/3 bg-baseDark" />
    <Skeleton class="animate-pulse-slow mt-20 h-40 w-2/3 bg-baseDark" />
    <Skeleton class="animate-pulse-slow mt-20 h-40 w-2/3 bg-baseDark" />
    <Skeleton class="animate-pulse-slow mt-20 h-40 w-2/3 bg-baseDark" />
  </div>
</template>

<style>
.animate-pulse-slow {
  animation: pulse-slow 2s infinite ease-in-out;
}

@keyframes pulse-slow {
  0%,
  100% {
    opacity: 0.3;
  }
  66% {
    opacity: 0.6;
  }
  33% {
    opacity: 0.9;
  }
}
</style>
