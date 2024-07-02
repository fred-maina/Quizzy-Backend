from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quizzes(request):
    if request.method == "GET":
        quizzes = Quiz.objects.all()
        quizzes_data = []
        for quiz in quizzes:
            quiz_data = {
                'quiz_code': quiz.code,
                'questions': []
            }
            questions = Question.objects.filter(quiz=quiz)
            for question in questions:
                question_data = {
                    'question': question.question_text,
                    'correct_answer': None,
                    'other_choices': []
                }
                choices = Choice.objects.filter(question=question)
                for choice in choices:
                    if choice.is_correct:
                        question_data['correct_answer'] = choice.choice_text
                    else:
                        question_data['other_choices'].append(choice.choice_text)
                quiz_data['questions'].append(question_data)
            quizzes_data.append(quiz_data)
        response_data = {
            'response_code': status.HTTP_200_OK,
            'quizzes': quizzes_data
        }
        return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, quiz_code):  # Update argument name to match URL configuration
    try:
        quiz = Quiz.objects.get(code=quiz_code)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def questions_by_quiz(request, quiz_code):
    try:
        quiz = Quiz.objects.get(code=quiz_code)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    questions = Question.objects.filter(quiz=quiz)

    questions_data = []
    for question in questions:
        question_data = {
            'question': question.question_text,
            'correct_answer': None,
            'other_choices': []
        }

        choices = Choice.objects.filter(question=question)
        for choice in choices:
            if choice.is_correct:
                question_data['correct_answer'] = choice.choice_text
            else:
                question_data['other_choices'].append(choice.choice_text)

        questions_data.append(question_data)

    response_data = {
        'response_code': status.HTTP_200_OK,
        'quiz_code': quiz.code,
        'questions': questions_data
    }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def create(request):
    # Retrieve questions and choices from request data
    questions = request.data.pop('questions', [])
    choices = [question.pop('choices', []) for question in questions]

    # Add user information to the quiz data
    quiz_data = request.data
    quiz_data['created_by'] = request.user.id  # Assign the logged-in user's ID to created_by

    # Serialize and save the Quiz object
    quiz_serializer = QuizSerializer(data=quiz_data)
    if quiz_serializer.is_valid():
        quiz = quiz_serializer.save()

        # Process each question and its choices
        for question, choice_list in zip(questions, choices):
            question['quiz'] = quiz.id  # Assign quiz ID to each question
            question_serializer = QuestionSerializer(data=question)
            if question_serializer.is_valid():
                saved_question = question_serializer.save()

                # Process each choice for the current question
                for choice in choice_list:
                    choice['question'] = saved_question.id  # Assign question ID to each choice
                    choice_serializer = ChoiceSerializer(data=choice)
                    if choice_serializer.is_valid():
                        choice_serializer.save()
                    else:
                        print(choice_serializer.errors)
            else:
                print(question_serializer.errors)

        return Response({'quiz_code': quiz.code}, status=status.HTTP_201_CREATED)
    else:
        return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
