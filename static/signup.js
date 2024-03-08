document.getElementById('signupForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const description = document.getElementById('description').value;

    const apiEndpoint = '/user_data?text=' + encodeURIComponent(description);

    try {
        // Making a POST request to the specified endpoint
        const response = await fetch(apiEndpoint);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.text(); // Assuming the response is JSON

        // Handle success - you might want to redirect the user or display a success message
        
        // Redirect or display success message
        // window.location.href = 'successPage.html'; // Example redirection
    } catch(error) {
        console.error('Signup failed:', error);
        // Handle the error - you might want to display an error message to the user
        alert('Signup failed. Please try again.');
    }

    // Basic validation (Further validation can be added)
    if(name && email && password && description) {
        // Here you would typically send the data to the server
        // For demonstration purposes, we'll just reset the form
        this.reset();
        window.location.href = "/phil"
    } else {
        alert('Please fill out all fields.');
    }
});
