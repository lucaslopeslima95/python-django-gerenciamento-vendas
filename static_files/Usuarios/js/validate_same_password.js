function validate_same_password(){
    password = document.getElementById('id_password');
    password_check =  document.getElementById('id_password_check');
    if (password.value == password_check.value){
        return confirm("Deseja Realmente atualizar")
    }else{
        alert("As senhas nao coincidem")
        return false;
    }
}