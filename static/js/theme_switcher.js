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
function setCookie(name, value, options = {}) {

    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }
    document.cookie = updatedCookie;
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}