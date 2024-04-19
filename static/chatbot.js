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

    let i = 0;
    const speed = 20; // Speed in milliseconds for the typing effect
    let typedText = ''; // Accumulator for the typed text

    function typeWriter() {
        if (i < message.length) {
            typedText += message.charAt(i); // Accumulate character by character
            messageElement.innerHTML = converter.makeHtml(typedText); // Convert accumulated text to HTML
            i++;
            setTimeout(typeWriter, speed);
        } else {
            chatMessages.scrollTop = chatMessages.scrollHeight; // Automatically scroll to the bottom of the chat area
        }
    }

    typeWriter(); // Start the typing effect
}

function disableInput(disabled) {
    document.getElementById('userInput').disabled = disabled;
}
