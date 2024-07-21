# Quizzy Django Application

## Overview

The Quizzy Django application allows users to create, manage, and take quizzes. It uses Django for the backend, with JWT authentication to secure endpoints. Users can add new quizzes, view quizzes, and take quizzes to get their scores.
## Preview
You can preview Quizzy <a href="https://fchege04.pythonanywhere.com/">Here.</a>
## Features

- **User Authentication**: Secure access to quiz management through JWT.
- **Quiz Management**: Create, view, and take quizzes.
- **Score Calculation**: Calculate and display the final score for quizzes taken.

## Requirements

- Python 3.x
- Django 3.x or later
- Django REST Framework
- Requests library

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/quizzy.git
   cd quizzy
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Setup the database**:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the development server**:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Retrieve All Quizzes with Questions and Choices

- **URL:** `/api/quizzes/`
- **Method:** GET
- **Description:** Retrieves all quizzes along with their associated questions and choices.

### Retrieve Quiz Detail

- **URL:** `/api/quiz/<quiz_code>/`
- **Method:** GET
- **Description:** Retrieves details of a specific quiz identified by its unique `quiz_code`.

### Retrieve Questions by Quiz

- **URL:** `/api/questions/<quiz_code>/`
- **Method:** GET
- **Description:** Retrieves all questions for a specific quiz identified by its `quiz_code`. Each question includes its correct answer and other choices.

### Create Quiz with Questions and Choices

- **URL:** `/api/create/`
- **Method:** POST
- **Description:** Allows authenticated users to create a new quiz with multiple questions and choices. Requires authentication with JWT (JSON Web Token).

#### Request (POST `/api/create/`)

```json
{
  "title": "Sample Quiz",
  "description": "Enter your description here",
  "questions": [
    {
      "question_text": "What is 2 + 2?",
      "choices": [
        {"choice_text": "3", "is_correct": false},
        {"choice_text": "4", "is_correct": true}
      ]
    },
    {
      "question_text": "Which planet is closest to the sun?",
      "choices": [
        {"choice_text": "Earth", "is_correct": false},
        {"choice_text": "Mercury", "is_correct": true}
      ]
    }
  ]
}
```

#### Response (POST `/api/create/`)

```json
{
  "quiz_code": "qz1",
  "status": "Quiz created successfully"
}
```

## Error Responses

- **404 Not Found:** Returned when attempting to retrieve or access a quiz that does not exist.
- **400 Bad Request:** Returned when the request payload is invalid or missing required fields during quiz creation.

## Permissions

- **Authentication:** The API uses JWT (JSON Web Token) authentication. Endpoints like `/api/create/` require the user to be authenticated.
- **Authorization:** Certain endpoints may require additional permissions based on user roles or application requirements.

## Authentication Views

### Register

- **URL:** `/register/`
- **Method:** POST
- **Description:** Allows a new user to register. Requires `username`, `password`, and other user details.

#### Request

```json
{
  "username": "newuser",
  "password": "password123",
  "email": "newuser@example.com"
}
```

#### Response

```json
{
  "id": 1,
  "username": "newuser",
  "email": "newuser@example.com"
}
```

### Login

- **URL:** `/login/`
- **Method:** POST
- **Description:** Allows a user to login with `username` and `password`. Returns JWT tokens if credentials are valid.

#### Request

```json
{
  "username": "existinguser",
  "password": "password123"
}
```

#### Response

```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

### Models and Serializers

- **Models:** `Quiz`, `Question`, `Choice` represent the data structure of quizzes, questions, and choices stored in the database.
- **Serializers:** `RegisterSerializer`, `LoginSerializer`, `QuizSerializer`, `QuestionSerializer`, `ChoiceSerializer` serialize and deserialize data between JSON and Python objects, ensuring data integrity and validation.

## Usage

- Users can interact with the API using HTTP methods (GET, POST) to manage quizzes and quiz-related data.
- Ensure proper authentication and authorization mechanisms are in place to secure sensitive operations and data.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.
