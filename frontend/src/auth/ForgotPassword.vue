<template>
  <div>
    <Card class="w-3/4 p-4">
      <form @submit="onSubmit">
        <h3>Mot de passe oublié</h3>

        <div class="w-1/2">
          <FormField v-slot="{ componentField }" :form="form" name="email">
            <FormItem>
              <FormLabel>Email</FormLabel>
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

          <div class="pt-8">
            <Button type="submit" class="w-full bg-accentPrimary dark:bg-mintGreen dark:text-black">
              <span>Envoyer la demande</span>
            </Button>
          </div>

          <div v-if="submitSuccess" class="mt-4 text-green-600">
            Un email de réinitialisation a été envoyé à votre adresse. Veuillez vérifier votre boîte
            de réception (et vos spams !).
          </div>
          <div v-if="submitError" class="mt-4 text-red-600">
            {{ submitError }}
          </div>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card } from '@/components/ui/card'
import { FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form'
import FormLabel from '@/components/ui/form/FormLabel.vue'
import { Input } from '@/components/ui/input'
import { useToast } from '@/components/ui/toast'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ref } from 'vue'
import z from 'zod'

const { toast } = useToast()

const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref<string | null>(null)

const formSchema = toTypedSchema(
  z.object({
    email: z.string().email("Format d'email invalide").min(1, "L'email est requis"),
  }),
)

const form = useForm({
  validationSchema: formSchema,
})

const onSubmit = form.handleSubmit(async (values) => {
  isSubmitting.value = true
  submitSuccess.value = false
  submitError.value = null

  try {
    const response = await fetch('http://localhost:8000/api/auth/forgot-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: values.email }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || "Une erreur est survenue lors de l'envoi de la demande")
    }

    submitSuccess.value = true
    toast({
      class: 'text-green-500 bg-neutral-800',
      title: `Demande de réinitialisation envoyée pour: ${values.email}`,
    })
  } catch (error: any) {
    submitError.value = error.message
    toast({
      class: 'text-red-500 bg-neutral-800',
      title: `Erreur lors de la soumission: ${error}`,
    })
  } finally {
    isSubmitting.value = false
  }
})
</script>
