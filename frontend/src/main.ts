import './style.css'

// import "../node_modules/@milkdown/crepe/src/theme/nord-dark/style.css";
// import "../node_modules/@milkdown/crepe/src/theme/common/style.css"

let toggler = document.getElementById('theme-toggler');
let htmlEL = document.documentElement


toggler?.addEventListener('click', (_) => {
    htmlEL.classList.toggle('dark');

    let isDark = htmlEL.classList.contains('dark');

    if (isDark) {
        localStorage.setItem("theme", "dark");
    }
    else {
        localStorage.setItem("theme", "light");
    }
})