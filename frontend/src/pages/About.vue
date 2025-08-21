<template>
  <Motion
    :initial="{ opacity: 0, y: 20 }"
    :enter="{ opacity: 1, y: 0 }"
    transition="ease-in-out"
    class="relative mx-auto w-full py-16"
  >
    <div class="mt-10 flex flex-col items-end justify-end">
      <div class="flex w-full justify-center md:mt-0 md:w-1/2 md:justify-start">
        <div
          class="z-10 h-40 w-40 overflow-hidden rounded-[41%_59%_64%_36%_/_40%_25%_75%_60%] bg-gray-200 shadow-xl hover:shadow-br-light hover:dark:shadow-br-dark md:h-52 md:w-52"
        >
          <img src="../assets/photo-profil.png" alt="Image" class="h-full w-full object-cover" />
        </div>
      </div>

      <div class="z-10 w-4/5 justify-center self-center">
        <h1 class="text-4xl font-extrabold text-accentPrimary dark:text-mintGreen md:text-5xl">
          À propos
        </h1>
        <p class="mx-auto mt-6 p-1 text-base leading-relaxed md:mx-0 md:text-xl">
          NextOffer est un site web qui récupère des offres d'emplois via 2 APIs publiques :
          <span class="font-semibold italic">France Travail</span> et
          <span class="font-semibold italic">Remotive</span>. Ce projet a été réalisé avec ❤️ par
          moi, un développeur full-stack passionné d’UX et backend.
        </p>
      </div>
    </div>

    <div class="mx-auto mt-16 max-w-4xl text-base leading-relaxed text-neutral-300 md:text-xl">
      <div class="mt-16 flex flex-col items-center">
        <div class="mb-6 flex items-center">
          <SquareTerminal class="text-2xl text-accentPrimary dark:text-mintGreen md:text-3xl" />
          <p
            class="ml-2 text-xl font-bold text-accentPrimary dark:text-mintGreen md:ml-3 md:text-3xl"
          >
            Stack du projet
          </p>
        </div>
        <div
          class="mt-4 grid w-full max-w-2xl grid-cols-1 gap-8 text-accentPrimary dark:text-mintGreen md:grid-cols-2"
        >
          <div
            class="rounded-lg border border-accentPrimary bg-gray-300 p-6 text-accentPrimary shadow-lg transition-all duration-300 hover:shadow-mintGreen/40 dark:border-mintGreen dark:bg-neutral-800 dark:text-mintGreen"
          >
            <h3
              class="mb-4 text-xl font-semibold text-accentPrimary dark:text-mintGreen md:text-2xl"
            >
              Frontend
            </h3>
            <ul
              class="list-inside list-none space-y-2 text-base text-accentPrimary dark:text-mintGreen"
            >
              <li class="flex items-center">
                <GreenIconChecked />
                Vue.js
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                TailwindCSS
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                TypeScript
              </li>
            </ul>
          </div>
          <div>
            <h3
              class="mb-4 text-xl font-semibold text-accentPrimary dark:text-mintGreen md:text-2xl"
            >
              Backend
            </h3>
            <ul
              class="list-inside list-none space-y-2 text-base text-accentPrimary dark:text-mintGreen"
            >
              <li class="flex items-center">
                <GreenIconChecked />
                Node.js
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                Python
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                Pydantic
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                FastAPI
              </li>
              <li class="flex items-center">
                <GreenIconChecked />
                PostgreSQL
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="mx-auto mt-20 flex w-full flex-col items-center space-y-6 text-base md:text-lg">
      <div class="mx-auto flex max-w-3xl justify-center">
        <p class="leading-relaxed dark:text-neutral-300">
          Si vous souhaitez prendre contact, je me ferais un plaisir de discuter avec vous. Vous
          trouverez ci-dessous les différents liens pour me contacter. Bonne journée ☀️
        </p>
      </div>
      <div class="flex flex-col items-center space-y-4 pb-10 md:flex-row md:space-x-8 md:space-y-0">
        <a
          :href="githubUrl"
          target="_blank"
          class="flex items-center space-x-2 text-accentPrimary transition-colors duration-300 hover:underline dark:text-mintGreen"
        >
          <Github class="text-xl md:text-2xl" />
          <span>GitHub</span>
        </a>
        <p class="hidden text-xl font-light text-neutral-500 md:block">|</p>
        <a
          :href="linkedinUrl"
          target="_blank"
          class="flex items-center space-x-2 text-accentPrimary transition-colors duration-300 hover:underline dark:text-mintGreen"
        >
          <Linkedin class="text-xl md:text-2xl" />
          <span>LinkedIn</span>
        </a>
        <p class="hidden text-xl font-light text-neutral-500 md:block">|</p>
        <a
          :href="mailto"
          target="_blank"
          class="flex items-center space-x-2 text-accentPrimary transition-colors duration-300 hover:underline dark:text-mintGreen"
        >
          <Mail class="text-xl md:text-2xl" />
          <span>Mail</span>
        </a>
      </div>
    </div>
  </Motion>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { SquareTerminal, Github, Linkedin, Mail } from 'lucide-vue-next'
import GreenIconChecked from '@/components/icons/GreenIconChecked.vue'
const githubUrl = 'https://github.com/PierrealFOY'
const linkedinUrl = 'https://www.linkedin.com/in/pierre-alexis-foy/'

const mailto = ref('#')
const user = 'pierre.alexis.56'
const domain = 'gmail.com'

onMounted(() => {
  mailto.value = `mailto:${user}@${domain}`
})
</script>

<style>
.rounded-custom-shape {
  border-radius: 6% 64% 42% 34% / 48% 27% 42% 65%;
}
</style>
