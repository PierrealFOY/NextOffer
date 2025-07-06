<template>
  <div class="account-page max-3/4 mx-auto rounded-md py-10 px-4 dark:bg-neutral-800">
    <h1 class="text-3xl font-semibold mb-6">Mon compte</h1>

    <div v-if="isLoggedIn && currentUser" class=" shadow-md rounded-lg p-6">
      <p class="text-lg"><strong>Nom d'utilisateur :</strong> {{ currentUser.username }}</p>
      <p class="text-lg"><strong>Email :</strong> {{ currentUser.email }}</p>

      <div class="mt-6">
        <button @click="logout" class="bg-red-500 hover:bg-red-600 font-semibold px-4 py-2 rounded">
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
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const { currentUser, isLoggedIn } = authStore

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

