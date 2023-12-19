socket = io();

socket.on('connect', function() {
    // Do nothing or handle any specific connection behavior here
});

socket.on('message', function(msg) {
    var chatBox = document.getElementById('chat-box');
    var newMessage = document.createElement('p');
    newMessage.textContent = msg;
    chatBox.appendChild(newMessage);

    // Scroll chat box to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
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
        socket.emit('my event', { message: message });
    }
}

// Attach the sendMessage function to the button click event
document.getElementById('sendButton').addEventListener('click', sendMessage);

// Fetch previous messages from the server when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // You may want to emit an event to request previous messages from the server here
    // For instance: socket.emit('get_previous_messages');
});

