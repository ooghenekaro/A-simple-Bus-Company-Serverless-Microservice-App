const apiUrl = 'https://yy1m72qayk.execute-api.eu-west-2.amazonaws.com/v1';

// Function to handle user registration
async function registerUser(email, password) {
    const response = await fetch(`${apiUrl}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    return data;
}

// Function to handle user login
async function loginUser(email, password) {
    const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    return data;
}

// Function to handle booking
async function bookAppointment(user_id, details) {
    const response = await fetch(`${apiUrl}/book`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id, ...details })
    });
    const data = await response.json();
    return data;
}

// Function to handle placing an order
async function placeOrder(user_id, items) {
    const response = await fetch(`${apiUrl}/order`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id, items })
    });
    const data = await response.json();
    return data;
}

// Function to view cart
async function viewCart(user_id) {
    const response = await fetch(`${apiUrl}/view_cart?user_id=${user_id}`, {
        method: 'GET'
    });
    const data = await response.json();
    return data;
}

// Function to send contact message
async function sendContactMessage(message) {
    const response = await fetch(`${apiUrl}/contact`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    });
    const data = await response.json();
    return data;
}

// Example usage
document.getElementById('registerBtn').addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const result = await registerUser(email, password);
    console.log(result);
});
