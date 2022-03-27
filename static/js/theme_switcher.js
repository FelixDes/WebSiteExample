const moonPath = "/static/assets/theme_switcher/moon.svg";
const sunPath = "/static/assets/theme_switcher/sun.svg";

(function () {
    setTheme(getCookie("theme") == "theme-dark" ? "theme-dark" : "theme-light");
    document.getElementById("theme_switcher_icon").scr = themeName == "theme-dark" ? sunPath : moonPath;
})();

function setTheme(themeName) {
    setCookie("theme", themeName, {secure: true, 'max-age': 259200});
    const html = document.querySelector('html');
    html.dataset.theme = themeName;
    if (themeName == "theme-dark") {
        document.getElementById("theme_switcher_icon").scr = sunPath;
    } else {
        document.getElementById("theme_switcher_icon").scr = moonPath;
    }
}

function toggleTheme() {
    if (getCookie("theme") == "theme-dark") {
        setTheme("theme-light");
        document.getElementById("theme_switcher_icon").src = moonPath;
    } else {
        setTheme("theme-dark");
        document.getElementById("theme_switcher_icon").src = sunPath;
    }
}

//alert(document.cookie);

// cookie файлы не будут работать, если не эмулировать сайт
// на сервере можно использовать закоментированную реализацию
// если же открывать сайт как index.html, то будет использовано сохранение в LocalStorage

function setCookie(name, value) {
    localStorage.setItem(name, value);
}
function getCookie(name) {
    return localStorage.getItem(name);
}

// function setCookie(name, value, options = {}) {
//     options = {
//         path: '/',
//         ...options
//     };
//
//     if (options.expires instanceof Date) {
//         options.expires = options.expires.toUTCString();
//     }
//
//     let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
//
//     for (let optionKey in options) {
//         updatedCookie += "; " + optionKey;
//         let optionValue = options[optionKey];
//         if (optionValue !== true) {
//             updatedCookie += "=" + optionValue;
//         }
//     }
//     document.cookie = updatedCookie;
// }
//
// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }