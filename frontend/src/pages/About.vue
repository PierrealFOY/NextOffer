<template>
  <Motion
    :initial="{ opacity: 0, y: 20 }"
    :enter="{ opacity: 1, y: 0 }"
    transition="ease-in-out"
    class="mx-auto w-full px-2 py-16 text-center md:px-4"
  >
    <div
      class="fixed right-1/4 top-8 h-28 w-28 items-center justify-center overflow-hidden rounded-[41%_59%_64%_36%_/_40%_25%_75%_60%] bg-gray-200 shadow-xl md:h-48 md:w-48 lg:flex"
    >
      <img src="../assets/photo-profil.png" alt="Image" class="h-full w-full object-cover" />
    </div>

    <div
      :class="[
        '-top-26 pointer-events-none absolute z-0 rotate-6 rounded-[6%_64%_42%_34%_/_48%_27%_42%_65%] bg-mintGreen opacity-20 md:opacity-40',
        open ? 'left-[-5rem] w-[50vw] md:w-[55vw]' : 'left-0 w-full',
      ]"
      class="md:h-50 h-40"
    ></div>

    <h1 class="mt-28 text-4xl font-extrabold text-mintGreen md:text-5xl">À propos</h1>

    <div class="mx-auto mt-6 max-w-4xl text-base leading-relaxed text-neutral-300 md:text-xl">
      <p>
        NextOffer est un site web qui récupère des offres d'emplois via 2 APIs publiques :
        <span class="font-semibold italic">France Travail</span> et
        <span class="font-semibold italic">Remotive</span>. Ce projet a été réalisé avec ❤️ par moi,
        un développeur full-stack passionné d’UX et backend.
      </p>

      <div class="mt-16 flex flex-col items-center">
        <div class="mb-6 flex items-center">
          <SquareTerminal class="text-2xl text-mintGreen md:text-3xl" />
          <p class="ml-2 text-xl font-bold text-mintGreen md:ml-3 md:text-3xl">Stack du projet</p>
        </div>
        <div class="mt-4 grid w-full max-w-2xl grid-cols-1 gap-8 md:grid-cols-2">
          <div
            class="rounded-lg border border-mintGreen bg-neutral-800 p-6 shadow-lg transition-all duration-300 hover:shadow-mintGreen/40"
          >
            <h3 class="mb-4 text-xl font-semibold text-mintGreen md:text-2xl">Frontend</h3>
            <ul class="list-inside list-none space-y-2 text-base text-neutral-300">
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
            <h3 class="mb-4 text-xl font-semibold text-mintGreen md:text-2xl">Backend</h3>
            <ul class="list-inside list-none space-y-2 text-base text-neutral-300">
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

    <div
      class="absolute bottom-[-2rem] left-1/2 flex h-32 w-[90%] -translate-x-1/2 rotate-3 transform items-center overflow-hidden rounded-[89%_11%_76%_24%_/_50%_23%_25%_20%] bg-mintGreen opacity-20 md:h-48 md:opacity-30"
    ></div>

    <div class="mx-auto mt-20 flex w-full flex-col items-center space-y-6 text-base md:text-lg">
      <div class="mx-auto flex max-w-3xl justify-center">
        <p class="leading-relaxed text-neutral-300">
          Si vous souhaitez prendre contact, je me ferais un plaisir de discuter avec vous. Vous
          trouverez ci-dessous les différents liens pour me contacter. Bonne journée ! ☀️
        </p>
      </div>
      <div class="flex flex-col items-center space-y-4 md:flex-row md:space-x-8 md:space-y-0">
        <a
          :href="githubUrl"
          target="_blank"
          class="hover:text-lightMintGreen flex items-center space-x-2 text-mintGreen transition-colors duration-300 hover:underline"
        >
          <Github class="text-xl md:text-2xl" />
          <span>GitHub</span>
        </a>
        <p class="hidden text-xl font-light text-neutral-500 md:block">|</p>
        <a
          :href="linkedinUrl"
          target="_blank"
          class="hover:text-lightMintGreen flex items-center space-x-2 text-mintGreen transition-colors duration-300 hover:underline"
        >
          <Linkedin class="text-xl md:text-2xl" />
          <span>LinkedIn</span>
        </a>
        <p class="hidden text-xl font-light text-neutral-500 md:block">|</p>
        <a
          :href="mailto"
          target="_blank"
          class="hover:text-lightMintGreen flex items-center space-x-2 text-mintGreen transition-colors duration-300 hover:underline"
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
import { useSidebar } from '@/components/ui/sidebar'
import GreenIconChecked from '@/components/icons/GreenIconChecked.vue'
const githubUrl = 'https://github.com/PierrealFOY'
const linkedinUrl = 'https://www.linkedin.com/in/pierre-alexis-foy/'

const mailto = ref('#')
const user = 'pierre.alexis.56'
const domain = 'gmail.com'

const { open } = useSidebar()

onMounted(() => {
  mailto.value = `mailto:${user}@${domain}`
})
</script>
