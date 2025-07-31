<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  useSidebar,
} from '@/components/ui/sidebar'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { useAuthStore } from '@/stores/authStore'
import {
  Home,
  Info,
  X,
  PanelLeftOpen,
  PanelRightOpen,
  Heart,
  HousePlus,
  LogOut,
  LogIn,
  BriefcaseBusiness,
  Eye,
  ChevronDown,
  Save,
  Send,
} from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import NavUser from './NavUser.vue'
import ToggleMode from './ToggleMode.vue'
const authStore = useAuthStore()
const isLoggedIn = computed(() => authStore.isAuthenticated)
const route = useRoute()

const user = computed(() => authStore.currentUser)

const pages = {
  main: [
    {
      title: 'Accueil',
      icon: Home,
      to: '/',
    },
    {
      title: 'À propos',
      icon: Info,
      to: '/about',
    },
  ],
  myJobs: [
    {
      title: 'Mes offres',
      to: '/myJobs',
      name: 'myJobs',
      icon: Save,
      items: [
        {
          title: 'Likées',
          icon: Heart,
          to: '/myJobs/liked',
        },
        {
          title: 'Consultées',
          icon: Eye,
          to: '/myJobs/seen',
        },
        {
          title: 'Candidatures envoyées',
          icon: Send,
          to: '/myJobs/applied',
        },
      ],
    },
  ],
  offers: [
    {
      title: 'Les offres',
      icon: BriefcaseBusiness,
      to: '/offers',
    },
  ],
}

const openCollapsible = ref<string | null>(null)

const handleCollapsibleToggle = (key: string) => {
  openCollapsible.value = openCollapsible.value === key ? null : key
}
const isLinkActive = (to: string) => {
  return route.path === to
}
const isCollapsibleGroupActive = (items: (typeof pages.myJobs)[0]['items']) => {
  return items.some((item) => route.path.startsWith(item.to))
}

const props = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
  openMobile: {
    type: Boolean,
    required: true,
  },
})

const { setOpenMobile, setOpen, isMobile } = useSidebar()

defineEmits(['toggle'])
const closeSidebar = () => {
  setOpenMobile(false)
  setOpen(false)
}

const openSidebarMobileFromParent = () => {
  if (isMobile.value) setOpenMobile(true)
}

defineExpose({
  openSidebarMobileFromParent,
})

onMounted(() => {
  if (isMobile.value) {
    setOpenMobile(false)
  }
})
</script>

<template>
  <!-- Mobile -->
  <Sidebar
    v-if="isMobile && openMobile"
    class="fixed inset-y-0 left-0 z-40 flex h-full w-64 transform flex-col border-r border-border bg-gray-300 text-accentPrimary shadow-xl transition-transform duration-300 ease-in-out dark:bg-neutral-800 dark:text-mintGreen"
    :class="{ 'translate-x-0': openMobile, '-translate-x-full': !openMobile }"
  >
    <SidebarHeader class="flex p-4">
      <div class="mb-4 flex justify-between space-x-2">
        <div
          class="-ml-2 flex items-center space-x-2 text-lg font-bold text-accentPrimary dark:ml-0 dark:text-mintGreen"
        >
          <img
            class="hidden dark:block"
            width="24"
            src="../assets/coffeeMintGreen.png"
            alt="icon"
          />
          <img
            class="block dark:hidden"
            width="24"
            src="../assets/coffeeAccentPrimary.png"
            alt="icon"
          />
          <p class="pt-2.5">NextOffer</p>
        </div>
        <Button @click="closeSidebar" variant="ghost" size="icon" class="flex text-foreground">
          <X class="h-5 w-5 text-accentPrimary dark:text-mintGreen" />
        </Button>
      </div>
      <div>
        <ToggleMode />
      </div>
    </SidebarHeader>
    <SidebarContent class="flex-1 overflow-y-auto">
      <SidebarGroup>
        <ul class="space-y-2">
          <li v-for="item in pages.main" :key="item.to">
            <RouterLink
              :to="item.to"
              @click="closeSidebar"
              class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            >
              <component :is="item.icon" class="h-5 w-5" />
              <span
                :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive(item.to) }"
              >
                {{ item.title }}
              </span>
            </RouterLink>
          </li>
          <li v-for="(group, groupIndex) in pages.myJobs" :key="`job-group-mobile-${groupIndex}`">
            <Collapsible v-model="openCollapsible" class="space-y-1">
              <CollapsibleTrigger as-child>
                <Button
                  variant="ghost"
                  class="flex w-full items-center justify-between px-4 py-2 text-left"
                  @click="handleCollapsibleToggle('my-jobs-group-mobile')"
                >
                  <div class="flex items-center space-x-3">
                    <component :is="group.icon" class="h-5 w-5" />
                    <span
                      :class="{
                        'text-green-800 underline dark:text-mintGreen': isCollapsibleGroupActive(
                          group.items,
                        ),
                      }"
                    >
                      {{ group.title }}
                    </span>
                  </div>
                  <ChevronDown
                    :class="{ 'rotate-180': openCollapsible === 'my-jobs-group-mobile' }"
                    class="h-4 w-4 transition-transform duration-200"
                  />
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent class="ml-4 mt-1 space-y-1">
                <ul class="space-y-1">
                  <li
                    v-for="(subItem, subIndex) in group.items"
                    :key="`my-jobs-sub-mobile-${subIndex}`"
                  >
                    <RouterLink
                      :to="subItem.to"
                      @click="closeSidebar"
                      class="flex items-center space-x-2 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
                      :class="{
                        'text-green-800 underline dark:text-mintGreen': isLinkActive(subItem.to),
                      }"
                    >
                      <component :is="subItem.icon" class="h-5 w-5" v-if="subItem.icon" />
                      <span>{{ subItem.title }}</span>
                    </RouterLink>
                  </li>
                </ul>
              </CollapsibleContent>
            </Collapsible>
          </li>
          <li v-for="item in pages.offers" :key="item.to + '-mobile'">
            <RouterLink
              :to="item.to"
              @click="closeSidebar"
              class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            >
              <component :is="item.icon" class="h-5 w-5" />
              <span
                :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive(item.to) }"
              >
                {{ item.title }}
              </span>
            </RouterLink>
          </li>
        </ul>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter class="mt-auto p-4">
      <div class="flex flex-col space-y-2">
        <template v-if="isLoggedIn && user !== null">
          <NavUser :user="user" />
          <a
            @click="`authStore.logout(); closeSidebar()`"
            class="flex cursor-pointer items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
          >
            <LogOut class="h-5 w-5" />
            <span>Déconnexion</span>
          </a>
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            @click="closeSidebar"
            class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive('/login') }"
          >
            <LogIn class="h-5 w-5" />
            <span>Connexion</span>
          </RouterLink>
          <RouterLink
            to="/register"
            @click="closeSidebar"
            class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive('/register') }"
          >
            <HousePlus class="h-5 w-5" />
            <span>Inscription</span>
          </RouterLink>
        </template>
      </div>
    </SidebarFooter>
  </Sidebar>

  <!-- Desktop -->
  <Sidebar
    variant="sidebar"
    collapsible="none"
    v-else-if="!isMobile"
    class="sticky z-30 flex h-screen transform flex-col border-r border-border bg-baseMedium shadow-br-light transition-all duration-300 ease-in-out dark:bg-neutral-800 dark:shadow-br-dark"
  >
    <SidebarHeader
      class="flex items-center p-4"
      :class="{ 'justify-end': open, 'justify-center': !open }"
    >
      <Button
        @click="$emit('toggle')"
        :class="{ 'self-end': open }"
        variant="ghost"
        size="icon"
        class="text-foreground"
      >
        <component :is="open ? PanelRightOpen : PanelLeftOpen" class="h-5 w-5" />
      </Button>
    </SidebarHeader>

    <SidebarContent class="flex-1 overflow-y-auto" :class="{ 'p-3': !open }">
      <SidebarGroup>
        <ul class="justify-start space-y-2">
          <li v-for="item in pages.main" :key="item.to">
            <RouterLink
              :to="item.to"
              class="flex items-center space-x-3 rounded-md py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
              :class="{
                'px-4': open,
                'justify-center': !open,
                'text-green-800 underline dark:text-mintGreen': isLinkActive(item.to),
              }"
              :title="!open ? item.title : ''"
            >
              <component :is="item.icon" class="h-5 w-5" />
              <span v-if="open">{{ item.title }}</span>
            </RouterLink>
          </li>

          <li v-for="(group, groupIndex) in pages.myJobs" :key="`job-group-desktop-${groupIndex}`">
            <Collapsible v-model="openCollapsible" class="space-y-1">
              <CollapsibleTrigger as-child v-if="open">
                <Button
                  variant="ghost"
                  class="flex w-full items-center justify-between px-4 py-2 text-left"
                  @click="handleCollapsibleToggle('my-jobs-group-desktop')"
                >
                  <div class="flex items-center space-x-3">
                    <component :is="group.icon" class="h-5 w-5" />
                    <span
                      :class="{
                        'text-green-800 underline dark:text-mintGreen': isCollapsibleGroupActive(
                          group.items,
                        ),
                      }"
                    >
                      {{ group.title }}
                    </span>
                  </div>
                  <ChevronDown
                    :class="{ 'rotate-180': openCollapsible === 'my-jobs-group-desktop' }"
                    class="h-4 w-4 transition-transform duration-200"
                  />
                </Button>
              </CollapsibleTrigger>
              <RouterLink
                v-else
                :to="group.to"
                class="flex justify-center rounded-md py-2 text-foreground transition-colors hover:bg-gray-100"
                :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive(group.to) }"
                :title="group.title"
              >
                <component :is="group.icon" class="h-5 w-5" />
              </RouterLink>

              <CollapsibleContent v-if="open" class="ml-4 mt-1 space-y-1">
                <ul class="space-y-1">
                  <li
                    v-for="(subItem, subIndex) in group.items"
                    :key="`my-jobs-sub-desktop-${subIndex}`"
                  >
                    <RouterLink
                      :to="subItem.to"
                      class="flex items-center space-x-2 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
                      :class="{
                        'text-green-800 underline dark:text-mintGreen': isLinkActive(subItem.to),
                      }"
                    >
                      <component :is="subItem.icon" class="h-5 w-5" v-if="subItem.icon" />
                      <span>{{ subItem.title }}</span>
                    </RouterLink>
                  </li>
                </ul>
              </CollapsibleContent>
            </Collapsible>
          </li>

          <li v-for="item in pages.offers" :key="item.to + '-desktop'">
            <RouterLink
              :to="item.to"
              class="flex items-center space-x-3 rounded-md py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
              :class="{
                'px-4': open,
                'justify-center': !open,
                'text-green-800 underline dark:text-mintGreen': isLinkActive(item.to),
              }"
              :title="!open ? item.title : ''"
            >
              <component :is="item.icon" class="h-5 w-5" />
              <span v-if="open">{{ item.title }}</span>
            </RouterLink>
          </li>
        </ul>
      </SidebarGroup>
    </SidebarContent>

    <SidebarFooter class="flex h-full flex-col">
      <div v-if="open" class="flex h-full w-full flex-col justify-center space-y-2">
        <template v-if="isLoggedIn && user !== null">
          <NavUser :user="user" />
          <a
            @click="authStore.logout()"
            class="flex cursor-pointer items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
          >
            <LogOut class="h-5 w-5" />
            <span>Déconnexion</span>
          </a>
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive('/login') }"
          >
            <LogIn class="h-5 w-5" />
            <span>Connexion</span>
          </RouterLink>
          <RouterLink
            to="/register"
            class="flex items-center space-x-3 rounded-md px-4 py-2 text-foreground transition-colors hover:bg-gray-100 dark:hover:bg-black"
            :class="{ 'text-green-800 underline dark:text-mintGreen': isLinkActive('/register') }"
          >
            <HousePlus class="h-5 w-5" />
            <span>Inscription</span>
          </RouterLink>
        </template>
      </div>
      <div class="flex h-full flex-col justify-center" v-else>
        <template v-if="isLoggedIn">
          <a
            @click="authStore.logout()"
            class="flex cursor-pointer justify-center rounded-md py-2 text-foreground transition-colors hover:bg-gray-100"
            title="Déconnexion"
          >
            <LogOut class="h-5 w-5" />
          </a>
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            class="flex justify-center rounded-md py-2 text-foreground transition-colors hover:bg-gray-100"
            title="Connexion"
          >
            <LogIn class="h-5 w-5" />
          </RouterLink>
          <RouterLink
            to="/register"
            class="flex justify-center rounded-md py-2 text-foreground transition-colors hover:bg-gray-100"
            title="Inscription"
          >
            <HousePlus class="h-5 w-5" />
          </RouterLink>
        </template>
      </div>
    </SidebarFooter>
  </Sidebar>
</template>
