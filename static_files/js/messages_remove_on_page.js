function remove_messages() {
    
    setTimeout(function () {
        var messages = document.querySelector('.alert');
        if (messages) {
            messages.remove();
        }
    }, 4000);

    setTimeout(function () {
        var messages = document.querySelector('.errorlist');
        if (messages) {
            messages.remove();
        }
    }, 4000);
    
    
}