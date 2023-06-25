const checkbox = document.getElementById('flexSwitchCheckDefault');

checkbox.addEventListener('change', function() {
  const confirmed = confirm('Confirma a alteração de Habilitação do colaborador para compras?');
  if (!confirmed) {
      checkbox.checked = !checkbox.checked;    
  }else{ 
    var id_colab =  document.getElementById('id_colab').value;
    var url = "http://127.0.0.1:8000/collaborator/update_active_collaborator/"+id_colab;
    window.location.href = url;
  }
});