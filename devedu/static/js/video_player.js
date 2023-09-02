const btn = document.querySelector(".video-btn");
const videoContainer = document.querySelector(".container");
const videoTag = document.querySelector(".video");
const overlay = document.querySelector(".overlay");


btn.addEventListener("click", () => {
  videoContainer.classList.remove("hidden");
  videoTag.play();
  videoTag.volume=0;

  // videoTag.setAttribute("controls", "true");
  // videoTag.src = videoTag.dataset.url;
});

overlay.addEventListener("click", () => {
  videoContainer.classList.add("hidden");
  // videoTag.src = "";
});
