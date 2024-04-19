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

    // Remove URLs from the message before typing it out
    const cleanMessage = message.replace(/(https?:\/\/[^\s]+)/g, '');

    let i = 0;
    const speed = 20; // Speed in milliseconds for the typing effect
    let typedText = ''; // Accumulator for the typed text

    function typeWriter() {
        if (i < cleanMessage.length) {
            typedText += cleanMessage.charAt(i);
            messageElement.innerHTML = converter.makeHtml(typedText); // Convert accumulated text to HTML
            i++;
            setTimeout(typeWriter, speed);
        } else {
            chatMessages.scrollTop = chatMessages.scrollHeight; // Automatically scroll to the bottom of the chat area
            // Add buttons for each URL after the message is typed out
            addLinkButtons(message, messageElement);
        }
    }

    typeWriter(); // Start the typing effect
}

function addLinkButtons(text, container) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    let match;
    const linksContainer = document.createElement('div');  // Container for all link buttons
    linksContainer.classList.add('links-container');  // Apply flex styles if using flex

    while ((match = urlRegex.exec(text)) !== null) {
        const url = match[0];
        const linkButton = document.createElement('button');
        let splitArray = url.split("/");
        linkButton.textContent = splitArray[splitArray.length - 1];
        linkButton.onclick = function() {
            window.open(url, '_blank');
        };
        linkButton.classList.add('link-button');
        linksContainer.appendChild(linkButton);  // Append each button to the container
    }

    if (linksContainer.hasChildNodes()) {
        container.appendChild(linksContainer);  // Only append if there are buttons
    }
}



// function showLinksModal(urls) {
//     var modal = document.getElementById("linksModal");
//     var linksList = document.getElementById("linksList");
//     var closeBtn = document.getElementsByClassName("close")[0];

//     // Populate the modal with links
//     linksList.innerHTML = urls.map(url => `<a href="${url}" target="_blank">${url}</a><br>`).join('');

//     // Display the modal
//     modal.style.display = "block";

//     // When the user clicks on <span> (x), close the modal
//     closeBtn.onclick = function() {
//         modal.style.display = "none";
//     }

//     // When the user clicks anywhere outside of the modal, close it
//     window.onclick = function(event) {
//         if (event.target == modal) {
//             modal.style.display = "none";
//         }
//     }
// }


function disableInput(disabled) {
    document.getElementById('userInput').disabled = disabled;
}
