$(document).ready(function () {
    $('#id_cpf').inputmask('999.999.999-99');
});


$(document).ready(function() {
    var selector = ".code_bar";
    $(selector).each(function() {
      $(this).inputmask('9-999-999999-999'); 
    });
  });


  $(document).ready(function () {
    $('#id_code_bar').inputmask('9-999-999999-999');
});