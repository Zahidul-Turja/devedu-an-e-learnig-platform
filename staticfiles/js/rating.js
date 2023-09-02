const rating_stars = document.querySelectorAll(".rating-star")
const rating_input = document.getElementById("id_rating")

const avg_review= document.querySelector(".avg_review")

const rating_block = document.querySelectorAll(".rating_block")
let star_num = 0


// ! ---------------------------------- UTILITY FUNCTIONS ------------------
function addRating(index) {
    let rating = index+1
    rating_input.value = rating
}


function addFill(cls, index) {
    for (let i=0; i<=index; i++) {
        // const star = document.getElementById(cls+i)
        const star = document.querySelector(String(cls+i))
        star.classList.remove("not-filled")
    }
}

// ! ----------------------------------- Utility End -----------------------

rating_stars.forEach((item, index) => {
    item.addEventListener("click", ()=> {
        console.log(index)
        rating_stars.forEach((item)=> {
            item.classList.add("not-filled")       
        })
        addFill(".s", index)
        addRating(index)
    })
})

rating_block.forEach((item) => {
    const r = item.dataset.rating
    const stars = item.querySelector(".stars").querySelectorAll(".user-star")
    stars.forEach((star) => {
        star.classList.add("not-filled")
    })
    for (let i=0; i < r; i++) {
        stars[i].classList.remove("not-filled")
        console.log(i)
    }
    // console.log(r)
})


// ! ----------------------- AVG RATING --------------
const avg_rating = avg_review.querySelector(".avg_rating")
const avg_stars = avg_review.querySelectorAll(".avg-star")
let avg_rating_arr = avg_rating.textContent.split(".")
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
