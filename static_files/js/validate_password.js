function validarSenha() {
    
    
    if (senha.length < 8) {
        return false; 
    }

    if (!/[a-z]/.test(senha) || !/[A-Z]/.test(senha) || !/[0-9]/.test(senha) || !/[!@#$%^&*]/.test(senha)) {
        return false; // A senha não contém a combinação de caracteres necessária
    }

    if (senha.includes("seu_nome") || senha.includes("data_de_nascimento")) {
        return false; // A senha contém informações pessoais óbvias
    }

    if (/([a-zA-Z])\1{2,}/.test(senha)) {
        return false; // A senha contém sequências repetitivas de caracteres
    }

    // Verificar com lista de senhas comuns
    var senhasComuns = ["password", "12345678", "qwertyui",];
    if (senhasComuns.includes(senha)) {
        return false; // A senha está na lista de senhas comuns
    }

    return true; // A senha é segura
}
