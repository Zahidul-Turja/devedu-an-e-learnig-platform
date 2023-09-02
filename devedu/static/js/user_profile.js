// const btn_learnings = document.querySelectorAll(".btn-learnings")
// const btn_wishlist = document.querySelectorAll(".btn-wishlist")

// const learning_container = document.querySelector(".my_learnings")
// const wishlist_container = document.querySelector(".wishlist")

// btn_learnings.forEach((btn) => {
//     btn.addEventListener("click", () => {
//         wishlist_container.classList.add("hidden")
//         learning_container.classList.remove("hidden")
//     })
// })
// btn_wishlist.forEach((btn) => {
//     btn.addEventListener("click", () => {
//         learning_container.classList.add("hidden")
//         wishlist_container.classList.remove("hidden")
//     })
// })


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

// ! ------------------------- Count PDFs ------------------------------



// ! -------------------------- Progress Bar ----------------------------

const progressBars = document.querySelectorAll(".progress_bar")

progressBars.forEach((bar) => {
    const progress = bar.querySelector(".progress_filled")
    let finished = bar.dataset.completed
    let total = bar.dataset.total
    let pdf_count = 0;
    
    const content_urls = bar.querySelectorAll(".content-urls")
    content_urls.forEach((url) => {
        let type = url.dataset.url.slice(-3)
        if(type != "mp4") {
            total -= 1;
            pdf_count += 1;
        }
    })

    if(total == 0){ 
        total = 1;
    }

    if(pdf_count == total) {
        finished = 1;
        total = 1;
    }
    
    const percent = (finished / total) * 100;
    progress.style.flexBasis = `${percent}%`;

    bar.parentElement.dataset.percent = percent;
})


// ! -------------------------------------------- Certificate -----------------------------------
const allCards = document.querySelectorAll(".course_card")

allCards.forEach((card) => {
    const per = parseFloat(card.dataset.percent)

    if(per > 90) {
        console.log(per)
        const btnCertificate = card.querySelector(".btn-certificate")
        btnCertificate.classList.remove("hidden")
    }
})