function inputPriceMask(input) {
    var valor = input.value;

    valor = valor.replace(/\D/g, '');

    var parteInteira = valor.slice(0, -2);
    var parteDecimal = valor.slice(-2);

    parteInteira = parteInteira.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');

    var valorFormatado = 'R$ ' + parteInteira + ',' + parteDecimal;

    input.value = valorFormatado;
}


  
  
  
  


  