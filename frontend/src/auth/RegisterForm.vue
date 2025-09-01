<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { ref } from 'vue'
import axios from 'axios'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useSidebar } from '@/components/ui/sidebar'
import { toast } from '@/components/ui/toast'

const API_URL = import.meta.env.VITE_API_URL

const formSchema = toTypedSchema(
  z
    .object({
      username: z.string().min(2, {
        message: "Le nom d'utilisateur doit contenir au moins 2 caractères.",
      }),
      email: z.string().email({
        message: 'Veuillez saisir une adresse email valide.',
      }),
      password: z.string().min(6, {
        message: 'Le mot de passe doit contenir au moins 6 caractères.',
      }),
      confirmPassword: z.string().min(6, {
        // Add a confirmation password field
        message: 'Veuillez confirmer votre mot de passe.',
      }),
    })
    .refine((data) => data.password === data.confirmPassword, {
      message: 'Les mots de passe ne correspondent pas.',
      path: ['confirmPassword'],
    }),
)

const form = useForm({
  validationSchema: formSchema,
})

const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const isLoading = ref(false)

const onSubmit = form.handleSubmit(async (values) => {
  errorMessage.value = null
  successMessage.value = null
  isLoading.value = true

  try {
    await axios.post(`${API_URL}/api/auth/register`, {
      username: values.username,
      email: values.email,
      password: values.password,
    })

    toast({
      class: 'text-green-500 bg-neutral-800',
      title: 'Inscription réussie ! Vous pouvez maintenant vous connecter !',
    })
    form.resetForm()
  } catch (err) {
    console.error('Registration error:', err)
    if (axios.isAxiosError(err)) {
      errorMessage.value = "Erreur d'inscription : " + (err.response?.data?.detail || err.message)
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
  <div class="flex min-h-screen flex-col items-center justify-start pb-16">
    <Card
      :class="{ '-ml-4 mb-20 mt-16 w-[95%]': isMobile, 'mt-20 w-2/3': !isMobile }"
      class="h-fit border border-accentPrimary shadow-br-light dark:border-mintGreen dark:bg-neutral-800 dark:shadow-br-dark"
    >
      <CardHeader>
        <CardTitle class="text-center text-2xl font-bold">Inscription</CardTitle>
        <CardDescription class="text-center">Créez votre compte</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit="onSubmit" class="space-y-6">
          <FormField v-slot="{ componentField }" name="username">
            <FormItem>
              <FormLabel>Nom d'utilisateur</FormLabel>
              <FormControl>
                <Input
                  class="border-accentPrimary dark:border-mintGreen"
                  type="text"
                  placeholder="johndoe"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="email">
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  class="border-accentPrimary dark:border-mintGreen"
                  type="email"
                  placeholder="john.doe@example.com"
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
                  class="border-accentPrimary dark:border-mintGreen"
                  type="password"
                  placeholder="••••••••"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="confirmPassword">
            <FormItem>
              <FormLabel>Confirmer le mot de passe</FormLabel>
              <FormControl>
                <Input
                  class="border-accentPrimary dark:border-mintGreen"
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
              <span v-if="isLoading">Inscription en cours...</span>
              <span v-else>S'inscrire</span>
            </Button>
          </div>

          <p v-if="successMessage" class="mt-4 text-center text-sm text-green-500">
            {{ successMessage }}
          </p>
          <p v-if="errorMessage" class="mt-4 text-center text-sm text-red-500">
            {{ errorMessage }}
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
