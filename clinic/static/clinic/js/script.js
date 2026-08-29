// ============================================================
// SMILE CARE DENTAL – MASTER JAVASCRIPT (CLEAN)
// ============================================================
// Features:
// 1.  Preloader hide
// 2.  Hamburger menu toggle
// 3.  Scroll‑reveal animations
// 4.  Testimonial carousel (manual + auto‑scroll)
// 5.  Back‑to‑top button
// 6.  Header scrolled class
// 7.  Active navigation link
// 8.  Smooth internal anchor scrolling
// 9.  Animated counters (About page)
// 10. Mascot click giggle (Booking page)
// 11. Lazy‑loading images
// 12. Floating label effect on form inputs
// 13. Staggered team card reveal (Team page)
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ========== 1. PRELOADER ==========
  const preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', () => preloader.classList.add('hidden'));
  }

  // ========== 2. HAMBURGER MENU ==========
  const hamburger = document.getElementById('hamburgerBtn');
  const mainNav = document.getElementById('mainNav');
  if (hamburger && mainNav) {
    hamburger.addEventListener('click', () => mainNav.classList.toggle('active'));
    // Close menu when a link is clicked (mobile)
    mainNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) mainNav.classList.remove('active');
      });
    });
  }

  // ========== 3. SCROLL REVEAL (sections) ==========
  const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (revealElements.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -30px 0px' });
    revealElements.forEach(el => revealObserver.observe(el));
  }

  // ========== 4. TESTIMONIAL CAROUSEL ==========
  const prevBtn = document.getElementById('prevTestimonial');
  const nextBtn = document.getElementById('nextTestimonial');
  const testimonialGrid = document.querySelector('.testimonial-grid');
  if (prevBtn && nextBtn && testimonialGrid) {
    const scrollAmount = 350;
    prevBtn.addEventListener('click', () => testimonialGrid.scrollBy({ left: -scrollAmount, behavior: 'smooth' }));
    nextBtn.addEventListener('click', () => testimonialGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' }));

    let autoScrollInterval = setInterval(() => {
      testimonialGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      if (testimonialGrid.scrollLeft + testimonialGrid.clientWidth >= testimonialGrid.scrollWidth - 10) {
        testimonialGrid.scrollTo({ left: 0, behavior: 'smooth' });
      }
    }, 4000);

    testimonialGrid.addEventListener('mouseenter', () => clearInterval(autoScrollInterval));
    testimonialGrid.addEventListener('mouseleave', () => {
      autoScrollInterval = setInterval(() => {
        testimonialGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      }, 4000);
    });
  }

  // ========== 5. BACK TO TOP BUTTON ==========
  const backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('show', window.scrollY > 400);
    });
    backToTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ========== 6. HEADER SCROLLED CLASS ==========
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ========== 7. ACTIVE NAVIGATION LINK ==========
  const currentPage = window.location.pathname;
  document.querySelectorAll('.nav a').forEach(link => {
    const linkPath = link.getAttribute('href').replace(/\/$/, '');
    link.classList.toggle('active-link', (currentPage === linkPath || (currentPage === '/' && linkPath === '')));
  });

  // ========== 8. SMOOTH INTERNAL ANCHOR SCROLLING ==========
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // ========== 9. ANIMATED COUNTERS (About page) ==========
  const statNumbers = document.querySelectorAll('.stat-number');
  if (statNumbers.length) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target'));
          if (!target) return;
          let current = 0;
          const increment = target / 50;
          const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
              el.textContent = target + '+';
              clearInterval(timer);
            } else {
              el.textContent = Math.floor(current) + '+';
            }
          }, 30);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statNumbers.forEach(el => counterObserver.observe(el));
  }

  // ========== 10. MASCOT CLICK GIGGLE (Booking page) ==========
  const mascot = document.querySelector('.mascot img');
  if (mascot) {
    mascot.addEventListener('click', function () {
      this.style.animation = 'none';
      this.offsetHeight; // reflow
      this.style.animation = 'toothWiggle 0.5s ease-in-out';
    });
  }

  // ========== 11. LAZY LOADING IMAGES ==========
  const lazyImages = document.querySelectorAll('img[data-src]');
  if (lazyImages.length) {
    const imgObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    }, { rootMargin: '50px 0px' });
    lazyImages.forEach(img => imgObserver.observe(img));
  }

  // ========== 12. FLOATING LABEL EFFECT ==========
  document.querySelectorAll('.form-group input, .form-group select, .form-group textarea').forEach(field => {
    field.addEventListener('focus', () => field.parentElement.classList.add('focused'));
    field.addEventListener('blur', () => {
      if (!field.value) field.parentElement.classList.remove('focused');
    });
    if (field.value) field.parentElement.classList.add('focused');
  });

  document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.service-card');
  if (!cards.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // Add staggered delay
        const delay = index * 0.08; // 80ms between each card
        entry.target.style.transition = 'opacity 0.6s ease ' + delay + 's, transform 0.6s ease ' + delay + 's';
        entry.target.classList.add('reveal', 'active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(40px)';
    observer.observe(card);
  });
});


// ==============================================
// CONTACT PAGE – MODAL & INTERACTIONS
// ==============================================

// Show modal
function showModal(message) {
  const modal = document.getElementById('popupModal');
  const msg = document.getElementById('modalMessage');
  if (modal && msg) {
    msg.textContent = message;
    modal.classList.add('open');
  }
}

// Close modal
function closeModal() {
  const modal = document.getElementById('popupModal');
  if (modal) {
    modal.classList.remove('open');
  }
}

// Close if user clicks outside the modal
window.addEventListener('click', function(event) {
  const modal = document.getElementById('popupModal');
  if (event.target === modal) {
    closeModal();
  }
});

  // Auto-open SMS app after booking (user still needs to press Send)
  window.addEventListener('load', function() {
    var phone = "{{ formatted_phone }}";  // pass this from your view
    var message = "{{ sms_text|escapejs }}";
    if (phone && message) {
      var smsUrl = 'sms:' + phone + '?body=' + encodeURIComponent(message);
      window.open(smsUrl, '_blank');
    }
  });


  // ========== 13. STAGGERED TEAM CARD REVEAL (Team page) ==========
  const teamCards = document.querySelectorAll('.team-card');
  if (teamCards.length) {
    const teamObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          const delay = index * 0.1;
          entry.target.style.transitionDelay = delay + 's';
          entry.target.classList.add('reveal', 'active');
          teamObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    teamCards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      teamObserver.observe(card);
    });
  }

}); 

// ==============================================
// REVIEWS PAGE – CAROUSEL & INTERACTIONS
// ==============================================

document.addEventListener('DOMContentLoaded', function () {
  // Review carousel scroll
  var prev = document.getElementById('prevReview');
  var next = document.getElementById('nextReview');
  var grid = document.getElementById('reviewGrid');
  if (prev && next && grid) {
    var amount = 350;
    prev.addEventListener('click', function () {
      grid.scrollBy({ left: -amount, behavior: 'smooth' });
    });
    next.addEventListener('click', function () {
      grid.scrollBy({ left: amount, behavior: 'smooth' });
    });
  }
});

// end DOMContentLoaded



