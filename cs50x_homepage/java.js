//Button functionalities

document.querySelectorAll(".btn-link").forEach(link => {
    link.addEventListener("click", function() {
        console.log("Button clicked!");
        const url = this.getAttribute("data-url");
        if (url) {
            // Open the URL in a new tab
            window.open(url, '_blank');
        }
    });
});
