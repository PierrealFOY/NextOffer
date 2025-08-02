<script setup lang="ts">
import { useEventListener, useMediaQuery, useVModel } from '@vueuse/core'
import { TooltipProvider } from 'reka-ui'
import { computed, type HTMLAttributes, type Ref, ref } from 'vue'
import { cn } from '@/lib/utils'
import {
  provideSidebarContext,
  SIDEBAR_COOKIE_MAX_AGE,
  SIDEBAR_COOKIE_NAME,
  SIDEBAR_KEYBOARD_SHORTCUT,
  SIDEBAR_WIDTH,
  SIDEBAR_WIDTH_ICON,
} from './utils'
import { useDeviceDetection } from '@/utils/useDeviceDetection'

const props = withDefaults(
  defineProps<{
    defaultOpen?: boolean
    open?: boolean
    class?: HTMLAttributes['class']
  }>(),
  {
    defaultOpen: true,
    open: undefined,
  },
)

const emits = defineEmits<{
  'update:open': [open: boolean]
}>()

const isMobile = useMediaQuery('(max-width: 768px)')
const openMobile = ref(false)

const { isTabletDevice } = useDeviceDetection()
const openTablet = ref(false)

const open = useVModel(props, 'open', emits, {
  defaultValue: props.defaultOpen ?? false,
  passive: (props.open === undefined) as false,
}) as Ref<boolean>

function setOpen(value: boolean) {
  open.value = value // emits('update:open', value)

  // This sets the cookie to keep the sidebar state.
  document.cookie = `${SIDEBAR_COOKIE_NAME}=${open.value}; path=/; max-age=${SIDEBAR_COOKIE_MAX_AGE}`
}

function setOpenMobile(value: boolean) {
  openMobile.value = value
}

const setOpenTablet = (value: boolean) => {
  openTablet.value = value
}

// Helper to toggle the sidebar.
const toggleSidebar = () => {
  return isMobile.value ? setOpenMobile(!openMobile.value) : setOpen(!open.value)
}

useEventListener('keydown', (event: KeyboardEvent) => {
  if (event.key === SIDEBAR_KEYBOARD_SHORTCUT && (event.metaKey || event.ctrlKey)) {
    event.preventDefault()
    toggleSidebar()
  }
})

// We add a state so that we can do data-state="expanded" or "collapsed".
// This makes it easier to style the sidebar with Tailwind classes.
const state = computed(() => (open.value ? 'expanded' : 'collapsed'))

provideSidebarContext({
  state,
  open,
  setOpen,
  isMobile,
  openMobile,
  setOpenMobile,
  openTablet,
  setOpenTablet,
  toggleSidebar,
})
</script>

<template>
  <TooltipProvider :delay-duration="0">
    <div
      :style="{
        '--sidebar-width': SIDEBAR_WIDTH,
        '--sidebar-width-icon': SIDEBAR_WIDTH_ICON,
      }"
      :class="
        cn(
          'group/sidebar-wrapper flex min-h-svh has-[[data-variant=inset]]:bg-sidebar',
          props.class,
        )
      "
      v-bind="$attrs"
    >
      <slot
        :isMobile="isMobile"
        :isTablet="isTabletDevice"
        :open="open"
        :openMobile="openMobile"
        :openTablet="openTablet"
        @toggleSidebar="toggleSidebar"
      />
    </div>
  </TooltipProvider>
</template>
