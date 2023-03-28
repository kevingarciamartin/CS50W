// Confetti button src: https://www.npmjs.com/package/js-confetti

const button = document.querySelector('.button');
const canvas = document.querySelector('.confetti__container');
const sound = document.getElementById("sound");

const jsConfetti = new JSConfetti();

button.addEventListener('click', () => {
    jsConfetti.addConfetti();
    if (sound) {
        sound.currentTime = 0;
        sound.play();
    }
});