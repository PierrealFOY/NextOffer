import { ref, watchEffect } from 'vue'

const colorMode = ref<'light' | 'dark' | 'auto'>('auto')

if (typeof window !== 'undefined') {
  const updateClass = () => {
    const html = document.documentElement
    html.classList.remove('light', 'dark')

    const isDark =
      colorMode.value === 'dark' ||
      (colorMode.value === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches)

    html.classList.add(isDark ? 'dark' : 'light')
  }

  watchEffect(() => {
    updateClass()
  })
}

export function useGlobalColorMode() {
  return colorMode
}
