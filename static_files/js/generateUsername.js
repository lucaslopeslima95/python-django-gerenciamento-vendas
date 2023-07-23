function generateUsername(nameUser){
    var nameUserCurrent = nameUser.value;
    without_accents = nameUserCurrent.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    var suggestUsername = without_accents.replace(" ",".").replace(" ",".").replace(" ",".").replace(" ",".")
    document.getElementById('id_username').value = suggestUsername.toLowerCase().substring(0, 10);
    inputStandardPassword()
}


