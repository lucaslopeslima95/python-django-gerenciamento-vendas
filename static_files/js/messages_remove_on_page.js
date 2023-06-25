function remove_messages() {
    setTimeout(function () {
        var messages = document.querySelector('.alert');
        if (messages) {
            messages.remove();
        }
    }, 2000);
}