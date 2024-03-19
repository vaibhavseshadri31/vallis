document.getElementById('chatForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    const userInputField = document.getElementById('userInput');
    const userMessage = userInputField.value;

    if (!userMessage.trim()) return; // Don't proceed if the message is only whitespace

    displayMessage('user', userMessage); // Display the user's message in the chat
    
    // Clear the input field after sending the message
    userInputField.value = '';

    // Here, we're appending the user's message as a query parameter for the GET request.
    const apiUrl = '/query?text=' + encodeURIComponent(userMessage);

    // Fetch the response from the API
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.text(); 

        // Display the response in the chat
        displayMessage('bot', data); 
    } catch (error) {
        console.error('Fetch error:', error);
        displayMessage('bot', 'Sorry, I couldn’t fetch the response. Please try again.');
    }
});

// Function to display a message in the chat
function displayMessage(sender, message) {
    const messageElement = document.createElement('div'); 
    messageElement.classList.add('message', sender); // 'user' or 'bot' CSS class
    messageElement.textContent = message;
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.appendChild(messageElement);

    // Automatically scroll to the bottom of the chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
