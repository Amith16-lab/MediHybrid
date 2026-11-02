/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#070d18',
          900: '#0c1524',
          800: '#132238',
          700: '#1e3557',
          600: '#2d4d77',
          500: '#3e669c'
        },
        cyan: {
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
        },
        teal: {
          900: '#0f3a38',
          800: '#115e59',
          700: '#0f766e',
          600: '#0d9488',
          500: '#14b8a6',
          400: '#2dd4bf',
          300: '#5eead4',
          100: '#ccfbf1',
          50: '#f0fdfa'
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.35s ease-out forwards',
        'fade-in-up': 'fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'pulse-subtle': 'pulseSubtle 2.5s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.65' },
        }
      }
    },
  },
  plugins: [],
}
