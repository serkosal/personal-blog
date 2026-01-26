import './style.css'

let toggler = document.getElementById('theme-toggler');
let htmlEL = document.documentElement


document.body.onload = (_ev) => {
    htmlEL.classList.toggle('dark', localStorage.getItem('theme') === 'dark');
}

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