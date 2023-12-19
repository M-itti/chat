var socket = io();

socket.on('connect', function() {
    var messageData = {
        message: 'Hello, this is a message!',
        user_id: '12345' // Replace this with the actual user ID
    };
    socket.emit('my event', messageData);
});

// Function to send a message
function sendMessage() {
    var messageInput = document.getElementById('message');
    var message = messageInput.value;
    messageInput.value = '';

    if (message.trim() !== '') {
        var chatBox = document.getElementById('chat-box');
        var newMessage = document.createElement('p');
        newMessage.textContent = message;
        chatBox.appendChild(newMessage);

        // Scroll chat box to bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send message to the server using Socket.IO
        socket.emit('my event', { data: message });
    }
}

// Attach the sendMessage function to the button click event
document.getElementById('sendButton').addEventListener('click', sendMessage);
