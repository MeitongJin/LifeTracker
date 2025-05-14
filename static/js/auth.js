// toggle password show/hide

function togglePasswordButton(inputId, toggleIconId){
    const passwordInput = document.getElementById(inputId);
    const toggleIcon = document.getElementById(toggleIconId);

    const isPassword = passwordInput.type === "password";

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