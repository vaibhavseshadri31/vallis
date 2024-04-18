// Setup the Socket.IO connection
var socket = io();

// Event listener for the form submission to send messages
document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const userInputField = document.getElementById('userInput');
    const userMessage = userInputField.value;
    if (!userMessage.trim()) return; // Do not send empty messages

    displayMessage('user', userMessage); // Display the user's message in the chat area
    userInputField.value = ''; // Clear the input field after sending
    disableInput(true); // Disable the input while the bot is "typing"

    socket.emit('send_message', {message: userMessage}); // Send the message to the server via WebSocket
});

// Listen for messages from the server
socket.on('receive_message', function(data) {
    displayMessage('bot', data.message); // Display the bot's response in the chat area
    disableInput(false); // Re-enable the input after the bot's message is fully displayed
});

// Function to display messages in the chat area
function displayMessage(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender); // Apply CSS classes for styling
    chatMessages.appendChild(messageElement);

    let i = 0;
    const speed = 50; // Speed in milliseconds for the typing effect

    function typeWriter() {
        if (i < message.length) {
            messageElement.textContent += message.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        } else {
            chatMessages.scrollTop = chatMessages.scrollHeight; // Automatically scroll to the bottom of the chat area
        }
    }

    typeWriter(); // Start the typing effect
}

// Function to enable or disable the user input field
function disableInput(disabled) {
    document.getElementById('userInput').disabled = disabled;
}
