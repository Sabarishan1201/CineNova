let lastScroll = 0;

const navbar = document.getElementById("mainNavbar");

window.addEventListener("scroll", () => {

    const currentScroll = window.pageYOffset;

    if(currentScroll <= 0){

        navbar.classList.remove("hide");

        return;

    }

    if(currentScroll > lastScroll){

        // scrolling down

        navbar.classList.add("hide");

    }else{

        // scrolling up

        navbar.classList.remove("hide");

    }

    lastScroll = currentScroll;

});