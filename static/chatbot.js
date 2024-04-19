// Setup the Socket.IO connection
var socket = io();

// Showdown converter setup
var converter = new showdown.Converter();
converter.setOption('simpleLineBreaks', true); // Handles line breaks as expected in chat

document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInputField = document.getElementById('userInput');
    const userMessage = userInputField.value;
    if (!userMessage.trim()) return;

    displayMessage('user', userMessage);
    userInputField.value = '';
    disableInput(true);

    socket.emit('send_message', {message: userMessage});
});

socket.on('receive_message', function(data) {
    displayMessage('bot', data.message);
    disableInput(false);
});

function displayMessage(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    chatMessages.appendChild(messageElement);

    const urlRegex = /(https?:\/\/[^\s]+)/g; // Regex to find URLs
    let cleanMessage = message.replace(urlRegex, '').trim(); // Remove URLs from the message

    let i = 0;
    const speed = 20; // Speed in milliseconds for the typing effect
    let typedText = ''; // Accumulator for the typed text

    function typeWriter() {
        if (i < cleanMessage.length) {
            typedText += cleanMessage.charAt(i); // Accumulate character by character
            messageElement.innerHTML = converter.makeHtml(typedText); // Convert accumulated text to HTML
            i++;
            setTimeout(typeWriter, speed);
        } else {
            // After text is done typing out, check for URLs and create a button
            const urls = message.match(urlRegex);
            if (urls) {
                urls.forEach(url => {
                    const linkButton = document.createElement('button');
                    linkButton.textContent = 'Open Link';
                    linkButton.onclick = function() {
                        window.open(url, '_blank'); // Opens the URL in a new tab
                    };
                    linkButton.classList.add('link-button');
                    messageElement.appendChild(linkButton);
                });
            }
            chatMessages.scrollTop = chatMessages.scrollHeight; // Automatically scroll to the bottom of the chat area
        }
    }

    typeWriter(); // Start the typing effect
}



function disableInput(disabled) {
    document.getElementById('userInput').disabled = disabled;
}
