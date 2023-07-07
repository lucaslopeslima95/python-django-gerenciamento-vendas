const checkbox = document.getElementById('switchStatusProduct');

checkbox.addEventListener('change', function() {
  const confirmed = confirm('Confirma a alteração da situação do produto?');
  if (!confirmed) {
      checkbox.checked = !checkbox.checked;    
  }else{ 
    var id_product =  document.getElementById('id_product').value;
    var url = "http://127.0.0.1:8000/product/update_status_product/"+id_product;
    window.location.href = url;
  }
});