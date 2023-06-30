function validatePassword() {
    var password = document.getElementById("id_password").value;
    var confirmPassword = document.getElementById("id_password_check").value;
  
    if (password !== confirmPassword) {
      alert("As senhas devem ser iguais.")
      return false;
    }
    if (password.length < 8) {
      alert("A senha deve ter pelo menos 8 caracteres.");
      return false;
    }
    if (!/[A-Z]/.test(password)) {
      alert("A senha deve conter pelo menos uma letra maiúscula.");
      return false;
    }
    if (!/\d/.test(password)) {
      alert("A senha deve conter pelo menos um número.");
      return false;
    }
    if (!/[a-zA-Z]/.test(password)) {
      alert("A senha deve conter pelo menos uma letra.");
      return false;
    }
    return true;
  }