<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useRouter } from 'vue-router'
import { useToast } from '@/components/ui/toast/use-toast'
import { useSidebar } from '@/components/ui/sidebar'

const router = useRouter()
const authStore = useAuthStore()

const formSchema = toTypedSchema(
  z.object({
    username: z.string().min(2, {
      message: "Le nom d'utilisateur doit contenir au moins 2 caractères.",
    }),
    password: z.string().min(6, {
      message: 'Le mot de passe doit contenir au moins 6 caractères.',
    }),
  }),
)
const form = useForm({
  validationSchema: formSchema,
})

const { toast } = useToast()

const errorMessage = ref<string | null>(null)
const isLoading = ref(false)

const API_URL = import.meta.env.VITE_API_URL

const onSubmit = form.handleSubmit(async (values) => {
  errorMessage.value = null
  isLoading.value = true

  try {
    const response = await axios.post(
      `${API_URL}/api/auth/token`,
      new URLSearchParams({
        username: values.username,
        password: values.password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      },
    )

    const accessToken = response.data.access_token
    const userMeResponse = await axios.get(`${API_URL}/api/auth/users/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
    const userData = userMeResponse.data

    authStore.login(userData, accessToken)
    router.push('/')
    toast({
      class: 'text-green-500 bg-neutral-800',
      title: 'Vous êtes connecté !',
    })
  } catch (err) {
    console.error('Login error:', err)
    if (axios.isAxiosError(err)) {
      if (err.response && err.response.data && err.response.data.detail) {
        errorMessage.value = 'Erreur de connexion : ' + err.response.data.detail
      } else {
        errorMessage.value = 'Erreur de connexion : ' + err.message
      }
    } else if (err instanceof Error) {
      errorMessage.value = 'Une erreur inattendue est survenue : ' + err.message
    } else {
      errorMessage.value = 'Une erreur inconnue est survenue.'
    }
  } finally {
    isLoading.value = false
  }
})
const { isMobile } = useSidebar()
</script>

<template>
  <div class="mt-16 flex min-h-screen justify-center">
    <Card
      :class="{ 'mx-2 w-[100%]': isMobile, 'w-2/3': !isMobile }"
      class="h-fit border border-accentPrimary shadow-br-light dark:border-mintGreen dark:bg-neutral-800 dark:shadow-br-dark"
    >
      <CardHeader>
        <CardTitle class="text-center text-2xl font-bold">Connexion</CardTitle>
        <CardDescription class="text-center">Connectez-vous à votre compte</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit="onSubmit" class="space-y-6">
          <FormField v-slot="{ componentField }" name="username">
            <FormItem>
              <FormLabel>Nom d'utilisateur</FormLabel>
              <FormControl>
                <Input
                  class="dark:border-mintGreen"
                  type="text"
                  placeholder="johndoe"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="password">
            <FormItem>
              <FormLabel>Mot de passe</FormLabel>
              <FormControl>
                <Input
                  class="dark:border-mintGreen"
                  type="password"
                  placeholder="••••••••"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <div class="pt-8">
            <Button type="submit" class="w-full dark:bg-mintGreen" :disabled="isLoading">
              <span v-if="isLoading">Connexion en cours...</span>
              <span v-else>Se connecter</span>
            </Button>
          </div>

          <p v-if="errorMessage" class="mt-4 text-center text-sm text-red-500">
            {{ errorMessage }}
          </p>

          <p class="mt-4 text-end text-sm">
            <router-link class="text-blue-500 underline" to="forgot"
              >Mot de passe oublié ?</router-link
            >
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
