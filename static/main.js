var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update_messages', function(messages) {
    var ul = document.getElementById('messages');
    ul.innerHTML = '';
    messages.forEach(function(msg) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(msg.username + ': ' + msg.message));
        ul.appendChild(li);
    });
});

function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();
    if (message !== '') {
        socket.emit('new_message', { 'username': getUsername(), 'message': message });
        messageInput.value = '';
    }
}

function getUsername() {
    var username = prompt('Enter your username:');
    return username ? username.trim() : 'Anonymous';
}

