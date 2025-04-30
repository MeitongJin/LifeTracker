// toggle password show/hide

function togglePasswordButton(inputId, toggleIconId){
    passwordInput = document.getElementById(inputId);
    const toggleIcon = document.getElementById(toggleIconId);

    isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "password" : "text";

    if(isPassword){
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
        passwordInput.type = "text";
    }else{
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
        passwordInput.type = "password";
    }
}