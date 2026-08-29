// ============================================================
// SMILE CARE DENTAL – BOOKING PAGE JAVASCRIPT
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ========== MASCOT CLICK GIGGLE ==========
  const mascot = document.querySelector('.mascot img');
  if (mascot) {
    mascot.addEventListener('click', function () {
      this.style.animation = 'none';
      this.offsetHeight;                  // reflow
      this.style.animation = 'toothWiggle 0.5s ease-in-out';
    });
  }

  // ========== SLOT CONFLICT MODAL FUNCTIONS ==========
  window.showSlotModal = function (message) {
    const modal = document.getElementById('slotModal');
    const msg = document.getElementById('slotModalMessage');
    if (modal && msg) {
      msg.textContent = message;
      modal.classList.add('open');
    }
  };

  window.closeSlotModal = function () {
    const modal = document.getElementById('slotModal');
    if (modal) modal.classList.remove('open');
  };

  // Close modal when clicking outside the content area
  window.addEventListener('click', function (event) {
    const modal = document.getElementById('slotModal');
    if (event.target === modal) {
      closeSlotModal();
    }
  });

  // ========== AUTO‑SHOW POPUP IF SLOT CONFLICT ==========
  // The hidden `<div id="slot-error-flag">` is only present when the view
  // detects a duplicate booking.
  if (document.getElementById('slot-error-flag')) {
    showSlotModal('This time-slot has already been taken. Please choose another time.');
  }

});