const avg_review= document.querySelectorAll(".review_card")

// ! ----------------------- AVG RATING --------------
avg_review.forEach((r) => {
    const stars = r.querySelectorAll(".user-star")
    const rating = r.querySelector(".stars").dataset.rating

    stars.forEach((star) => {
        star.classList.remove("not-filled")
    })

    for (let i=rating; i<5; i++) {
        stars[i].classList.add("not-filled")
    }
})

// ! ------------- Rating Stars ---------------------
const ratings= document.querySelectorAll(".rating")

ratings.forEach((r) => {
    const rate_arr = r.querySelector(".course_rating").textContent.split(".")
    const stars = r.querySelectorAll(".avg-star")

    rate_arr[0] = parseInt(rate_arr[0])
    rate_arr[1] = parseInt(rate_arr[1])

    stars.forEach((star) => {
        star.classList.add("not-filled")
    });

    if (rate_arr[1] > 5) {
        rate_arr[0] += 1
        rate_arr[1] = 0
    }
    else if (rate_arr[1] > 0 && rate_arr[1] < 6) {
        rate_arr[1] = 5
    }

    if (rate_arr[1] == 5) {
        stars[rate_arr[0]].textContent = "star_half"
    }

    for (let i=0; i<rate_arr[0]; i++) {
        stars[i].classList.remove("not-filled")
    }

})
