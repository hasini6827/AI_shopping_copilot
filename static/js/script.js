document.addEventListener("DOMContentLoaded", function () {

    // Auto-hide alerts
    document.querySelectorAll(".alert").forEach(alert => {

        setTimeout(() => {

            alert.style.transition = "0.5s";
            alert.style.opacity = "0";

            setTimeout(() => {

                alert.remove();

            }, 500);

        }, 3000);

    });

    // Navbar shadow
    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if (!navbar) return;

        navbar.style.boxShadow =
            window.scrollY > 40
            ? "0 10px 25px rgba(0,0,0,.10)"
            : "0 5px 15px rgba(0,0,0,.05)";

    });

    // Back to top
    const topBtn = document.getElementById("backToTop");

    if(topBtn){

        window.addEventListener("scroll",()=>{

            topBtn.style.display =
                window.scrollY>300 ? "flex":"none";

        });

        topBtn.addEventListener("click",()=>{

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }

});