import { ref, computed } from 'vue'
import { useMediaQuery, useScreenOrientation } from '@vueuse/core'

export const useDeviceDetection = () => {
  const userAgent = ref(typeof navigator !== 'undefined' ? navigator.userAgent : '')
  const ua = computed(() => userAgent.value.toLowerCase())

  const isTouchDevice = ref(false)
  if (typeof window !== 'undefined') {
    isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0
  }

  // Media queries
  const isMobileMediaQuery = useMediaQuery('(max-width: 768px)')
  const isTabletMediaQuery = useMediaQuery('(min-width: 769px) and (max-width: 1024px)')
  const isDesktopMediaQuery = useMediaQuery('(min-width: 1025px)')

  const orientation = useScreenOrientation()
  const isLandscape = computed(() => !!orientation?.orientation?.value?.includes('landscape'))

  // User agent checks
  const isRealMobileDevice = computed(() => /android|iphone|ipod|mobile/i.test(ua.value))

  const isTabletDevice = computed(
    () =>
      /ipad|tablet|playbook|silk|android(?!.*mobile)/i.test(ua.value) || isTabletMediaQuery.value,
  )

  const isMobileDevice = computed(
    () => isMobileMediaQuery.value || (isLandscape.value && isRealMobileDevice.value),
  )

  const isDesktopDevice = computed(
    () => isDesktopMediaQuery.value && !isMobileDevice.value && !isTabletDevice.value,
  )

  return {
    userAgent,
    isMobileDevice,
    isTabletDevice,
    isDesktopDevice,
    isTouchDevice,
    isLandscape,
  }
}
