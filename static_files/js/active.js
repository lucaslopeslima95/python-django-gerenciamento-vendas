function colorLink() {
    var currentURL = window.location.href;
    const linkColor = document.querySelectorAll('.nav-item')
    const links = []

    linkColor.forEach(function(l) {
        links.push(l)
    });

    if (currentURL.includes('usuarios')) {
        links[1].classList.add('active')
    }
    else if (currentURL.includes('relatorios')) {
        links[2].classList.add('active')
    }
    else if (currentURL.includes('colaborador')) {
        links[3].classList.add('active')
    }
    else if (currentURL.includes('produtos')) {
        links[4].classList.add('active')
    }
    else if (currentURL.includes('categorias')) {
        links[5].classList.add('active')
    }
    else if (currentURL.includes('estoque')) {
        links[6].classList.add('active')
    }
    else {
        links[0].classList.add('active')
    }
}

colorLink();