var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to generate messages dynamically
socket.on('update_messages', function(messages) {
		const messageContainer = document.getElementById('messageContainer');
    const chatBox = messageContainer.querySelector('.chat-box');
    // Clear the existing messages
    chatBox.innerHTML = '';

		messages.forEach(message => {
      if (message.message !== null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'media w-50 mb-3';
        
        messageDiv.innerHTML = `
          <img src="https://res.cloudinary.com/mhmd/image/upload/v1564960395/avatar_usae7z.svg" alt="user" width="50" class="rounded-circle">
          <div class="media-body ml-3">
            <div class="bg-light rounded py-2 px-3 mb-2">
              <p class="text-small mb-0 text-muted">${message.username}: ${message.message}</p>
            </div>
            <p class="small text-muted">${message.timestamp}</p>
          </div>
        `;
        
        messageContainer.querySelector('.chat-box').appendChild(messageDiv);
      }
    });
});

// sendMessage() is triggered from html <input>
async function sendMessage() {

    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();
    
    if (message !== '' && message != null) {
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

function dateNow() {
  var date = new Date();
  var aaaa = date.getFullYear();
  var gg = date.getDate();
  var mm = date.getMonth() + 1;

  if (gg < 10) gg = "0" + gg;

  if (mm < 10) mm = "0" + mm;

  var cur_day = aaaa + "-" + mm + "-" + gg;

  var hours = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();

  if (hours < 10) hours = "0" + hours;

  if (minutes < 10) minutes = "0" + minutes;

  if (seconds < 10) seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}

