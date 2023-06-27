function generateUsername(nameUser){
    var nameUserCurrent = nameUser.value;
    var suggestUsername = nameUserCurrent.replace(" ",".")
    document.getElementById('id_username').value = suggestUsername.toLowerCase()
    inputStandardPassword()
}