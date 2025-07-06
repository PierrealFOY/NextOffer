/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      animation: {
        pulseSlow: 'pulse 4s ease-in-out infinite',
      },
      colors: {
        //
        baseLight: '#F8F8F8',
        baseMedium: '#E0E0E0',
        baseDark: '#333333',
        accentPrimary: '#8A9A5B',
        accentSecondary: '#488A99',
        highlightGreen: '#9BAF6A',
        mintGreen: '#34D399',
        //
        neonBlue: '#33FFFF',
        matteBlack: '#1e1e2f',
        retroYellow: '#FFEFD5',
        softRed: '#FF6B6B',
        gold: '#FFD700',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          1: 'hsl(var(--chart-1))',
          2: 'hsl(var(--chart-2))',
          3: 'hsl(var(--chart-3))',
          4: 'hsl(var(--chart-4))',
          5: 'hsl(var(--chart-5))',
        },
        sidebar: {
          DEFAULT: 'hsl(var(--sidebar-background))',
          foreground: 'hsl(var(--sidebar-foreground))',
          primary: 'hsl(var(--sidebar-primary))',
          'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
          accent: 'hsl(var(--sidebar-accent))',
          'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
          border: 'hsl(var(--sidebar-border))',
          ring: 'hsl(var(--sidebar-ring))',
        },
      },
      borderRadius: {
        arcade: '6px',
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      fontFamily: {
        arcade: ['Press Start 2P"', 'VT323"', 'monospace'],
        roboto: ['Roboto', 'sans-serif'],
        Merriweather: ['Merriweather', 'serif'],
      },
      boxShadow: {
        'br-light': '6px 6px #8A9A5B',
        'br-dark': '6px 6px #34D399',
        // inset: 'inset 0 0 6px #00BFFF',
        inset: 'inset 0 0 6px #6E7C4E',
      },
      safelist: [
        'pulseSlow',
        'text-gold',
        'text-softRed',
        'border-neonBlue',
        'hover:text-matteBlack',
        'hover:bg-retroYellow',
      ],
    },
  },
  plugins: [
    require('tailwindcss-animate'),
    function ({ addUtilities, theme }) {
      const newUtilities = {
        '.highlight-bottom-light': {
          background: `linear-gradient(to top, ${theme('colors.highlightGreen')} 10%, transparent 80%)`,
          backgroundPosition: '0% 0%',
        },
        '.highlight-bottom-dark': {
          background: `linear-gradient(to top, ${theme('colors.mintGreen')} 10%, transparent 80%)`,
          backgroundPosition: '50% 50%',
        },
      }

      addUtilities(newUtilities)
    },
  ],
}
