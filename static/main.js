var socket = io.connect('http://' + document.domain + ':' + location.port);

// html input -> js (sendMessage) -> flask stores message to db -> js up    date_messages

// update messages onboard which is received from server
socket.on('update_messages', function(messages) {
    var ul = document.getElementById('messages');
    ul.innerHTML = '';
    messages.forEach(function(msg) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(msg.username + ': ' + msg.message));
        ul.appendChild(li);
    });
});

// sendMessage() is triggered from html
async function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();
    
    if (message !== '') {
        var username = await getUsername();
				console.log(username);

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
            console.log('Username:', data.username);
          return data.username
            // Now you can use this username in your front-end code
        } else {
            console.log('Username not found');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call getUsername() function wherever needed in your front-end JavaScript



/*
function getUsername() {
    var storedUsername = sessionStorage.getItem('username');
    if (storedUsername) {
        return storedUsername;
    } else {
        var username = prompt('Enter your username:');
        username = username ? username.trim() : 'Anonymous';
        sessionStorage.setItem('username', username);
        return username;
    }
}

*/
