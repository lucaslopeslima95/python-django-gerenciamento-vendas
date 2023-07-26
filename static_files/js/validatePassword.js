
const nameInput = document.getElementById("id_name");
const usernameInput = document.getElementById("id_username");
const emailInput = document.getElementById("id_email");
const passwordInput = document.getElementById("id_password");
const confirmPasswordInput = document.getElementById("id_password_check");
const passwordStrength = document.getElementById("passwordStrength");
const passwordMatch = document.getElementById("passwordMatch");
const cpfInput = document.getElementById("id_cpf");
const btnSaveUser = document.getElementById("btn-save-user");

function updatePasswordStrength() {
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

 
  if (password === "" && confirmPassword === "") {
    passwordStrength.style.display = "none";
    passwordMatch.textContent = "";
  } else {
   
    passwordStrength.style.display = "block";

    const result = zxcvbn(password);
    const score = result.score; 

    
    const progressBar = passwordStrength.querySelector(".progress-bar");
    progressBar.style.width = `${(score / 4) * 100}%`;

   
    if (score === 0) {
      progressBar.className = "progress-bar bg-danger";
    } else if (score === 1 || score === 2) {
      progressBar.className = "progress-bar bg-warning";
    } else {
      progressBar.className = "progress-bar bg-success";
    }

  
    if (score < 3) {
      passwordMatch.textContent = "Senha fraca. Por favor, insira uma senha mais forte.";
      passwordMatch.style.color = "red";
    } else {
      passwordMatch.textContent = "Senha forte. Pode prosseguir.";
      passwordMatch.style.color = "green";
    }
  }

  
  const nameValid = validateField(nameInput, 3);
  const usernameValid = validateField(usernameInput, 3);
  const emailValid = validateField(emailInput, 3);

 
  const cpfValid = validateCPF(cpfInput);
  if (!cpfValid) {
    cpfInput.classList.add("border-danger");
    cpfInput.classList.remove("border-success");
  } else {
    cpfInput.classList.remove("border-danger");
    cpfInput.classList.add("border-success");
  }

 
  const passwordScore = (zxcvbn(password).score / 4) * 100;
  const isPasswordStrong = passwordScore >= 75;
  if (isPasswordStrong) {
    passwordInput.classList.add("border-success");
    confirmPasswordInput.classList.add("border-success");
  } else {
    passwordInput.classList.remove("border-success");
    confirmPasswordInput.classList.remove("border-success");
  }


  btnSaveUser.disabled = !(isPasswordStrong && cpfValid && nameValid && usernameValid && emailValid);
}

function reverseString(str) {
  return str.split('').reverse().join('');
}

function validateCPF(input_cpf) {

  strTemp = input_cpf.value;
  var strCPF = strTemp.replaceAll(".", "").replaceAll("-", "").replaceAll("_", "");
  var Soma;
  var Resto;
  Soma = 0;
  if (strCPF == '___.___.___-__') return false
  if (strCPF == '') return false
  if (reverseString(strCPF) === strCPF) return false;

  for (i = 1; i <= 9; i++)
    Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (11 - i);
  Resto = (Soma * 10) % 11;
  if ((Resto == 10) || (Resto == 11))
    Resto = 0;
  if (Resto != parseInt(strCPF.substring(9, 10)))
    return false;
  Soma = 0;
  for (i = 1; i <= 10; i++)
    Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (12 - i);
  Resto = (Soma * 10) % 11;
  if ((Resto == 10) || (Resto == 11))
    Resto = 0;
  if (Resto != parseInt(strCPF.substring(10, 11)))
    return false;
  return true; 
}


function validateField(inputField, minLength) {
  const fieldValue = inputField.value.trim();
  if (fieldValue.length < minLength) {
    inputField.classList.add("border-danger");
    inputField.classList.remove("border-success");
    return false;
  } else {
    inputField.classList.remove("border-danger");
    inputField.classList.add("border-success");
    return true;
  }
}

passwordInput.addEventListener("input", updatePasswordStrength);
confirmPasswordInput.addEventListener("input", updatePasswordStrength);
cpfInput.addEventListener("input", updatePasswordStrength);
nameInput.addEventListener("input", updatePasswordStrength);
usernameInput.addEventListener("input", updatePasswordStrength);
emailInput.addEventListener("input", updatePasswordStrength);


