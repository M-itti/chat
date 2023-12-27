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
        var username = getUsername();
        socket.emit('new_message', { 'username': username, 'message': message });
        messageInput.value = '';
    }
}

function getUsername() {
    var storedUsername = localStorage.getItem('username');
    if (storedUsername) {
        return storedUsername;
    } else {
        var username = prompt('Enter your username:');
        username = username ? username.trim() : 'Anonymous';
        localStorage.setItem('username', username);
        return username;
    }
}

