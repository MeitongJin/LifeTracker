function openModal() {
  let modal = document.getElementById('confirmModal');
  modal.classList.add('show');
}

function closeModal() {
  let modal = document.getElementById('confirmModal');
  modal.classList.remove('show');
  setTimeout(function () {
    modal.style.display = 'none'; // Delay hiding for smooth animation
  }, 300);
}

function proceedRegistration() {
  // User confirms and jumps to the registration page
  location.href = "register.html";
}

function cancelRegistration() {
  // Cancel registration and jump back to home page
  location.href = "homepage.html";
}