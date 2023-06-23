function openModal(loginFailed) {
  if (loginFailed) {
    var modal = document.getElementById('staticBackdrop');
    modal.classList.add('show');
    modal.style.display = 'block';
  }
}