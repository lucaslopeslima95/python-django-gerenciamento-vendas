const checkbox = document.getElementById('flexSwitchCheckDefault');

checkbox.addEventListener('change', function() {
  const confirmed = confirm('Confirma a desabilitação do colaborador para compras?');
  if (!confirmed) {
      checkbox.checked = !checkbox.checked;    
  }
});