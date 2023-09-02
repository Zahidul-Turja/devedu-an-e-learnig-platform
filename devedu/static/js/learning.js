const video = document.querySelector("video");
const source = video.querySelector("source");
const contents = document.querySelectorAll(".content")
const title = document.querySelector(".video-title")

const pdf_reader = document.querySelector(".pdf-reader")

let vid_count = 0;
let pdf_count = 0;


contents.forEach((c) => {
    const url = c.dataset.url
    const type = url.slice(-3)

    c.addEventListener("click", () => {
        video.pause();
        source.src = "";
        if (type == "mp4") {
            source.src = url;
            video.load();
            video.currentTime = 0
            video.muted = false;
            video.play();
            title.textContent = c.dataset.serial + ". " + c.dataset.title;
            video.dataset.serial = c.dataset.serial;
            vid_count += 1;
        }
        else {
            pdf_reader.href = url;
            pdf_reader.click();
            video.pause();
            pdf_count += 1;
        }
    })

    if (type == "mp4") {
        c.textContent = c.textContent + " (video)"
    }
    else if (type == "pdf") {
        c.textContent = c.textContent + " (pdf)"
    }

})


// ! -------------------------- Course Type ----------------------------
// ! -------------------------- Certificate ----------------------------
// const certificate = document.getElementById("certificate")
// console.log(certificate.href)

// ! -------------------------- Session Video ----------------------------

while(true) {
    var n = 1;
    var contents_container = document.querySelector(".contents__container")
    if (video.dataset.serial <= 0) {
        var session_content = contents_container.querySelector(`[data-serial="${n}"]`)
        video.dataset.serial = 1
    }
    else {
        var session_content = contents_container.querySelector(`[data-serial="${video.dataset.serial}"]`)
    }

    console.log(video.dataset.serial)
    var item_type = session_content.dataset.url.slice(-3)
    
    console.log(item_type)

    if(item_type != "mp4"){
        video.dataset.serial -= 1;
        video.dataset.duration = 0
    }
    else {
        video.pause();
        source.src = session_content.dataset.url;
        video.load();
        video.currentTime = video.dataset.duration;
        // video.play();
        title.textContent = session_content.dataset.serial + ". " + session_content.dataset.title;
        video.dataset.serial = session_content.dataset.serial;
        break;
    }
}
// ! -------------------- Session ends------------------

