document.addEventListener('DOMContentLoaded', function() {

    let theme = localStorage.getItem("theme")
    let elements = document.getElementsByClassName('my_bg');
    let elements1 = document.getElementsByClassName('my_border');
    let elements2 = document.getElementsByClassName('my_text');

    let moon = document.getElementById('moon');
    let sun = document.getElementById('sun');

    if (theme) {
        if (theme === 'day') {
            day()
            hide_sun()
        } else {
            night()
            hide_moon()
        }
    } else {
        localStorage.setItem("theme", "day")
        day()
        hide_sun()
    }

    moon.addEventListener('click', night)
    moon.addEventListener('click', hide_moon)
    sun.addEventListener('click', day)
    sun.addEventListener('click', hide_sun)

    function hide_moon() {
        const att = document.createAttribute("hidden");
        moon.setAttributeNode(att);
        sun.removeAttribute('hidden');
    }

    function hide_sun() {
        const att = document.createAttribute("hidden");
        sun.setAttributeNode(att);
        moon.removeAttribute('hidden');
    }


    function night() {
        localStorage.setItem("theme", "night");

        for (let i = 0; i < elements.length; i++) {
            elements[i].className = elements[i].className + " bg-dark"
        }

        for (let i = 0; i < elements1.length; i++) {
            elements1[i].className = elements1[i].className + " border-primary"
        }


        for (let i = 0; i < elements2.length; i++) {
            elements2[i].className = elements2[i].className + " text-light"
        }
    }

    function day() {
        localStorage.setItem("theme", "day");

        for (let i = 0; i < elements.length; i++) {
            elements[i].className = elements[i].className.replace(" bg-dark", "");
       }

       for (let i = 0; i < elements1.length; i++) {
           elements1[i].className = elements1[i].className.replace("border-primary", "");
      }

      for (let i = 0; i < elements2.length; i++) {
       elements2[i].className = elements2[i].className.replace(" text-light", "");
       }
    }
})