export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}"
    ],
    theme: {
        extend: {
            colors: {
                film: "#3A2C1E",
                paper: "#F3EEE6",
                grain: "#7A746E",
                amber: "#D7A44B",
                dark: "#161413",
                danger: "#8B2E2E",
            },
            fontFamily: {
                title: ["Playfair Display", "serif"],
                ui: ["Montserrat", "sans-serif"],
                body: ["Source Sans 3", "sans-serif"],
            },
            td: {
                verticalAlign: "top",
            },
        },
    },
}