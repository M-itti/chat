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
        
        const white  = `
				<div class="media w-50 ml-auto mb-3">
          <div class="media-body ml-3">
            <div class="bg-light rounded py-2 px-3 mb-2">
              <p class="text-small mb-0 text-muted">${message.username}: ${message.message}</p>
            </div>
            <p class="small text-muted">${message.timestamp}</p>
          </div>
				</div>
        `;

				const blue = `
				<div class="media">
					<div class="media-body ml-3">
						<div class="bg-primary rounded py-2 px-3 mb-2">
							<p class="text-small mb-0 text-white">${message.username}: ${message.message}</p>
						</div>
						<p class="small text-muted">${message.timestamp}</p>
					</div>
				</div>
			`;

        if (message.username == localStorage.getItem('username'))
          messageDiv.innerHTML = blue
        else {
          messageDiv.innerHTML = white
        }
        
        messageContainer.querySelector('.chat-box').appendChild(messageDiv);
      }
    });
});

// sendMessage() is triggered from html <input>
async function sendMessage() {

    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();
  	
	// Sanitize the message 
	var message = santizeHTML(message)
	 
    if (message !== '' && message != null) {
        var username = await getUsername();

        // send username and message to server to store it in db
        socket.emit('new_message', { 'username': username, 'message': message, 'timestamp': dateNow()});
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

function sanitizeHTML(str) {
    // Replace potentially harmful characters with HTML entities
    return str.replace(/[&<>"']/g, function(match) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[match];
    });
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
