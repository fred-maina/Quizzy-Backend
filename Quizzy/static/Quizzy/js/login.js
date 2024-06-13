// Function to get CSRF token from meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Toggle between login and signup forms
document.getElementById('toggle-signup').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('login-form').classList.add('d-none');
    document.getElementById('signup-form').classList.remove('d-none');
});

document.getElementById('toggle-login').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('signup-form').classList.add('d-none');
    document.getElementById('login-form').classList.remove('d-none');
});

// Signup form submission
document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const firstName = document.getElementById('first-name').value.trim();
    const lastName = document.getElementById('last-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value.trim();
    const termsAccepted = document.getElementById('terms').checked;
    const csrftoken = getCSRFToken();

    // Validate terms acceptance
    if (!termsAccepted) {
        alert('You must accept the terms and conditions.');
        return;
    }

    // Prepare signup payload
    const signupPayload = {
        username: email,
        password: password,
        email: email,
        first_name: firstName,
        last_name: lastName
    };

    // Perform fetch request to register endpoint
    fetch('/authenticate/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(signupPayload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Signup failed');
        }
        return response.json();
    })
    .then(data => {
        console.log('Signup success data:', data);
        if (data.id) {
            alert('Signup successful');
            document.getElementById('toggle-login').click(); // Switch to login form
        } else {
            throw new Error('Signup failed: Unknown error');
        }
    })
    .catch(error => {
        console.error('Signup error:', error);
        alert(error.message);
    });
});

// Login form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const csrftoken = getCSRFToken();

    // Prepare login payload
    const loginPayload = {
        username: email,
        password: password
    };

    // Perform fetch request to login endpoint
    fetch('/authenticate/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(loginPayload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        console.log('Login success data:', data);
        document.cookie = `access=${data.access}; path=/; httponly`;
        window.location.href = '/dashboard/'; // Redirect to dashboard after successful login
    })
    .catch(error => {
        console.error('Login error:', error);
        alert('Login failed: ' + error.message);
    });
});
