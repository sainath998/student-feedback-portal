sidenav = document.querySelector(".sidenav");
sitebody = document.querySelector(".site-body");
toggler = document.querySelector(".toggler");

sidenav_status = true;

toggler.addEventListener("click", function (event) {
    if(sidenav_status) {
        sidenav.classList.add("sidenav-collapase");
        sidenav.classList.remove("sidenav-un-collapase");

        sitebody.classList.add("site-body-adjust");
        sitebody.classList.remove("site-body-un-adjust");


        sidenav_status = false;
    }

    else {
        sidenav.classList.add("sidenav-un-collapase");
        sidenav.classList.remove("sidenav-collapase");

        sitebody.classList.add("site-body-un-adjust");
        sitebody.classList.remove("site-body-adjust");

        sidenav_status = true;
    }

    console.log(sidenav.classList);
})


dissmisser = document.querySelector(".dismisser");
messages = document.querySelector(".messages");

dissmisser.addEventListener('click', function (event) {
    console.log(messages.style.display)
    messages.style.display = 'none';
})