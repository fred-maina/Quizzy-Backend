from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer

class QuizAPITestCase(APITestCase):

    def setUp(self):
        # Set up any initial data for the tests
        self.quiz = Quiz.objects.create(title="Sample Quiz", description="This is a sample quiz")
        self.question = Question.objects.create(quiz=self.quiz, question_text="Sample Question")
        self.choice1 = Choice.objects.create(question=self.question, choice_text="Choice 1", is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question, choice_text="Choice 2", is_correct=False)

    def test_get_quizzes(self):
        # Test the quizzes view
        response = self.client.get('/api/quizzes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quizzes', response.data)
        self.assertEqual(len(response.data['quizzes']), 1)

    def test_get_quiz_detail(self):
        # Test the quiz_detail view
        response = self.client.get(f'/api/quizzes/{self.quiz.code}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertEqual(response.data['description'], self.quiz.description)

    def test_get_questions_by_quiz(self):
        # Test the questions_by_quiz view
        response = self.client.get(f'/api/quizzes/{self.quiz.code}/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quiz_code'], self.quiz.code)
        self.assertEqual(len(response.data['questions']), 1)

    def test_create_quiz(self):
        # Test the create view
        data = {
            "title": "New Quiz",
            "description": "New quiz description",
            "questions": [
                {
                    "question_text": "New Question",
                    "choices": [
                        {"choice_text": "New Choice 1", "is_correct": True},
                        {"choice_text": "New Choice 2", "is_correct": False}
                    ]
                }
            ]
        }
        response = self.client.post('/api/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Quiz.objects.filter(title="New Quiz").exists())
        self.assertTrue(Question.objects.filter(question_text="New Question").exists())
        self.assertTrue(Choice.objects.filter(choice_text="New Choice 1").exists())
