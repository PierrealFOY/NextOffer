<template>
  <div
    :class="{ 'w-[62%]': !isMobile, 'h-1/2 w-full': isMobile }"
    class="mx-auto my-10 flex flex-col rounded-md border border-accentPrimary bg-gray-200 px-4 py-10 shadow-br-light dark:border-mintGreen dark:bg-neutral-800 dark:shadow-br-dark"
  >
    <h1 :class="{ 'text-3xl': !isMobile, 'text-xl': isMobile }" class="mb-6 font-semibold">
      Mon compte
    </h1>

    <div
      v-if="isLoggedIn && currentUser"
      :class="{ 'text-lg': !isMobile }"
      class="rounded-lg p-6 shadow-md"
    >
      <p><strong>Nom d'utilisateur :</strong> {{ currentUser.username }}</p>
      <p><strong>Email :</strong> {{ currentUser.email }}</p>

      <div class="mt-6">
        <button @click="logout" class="rounded bg-red-500 px-4 py-2 font-semibold hover:bg-red-600">
          Se déconnecter
        </button>
      </div>
    </div>

    <div v-else class="text-center text-gray-600">
      <p>Vous devez être connecté pour accéder à cette page.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSidebar } from '@/components/ui/sidebar'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const { isMobile } = useSidebar()

const authStore = useAuthStore()
const router = useRouter()

const { currentUser, isLoggedIn } = authStore

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
