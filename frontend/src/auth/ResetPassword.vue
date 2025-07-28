<template>
  <Card class="w-3/4 p-4 dark:bg-neutral-800 bg-baseMedium">
    <form @submit.prevent="onSubmit">
      <h3>Réinitialisation du mot de passe</h3>

      <div v-if="!token" class="text-red-600">Lien invalide ou expiré</div>

      <div class="w-1/2" v-else>
        <FormField v-slot="{ componentField }" :form="form" name="new_password">
          <FormItem>
            <FormLabel>Nouveau mot de passe</FormLabel>
            <FormControl>
              <Input
                class="dark:border-mintGreen border-accentPrimary"
                type="password"
                v-bind="componentField"
                placeholder="Entrez un nouveau mot de passe"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="pt-8">
          <Button type="submit" class="w-full bg-accentPrimary dark:bg-mintGreen dark:text-black">
            Réinitialiser le mot de passe
          </Button>
        </div>

        <div v-if="submitSuccess" class="mt-4 text-green-600">
          Mot de passe réinitialisé avec succès ! Vous pouvez maintenant vous connecter.
        </div>
        <div v-if="submitError" class="mt-4 text-red-600">
          {{ submitError }}
        </div>
      </div>
    </form>
  </Card>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { useForm } from 'vee-validate';
import z from 'zod';
import { toTypedSchema } from '@vee-validate/zod';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { FormField, FormItem, FormControl, FormMessage } from '@/components/ui/form';
import FormLabel from '@/components/ui/form/FormLabel.vue';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/toast';

const { toast } = useToast();

const route = useRoute();
const token = route.query.token as string;

const submitSuccess = ref(false);
const submitError = ref<string | null>(null);

const API_URL = import.meta.env.VITE_API_URL

const formSchema = toTypedSchema(
  z.object({
    new_password: z.string().min(6, 'Le mot de passe doit contenir au moins 6 caractères'),
  })
);

const form = useForm({
  validationSchema: formSchema,
});

const onSubmit = form.handleSubmit(async (values) => {
  submitError.value = null;
  submitSuccess.value = false;

  try {
    const res = await fetch(`${API_URL}/auth/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        token,
        new_password: values.new_password,
      }),
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || 'Erreur inconnue');
    }

    submitSuccess.value = true;
    toast({
      class: 'text-green-500 bg-neutral-800',
      title: 'Mot de passe réinitialisé avec succès !',
    });

  } catch (err: any) {
    submitError.value = err.message;
    toast({
      class: 'text-red-500 bg-neutral-800',
      title: 'Erreur',
      description: err.message,
    });
  }
});
</script>
