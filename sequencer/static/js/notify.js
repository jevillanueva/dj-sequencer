window.addEventListener('load', (event) => {
    const messages = document.getElementById('messages');
    const listItems = messages.querySelectorAll('li');
    listItems.forEach((item) => {
        notify(item.textContent, "is-info")
    });
});