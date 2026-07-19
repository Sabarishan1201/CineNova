const stars = document.querySelectorAll(".star");
const ratingInput = document.getElementById("rating");

if (stars.length > 0) {

    stars.forEach(star => {

        star.addEventListener("click", () => {

            let value = star.dataset.value;

            ratingInput.value = value;

            stars.forEach(s => s.classList.remove("active"));

            for (let i = 0; i < value; i++) {
                stars[i].classList.add("active");
            }

        });

    });

    // Default to 5 stars
    stars.forEach(star => star.classList.add("active"));
}