document.addEventListener('DOMContentLoaded', function() {
  window.addEventListener('scroll', fadeInSections);
  fadeInSections();
  
  // Smooth scroll for anchor links remains the same
});

// Simulate a smoother interaction for button clicks
function displayMessage() {
  const messageBox = document.createElement('div');
  messageBox.style.position = 'fixed';
  messageBox.style.bottom = '20px';
  messageBox.style.right = '20px';
  messageBox.style.padding = '10px 20px';
  messageBox.style.borderRadius = '5px';
  messageBox.style.background = 'rgba(40, 167, 69, 0.9)'; // Match button color
  messageBox.style.color = 'white';
  messageBox.style.fontSize = '16px';
  messageBox.innerText = 'Thank you for your interest in Vallis! We will get back to you soon.';
  document.body.appendChild(messageBox);

  // Fade out the message box after 4 seconds
  setTimeout(function() {
      messageBox.style.transition = 'opacity 0.5s ease-in-out';
      messageBox.style.opacity = '0';
      setTimeout(function() {
          document.body.removeChild(messageBox);
      }, 500); // Align with transition
  }, 4000);
}
