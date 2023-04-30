// function to toggle the sidebar
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("active");
}

// function to show or hide the password field
function togglePassword() {
  var passwordField = document.getElementById("password");
  if (passwordField.type === "password") {
    passwordField.type = "text";
  } else {
    passwordField.type = "password";
  }
}

// function to validate the password fields on the signup page
function validatePassword() {
  var passwordField = document.getElementById("password");
  var confirmPasswordField = document.getElementById("confirm-password");
  var errorMessage = document.getElementById("error-message");
  if (passwordField.value != confirmPasswordField.value) {
    errorMessage.style.display = "block";
    return false;
  } else {
    errorMessage.style.display = "none";
    return true;
  }
}

// function to show the preview of the selected image file
function previewImage(event) {
  var imagePreview = document.getElementById("image-preview");
  imagePreview.src = URL.createObjectURL(event.target.files[0]);
  imagePreview.style.display = "block";
}
