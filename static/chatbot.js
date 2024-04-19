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

    const urlRegex = /(https?:\/\/[^\s]+)/g;
    let cleanMessage = message.replace(urlRegex, '').trim(); // Remove URLs from the displayed message

    let i = 0;
    const speed = 20; // Speed in milliseconds for the typing effect
    let typedText = ''; // Accumulator for the typed text

    function typeWriter() {
        if (i < cleanMessage.length) {
            typedText += cleanMessage.charAt(i);
            messageElement.innerHTML = converter.makeHtml(typedText);
            i++;
            setTimeout(typeWriter, speed);
        } else {
            // Collect all URLs
            const urls = message.match(urlRegex);
            if (urls && urls.length > 0) {
                const linksButton = document.createElement('button');
                linksButton.textContent = 'View Links';
                linksButton.onclick = function() {
                    showLinksModal(urls); // Function to handle showing the links
                };
                linksButton.classList.add('link-button');
                messageElement.appendChild(linksButton);
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    typeWriter();
}

function showLinksModal(urls) {
    var modal = document.getElementById("linksModal");
    var linksList = document.getElementById("linksList");
    var closeBtn = document.getElementsByClassName("close")[0];

    // Populate the modal with links
    linksList.innerHTML = urls.map(url => `<a href="${url}" target="_blank">${url}</a><br>`).join('');

    // Display the modal
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}





function disableInput(disabled) {
    document.getElementById('userInput').disabled = disabled;
}
