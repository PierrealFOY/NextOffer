<script setup lang="ts">
import { BadgeCheck, ChevronsUpDown, LogOut } from 'lucide-vue-next'

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar'
import type { User } from '@/types/User'
import { useAuthStore } from '@/stores/authStore'
import { computed } from 'vue'
import Button from '@/components/ui/button/Button.vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
  user: User
}>()
const authStore = useAuthStore()
const router = useRouter()
const currentUser = computed(() => authStore.currentUser)

const avatarFallbackName = currentUser.value?.username.charAt(0).toLocaleUpperCase()
const { isMobile } = useSidebar()
const goToAccount = () => {
  router.push('/account')
}
</script>

<template>
  <SidebarMenu>
    <SidebarMenuItem>
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <SidebarMenuButton
            size="lg"
            class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
          >
            <Avatar class="h-8 w-8 rounded-lg">
              <AvatarImage :src="user.avatar" :alt="user.username" />
              <AvatarFallback class="rounded-lg">
                {{ avatarFallbackName }}
              </AvatarFallback>
            </Avatar>
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">{{ user.firstname }}</span>
              <span class="truncate text-xs">{{ user.email }}</span>
            </div>
            <ChevronsUpDown class="ml-auto size-4" />
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          class="dar:border-mintGreen w-[--reka-dropdown-menu-trigger-width] min-w-56 rounded-lg border border-accentPrimary bg-gray-200 dark:border-mintGreen dark:bg-neutral-800"
          :side="isMobile ? 'bottom' : 'right'"
          align="end"
          :side-offset="4"
        >
          <DropdownMenuLabel class="p-0 font-normal">
            <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
              <Avatar class="h-8 w-8 rounded-lg">
                <AvatarImage :src="user.avatar" :alt="user.username" />
                <AvatarFallback class="rounded-lg"> CN </AvatarFallback>
              </Avatar>
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{{ user.username }}</span>
                <span class="truncate text-xs">{{ user.email }}</span>
              </div>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator class="bg-accentPrimary dark:bg-mintGreen" />
          <DropdownMenuGroup>
            <DropdownMenuItem class="cursor-pointer" @click="goToAccount">
              <Button variant="ghost" class="hover:bg-gray-300 dark:hover:bg-neutral-900">
                <BadgeCheck />
                Account
              </Button>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator class="bg-accentPrimary dark:bg-mintGreen" />
          <DropdownMenuItem>
            <Button
              variant="destructive"
              class="bg-red-400 p-2 font-bold dark:bg-red-600 dark:text-white dark:hover:bg-red-400"
              @click="authStore.logout"
            >
              <LogOut />
              Déconnexion
            </Button>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenuItem>
  </SidebarMenu>
</template>
