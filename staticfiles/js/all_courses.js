
function starFill() {
    const review = document.querySelectorAll(".rating")
    
    review.forEach((item) => {
        stars = item.querySelectorAll(".user-star")
        rating_arr = item.querySelector(".avr_rating").textContent.split(".")
        rating_arr[0] = parseInt(rating_arr[0])
        rating_arr[1] = parseInt(rating_arr[1])
    
        if(rating_arr[1] > 0 && rating_arr[1]<6){
            rating_arr[1] = 5;
        }
        else if (rating_arr[1] > 5) {
            rating_arr[0] += 1;
            rating_arr[1] = 0
        }
    
        stars.forEach((star) => {
            star.classList.add("not-filled")
        })
    
        for (let i=0; i < rating_arr[0]; i++) {
            stars[i].classList.remove("not-filled")
        }
    
        if(rating_arr[1] == 5) {
            stars[rating_arr[0]].textContent = "star_half"
        }
    })
}


function handleDOMChanges(mutationsList, observer) {
    starFill();
}

var observer = new MutationObserver(handleDOMChanges);
var observerConfig = { childList: true, subtree: true };
observer.observe(document.body, observerConfig);
  