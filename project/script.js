const prompts = ["✨ Your AI-Powered Career Guide"];
let currentCharIndex = 0;
let typingSpeed = 100;

const promptElement = document.getElementById("typing-prompt");

function typePrompt() {
    if (currentCharIndex < prompts[0].length) {
        promptElement.textContent += prompts[0][currentCharIndex];
        currentCharIndex++;
        setTimeout(typePrompt, typingSpeed);
    }
}

typePrompt(); 
// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add scroll reveal animation
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.faq-card, .demo-image');

    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
});


// demo video starts when we reach to the see it in action section
document.addEventListener("DOMContentLoaded", () => {
    const video = document.querySelector(".demo-video");
    const section = document.querySelector("#demo");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    video.play();
                } else {
                    video.pause();
                }
            });
        },
        { threshold: 0.5 } // Adjust to control when video plays (50% visible)
    );

    observer.observe(section);
});