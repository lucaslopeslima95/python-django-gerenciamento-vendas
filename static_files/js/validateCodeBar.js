function validateCodeBar(element) {
    code = element.value;
    code = code.replace(/\D/g, '');
    if (code.length !== 13) {
      alert('Codigo de Barras Invalido')
      return false;
    }
    var sum = 0;
    for (var i = 0; i < 12; i += 2) {
      sum += parseInt(code.charAt(i));
    }
    sum *= 3;
    for (var j = 1; j < 12; j += 2) {
      sum += parseInt(code.charAt(j));
    }
    var checkDigit = (10 - (sum % 10)) % 10;
  
    return checkDigit === parseInt(code.charAt(12));
  }