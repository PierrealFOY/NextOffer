<script setup lang="ts">
import { ref } from 'vue'
import { useMotion } from '@vueuse/motion'
import { Search, Star, ShieldCheck, User, Telescope } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import TextShadow from '../../src/animations/TextShadow.vue'
import { useRouter } from 'vue-router'
import { useSidebar } from '@/components/ui/sidebar'

const router = useRouter()

const heroTitle = ref<HTMLElement>()
const heroSubtitle = ref<HTMLElement>()
const heroCta = ref<HTMLElement>()

useMotion(heroTitle, {
  initial: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0, transition: { duration: 600, delay: 200 } },
})

useMotion(heroSubtitle, {
  initial: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0, transition: { duration: 600, delay: 400 } },
})

useMotion(heroCta, {
  initial: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0, transition: { duration: 600, delay: 600 } },
})

const featuresRef = ref<HTMLElement>()
useMotion(featuresRef, {
  initial: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 500 } },
})

const applyStaggeredAnimations = (elements: HTMLElement[]) => {
  elements.forEach((el, i) => {
    useMotion(el, {
      initial: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0, transition: { duration: 400, delay: i * 150 } },
    })
  })
}

setTimeout(() => {
  if (featuresRef.value) {
    const featureItems = Array.from(featuresRef.value.children) as HTMLElement[]
    applyStaggeredAnimations(featureItems)
  }
}, 800)

const goToJobs = () => {
  router.push('/offers')
}
const { isMobile } = useSidebar()
</script>

<template>
  <div
    :class="{
      'w-full max-w-[80vw] overflow-y-auto overflow-x-hidden px-6': isMobile,
    }"
    class="flex w-full flex-col bg-background text-foreground md:-mx-36"
  >
    <section
      class="relative flex flex-col items-center justify-center px-2 py-20 text-center md:px-4 md:py-32"
    >
      <div
        class="animate-pulse-slow absolute inset-0 from-primary/10 to-secondary/10 opacity-30"
      ></div>

      <div class="relative w-full md:w-4/5">
        <h1 ref="heroTitle" class="mb-4 flex text-center text-2xl font-extrabold md:text-5xl">
          <TextShadow v-if="!isMobile" class="leading-6">Trouvez l'emploi idéal</TextShadow>
          <p v-else-if="isMobile" class="pl-8 leading-10">Trouvez l'emploi idéal</p>
        </h1>
        <p ref="heroSubtitle" class="mb-8 text-lg text-muted-foreground md:text-xl">
          Accédez à des milliers d'offres d'emploi en présentiel, en télétravail ou en hybride,
          filtrées pour vous.
        </p>
        <Button
          ref="heroCta"
          @click="goToJobs"
          class="sm:4/5 rounded-md px-3 py-4 shadow-lg transition-all duration-300 hover:shadow-xl dark:bg-mintGreen dark:text-black md:px-8 md:text-lg"
        >
          Explorer les offres d'emploi <Telescope class="h-5 w-5 md:ml-2" />
        </Button>
      </div>
    </section>

    <section class="px-4 py-16 text-center md:py-24">
      <h2 class="te mb-12 text-3xl font-bold text-primary dark:text-mintGreen md:text-4xl">
        Pourquoi choisir NextOffer ?
      </h2>
      <div ref="featuresRef" class="mx-auto grid max-w-4xl grid-cols-1 gap-8 md:grid-cols-3">
        <div
          class="flex transform flex-col items-center rounded-lg border border-border bg-background p-6 transition-transform duration-300 hover:scale-105 hover:shadow-br-light"
        >
          <Search class="mb-4 h-12 w-12 text-accentPrimary dark:text-mintGreen" />
          <h3 class="mb-2 text-xl font-semibold">Offres Filtrées</h3>
          <p class="text-muted-foreground">
            Accédez uniquement aux emplois 100% à distance et pertinents pour vos compétences.
          </p>
        </div>
        <div
          class="flex transform flex-col items-center rounded-lg border border-border bg-background p-6 shadow-md transition-transform duration-300 hover:scale-105 hover:shadow-br-light"
        >
          <Star class="mb-4 h-12 w-12 text-accentPrimary dark:text-mintGreen" />
          <h3 class="mb-2 text-xl font-semibold">Expérience Utilisateur Intuitive</h3>
          <p class="text-muted-foreground">
            Naviguez facilement, sauvegardez vos favoris et suivez vos candidatures.
          </p>
        </div>
        <div
          class="flex transform flex-col items-center rounded-lg border border-border bg-background p-6 shadow-md transition-transform duration-300 hover:scale-105 hover:shadow-br-light"
        >
          <ShieldCheck class="mb-4 h-12 w-12 text-accentPrimary dark:text-mintGreen" />
          <h3 class="mb-2 text-xl font-semibold">Sécurité et Fiabilité</h3>
          <p class="text-muted-foreground">
            Des offres vérifiées pour une recherche d'emploi en toute confiance.
          </p>
        </div>
      </div>
    </section>

    <section class="bg-background px-4 py-16 text-center">
      <h2 class="mb-6 text-3xl font-bold text-primary dark:text-mintGreen md:text-4xl">
        L'aggrégateur des offres d'emploi
      </h2>
      <Button
        @click="goToJobs"
        size="lg"
        class="px-8 py-4 text-lg text-black shadow-lg transition-all duration-300 hover:shadow-xl dark:bg-mintGreen"
      >
        Voir toutes les offres <User class="ml-2 h-5 w-5" />
      </Button>
    </section>
  </div>
</template>

<style>
@keyframes pulse-slow {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}
.animate-pulse-slow {
  animation: pulse-slow 6s infinite ease-in-out;
}

@keyframes blob {
  0% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0, 0) scale(1);
  }
}
.animate-blob {
  animation: blob 8s infinite ease-in-out;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
