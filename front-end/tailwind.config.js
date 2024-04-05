/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        main: {
          50: '#FAF7F6',
          100: '#F6F1EF',
          light: '#edd1cb',
          DEFAULT: '#DAA4AC',
          medium: '#945785',
          800: "#774576",
          dark: '#613969'
        }
      },
    },
  },
  plugins: [],
}

