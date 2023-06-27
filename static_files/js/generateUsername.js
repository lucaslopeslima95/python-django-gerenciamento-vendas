function generateUsername(nameUser){
    var nameUserCurrent = nameUser.value;
    var suggestUsername = nameUserCurrent.replaceAll(" ",".")
    document.getElementById('id_username').value = suggestUsername.toLowerCase()
    inputStandardPassword()
}