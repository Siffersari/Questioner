var email = document.getElementById("email");

email.addEventListener("input", function (event) {
  if (email.validity.typeMismatch) {
    email.setCustomValidity("Sorry, we are not to be able to validate your email. Please input a valid email address or use a different one.");
  } else {
    email.setCustomValidity("");
  }
});

function checkpassmatch(){
    var password = document.getElementById("pwd").value;
    var cpassword = document.getElementById("cpwd").value;

    if (password != cpassword) {
        document.getElementById('error').innerHTML = "Please make sure that passwords match!"
    }
}
