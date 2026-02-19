document.addEventListener("DOMContentLoaded", function () {

    const slider = document.getElementById("storiesSlider");
    if (!slider) return;

    const speed = 3500;

    setInterval(() => {
        const firstCard = slider.firstElementChild;

        slider.style.transition = "transform 0.6s ease";
        slider.style.transform = "translateX(-280px)";

        setTimeout(() => {
            slider.style.transition = "none";
            slider.style.transform = "translateX(0)";
            slider.appendChild(firstCard);
        }, 600);

    }, speed);

});



function openVideo(youtube, file) {
    document.getElementById("videoModal").style.display = "flex";

    if (youtube) {
        document.getElementById("youtubeFrame").src =
            youtube.replace("watch?v=", "embed/");
        document.getElementById("localVideo").style.display = "none";
    } else {
        document.getElementById("localVideo").src = file;
        document.getElementById("youtubeFrame").style.display = "none";
    }
}

function closeVideo() {
    document.getElementById("videoModal").style.display = "none";
    document.getElementById("youtubeFrame").src = "";
    document.getElementById("localVideo").pause();
}
