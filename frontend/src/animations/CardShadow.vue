<script setup lang="ts">
import { computed } from 'vue'
import { useWindowScroll } from '@vueuse/core'

const cards = [
  {
    icon: 'Search',
    title: 'Offres Filtrées',
    text: 'Accédez uniquement aux emplois 100% à distance et pertinents pour vos compétences.',
  },
  {
    icon: 'Star',
    title: 'Expérience Utilisateur Intuitive',
    text: 'Naviguez facilement, sauvegardez vos favoris et suivez vos candidatures.',
  },
  {
    icon: 'ShieldCheck',
    title: 'Sécurité et Fiabilité',
    text: "Des offres vérifiées pour une recherche d'emploi en toute confiance.",
  },
]

const { y: scrollY } = useWindowScroll()

const getBoxShadow = computed(() => {
  const maxIntensity = 30
  const intensity = Math.min(maxIntensity, scrollY.value / 10)

  return `0 0 ${intensity}px rgba(138, 154, 91, 0.6)`
})
</script>

<template>
  <div ref="featuresRef" class="mx-auto grid max-w-6xl grid-cols-1 gap-8 md:grid-cols-3">
    <div
      v-for="(card, index) in cards"
      :key="index"
      class="flex transform flex-col items-center rounded-lg border border-border bg-background p-6 transition-transform duration-300 hover:scale-105"
      :style="{ boxShadow: getBoxShadow }"
    >
      <component :is="card.icon" class="mb-4 h-12 w-12 text-accentPrimary dark:text-mintGreen" />
      <h3 class="mb-2 text-xl font-semibold">{{ card.title }}</h3>
      <p class="text-muted-foreground">{{ card.text }}</p>
    </div>
  </div>
</template>
