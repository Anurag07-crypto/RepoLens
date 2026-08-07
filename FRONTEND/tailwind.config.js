/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f4f7ff',
          100: '#e9efff',
          500: '#5b7cff',
          600: '#4b6bf5',
          700: '#3753d6'
        }
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(255,255,255,0.08), 0 20px 60px rgba(91,124,255,0.22)'
      }
    }
  },
  plugins: []
}
