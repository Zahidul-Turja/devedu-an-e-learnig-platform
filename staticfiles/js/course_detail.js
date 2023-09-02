const avg_review= document.querySelector(".avg_review")

// ! ---------------------------------------- AVG RATING -------------------------------------
avg_rating = avg_review.querySelector(".avg_rating")
avg_stars = avg_review.querySelectorAll(".avg-star")
avg_rating_arr = avg_rating.textContent.split(".")
avg_rating_arr[0] = parseInt(avg_rating_arr[0])
avg_rating_arr[1] = parseFloat("0." + avg_rating_arr[1])

if (avg_rating_arr[1] > 0 && avg_rating_arr[1] <= 0.5) {
    avg_rating_arr[1] = 5
}
else if (avg_rating_arr[1] > 0.5){
    avg_rating_arr[0] += 1
    avg_rating_arr[1] = 0
}

avg_stars.forEach((item) => {
    item.classList.add("not-filled")
})

for (let i=0; i < avg_rating_arr[0]; i++) {
    avg_stars[i].classList.remove("not-filled")
}

if (avg_rating_arr[1] == 5) {
    avg_stars[avg_rating_arr[0]].textContent = "star_half"
}

// ! ---------------------------------------- Course Type ------------------------------------------
const contents = document.querySelectorAll(".content")

contents.forEach((content) => {
    const url = content.querySelector(".title").dataset.url
    const c_type = url.slice(-3)
    const type_box = content.querySelector(".type")
    
    if (c_type == "mp4") {
        type_box.textContent = "Video(mp4)"
    }
    else if (c_type == "pdf"){
        type_box.textContent = "PDF"
    }
    else {
        type_box.textContent = "Other"
    }
})

// ! -------------------------------------- user reviews ------------
const user_reviews = document.querySelectorAll(".right")


user_reviews.forEach((r) => {
    const rating = r.dataset.rating
    const stars = r.querySelectorAll(".user-star")

    stars.forEach((star) => {
        star.classList.add("not-filled")
    })

    for (let i=0; i<rating; i++) {
        stars[i].classList.remove("not-filled")
    }
})
