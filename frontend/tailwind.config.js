/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                cyber: {
                    dark: "#050505",
                    gray: "#121212",
                    neon: "#00f0ff",
                    pink: "#ff0099",
                    purple: "#9d00ff",
                }
            },
            fontFamily: {
                mono: ['"JetBrains Mono"', 'monospace'],
                sans: ['"Inter"', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
