var socket = io.connect('http://' + document.domain + ':' + location.port);

// update messages onboard which is received from server
socket.on('update_messages', function(messages) {
    var ul = document.getElementById('messages');
    ul.innerHTML = '';
    messages.forEach(function(msg) {
      if (msg.message !== null) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(msg.username + ': ' + msg.message));
        ul.appendChild(li);
      }
    });
});

// sendMessage() is triggered from html
async function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();
    
    if (message !== '') {
        var username = await getUsername();

        // send username and message to server to store it in db
        socket.emit('new_message', { 'username': username, 'message': message });
        messageInput.value = '';
    }
}

async function getUsername() {
    try {
        const response = await fetch('/get_name');
        const data = await response.json();

        if (data.username) {
          return data.username
        } else {
            console.log('Username not found');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

