'use strict';

/**
 * navbar toggle
 */

const overlay = document.querySelector('[data-overlay]');
const navOpenBtn = document.querySelector('[data-nav-open-btn]');
const navbar = document.querySelector('[data-navbar]');
const navCloseBtn = document.querySelector('[data-nav-close-btn]');
const navLinks = document.querySelectorAll('[data-nav-link]');

const navElemArr = [navOpenBtn, navCloseBtn, overlay];

const navToggleEvent = function (elem) {
  for (let i = 0; i < elem.length; i++) {
    elem[i].addEventListener('click', function () {
      navbar.classList.toggle('active');
      overlay.classList.toggle('active');
    });
  }
};

navToggleEvent(navElemArr);
navToggleEvent(navLinks);

/**
 * header sticky & go to top
 */

const header = document.querySelector('[data-header]');
const goTopBtn = document.querySelector('[data-go-top]');

window.addEventListener('scroll', function () {
  if (window.scrollY >= 200) {
    header.classList.add('active');
    goTopBtn.classList.add('active');
  } else {
    header.classList.remove('active');
    goTopBtn.classList.remove('active');
  }
});

//side buttons

const carouselWrapper = document.querySelector('.carousel-wrapper');
const prevButton = document.querySelector('.carousel-control.prev');
const nextButton = document.querySelector('.carousel-control.next');

let currentSlide = 0; // Keeps track of the current slide index

function moveSlide(offset) {
  const slides = carouselWrapper.querySelectorAll('.blog-post');
  const slideWidth = slides[0].offsetWidth; // Get width of a single slide

  currentSlide = currentSlide + offset; // Update current slide index

  // (first and last slides)
  if (currentSlide < 0) {
    currentSlide = slides.length - 1; // Go to last slide
  } else if (currentSlide >= slides.length) {
    currentSlide = 0; // Go to first slide
  }

  carouselWrapper.style.transform = `translateX(-${
    currentSlide * slideWidth
  }px)`;
}

prevButton.addEventListener('click', () => moveSlide(-1));
nextButton.addEventListener('click', () => moveSlide(1));
