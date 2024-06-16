
## Quizzy API

### Overview

The Quizzy API allows users to manage quizzes, questions, and choices through a set of RESTful endpoints. It provides functionalities for retrieving quiz details, retrieving questions by quiz, retrieving all quizzes with their questions and choices, and creating new quizzes with associated questions and choices.

### Endpoints

#### 1. **Retrieve All Quizzes with Questions and Choices**

- **URL:** `/api/quizzes/`
- **Method:** GET
- **Description:** Retrieves all quizzes along with their associated questions and choices.

#### 2. **Retrieve Quiz Detail**

- **URL:** `/api/quiz/<quiz_code>/`
- **Method:** GET
- **Description:** Retrieves details of a specific quiz identified by its unique `quiz_code`.

#### 3. **Retrieve Questions by Quiz**

- **URL:** `/api/questions/<quiz_code>/`
- **Method:** GET
- **Description:** Retrieves all questions for a specific quiz identified by its `quiz_code`. Each question includes its correct answer and other choices.

#### 4. **Create Quiz with Questions and Choices**

- **URL:** `/api/create/`
- **Method:** POST
- **Description:** Allows authenticated users to create a new quiz with multiple questions and choices. Requires authentication with JWT (JSON Web Token).

### Request and Response Formats

#### Request (POST `/api/create/`)

```json
{
  "title": "Sample Quiz",
  "description":"Enter your description here"

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

#### Error Responses

- **404 Not Found:** Returned when attempting to retrieve or access a quiz that does not exist.
- **400 Bad Request:** Returned when the request payload is invalid or missing required fields during quiz creation.

### Permissions

- **Authentication:** The API uses JWT (JSON Web Token) authentication. Endpoints like `/api/create/` require the user to be authenticated.
- **Authorization:** Certain endpoints may require additional permissions based on user roles or application requirements.

### Models and Serializers

- **Models:** `Quiz`, `Question`, `Choice` represent the data structure of quizzes, questions, and choices stored in the database.
- **Serializers:** `QuizSerializer`, `QuestionSerializer`, `ChoiceSerializer` serialize and deserialize data between JSON and Python objects, ensuring data integrity and validation.

### Dependencies

- **Django REST Framework:** Provides robust tools for building APIs in Django, including serializers, views, permissions, and authentication classes.

### Usage

- Users can interact with the API using HTTP methods (GET, POST) to manage quizzes and quiz-related data.
- Ensure proper authentication and authorization mechanisms are in place to secure sensitive operations and data.