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
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error('Signup failed with status ' + response.status);
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log('Signup success data:', data);
        // Check for required fields in the response
        if (data.username && data.email) {
            // Proceed to login after successful signup
            const loginPayload = {
                username: email,
                password: password
            };

            return fetch('/authenticate/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(loginPayload)
            });
        } else {
            throw new Error('Signup failed: Missing username or email in response');
        }
    })
    .then(response => {
        console.log('Login response status:', response.status);
        if (!response.ok) {
            throw new Error('Login after signup failed');
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log('Login success data:', data);
        document.cookie = `access=${data.access}; path=/; Secure; SameSite=Lax;`;
        window.location.href = '/dashboard/'; // Redirect to dashboard after successful login
    })
    .catch(error => {
        console.error('Signup or login error:', error);
        alert('Signup or login failed: ' + error.message);
    });
});

// Login form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const csrftoken = getCSRFToken();

    const loginPayload = {
        username: email,
        password: password
    };

    // Perform login request
    fetch('/authenticate/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(loginPayload)
    })
    .then(response => {
        console.log('Login response status:', response.status);
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log('Login success data:', data);
        // Example expiration times from Django
        const ACCESS_TOKEN_LIFETIME_SECONDS = 5 * 24*60*60;  // 5 minutes in seconds
        const REFRESH_TOKEN_LIFETIME_SECONDS = 3 * 24 * 60 * 60;  // 3 days in seconds

        function setCookie(name, value, maxAgeSeconds) {
            const expires = new Date();
            expires.setTime(expires.getTime() + (maxAgeSeconds * 1000)); // Convert seconds to milliseconds
            document.cookie = `${name}=${value}; path=/; Secure; SameSite=Lax; expires=${expires.toUTCString()};`;
        }

        setCookie('access', data.access, ACCESS_TOKEN_LIFETIME_SECONDS);
        setCookie('refresh', data.refresh, REFRESH_TOKEN_LIFETIME_SECONDS);
        window.location="/dashboard/"

    })
    .catch(error => {
        console.error('Login error:', error);
        alert('Login failed: ' + error.message);
    });
});
