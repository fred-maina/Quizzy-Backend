from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question, Choice, Score
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, ScoreSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user_id = request.user.id
    names = request.user.first_name + " " + request.user.last_name
    email = request.user.email
    quiz_details = []
    number_of_people = 0;

    user_quizzes = Quiz.objects.filter(created_by_id=request.user.id)
    for quizz in user_quizzes:
        number_of_people = + Score.objects.filter(quiz=quizz).count()

        quiz_details.append(
            {"quiz_title": quizz.title,
             "quiz_code": quizz.code,
             "quiz_creation_date": quizz.date_created
             })
    response = {"id": user_id, "names": names, "email": email, "quiz_details": quiz_details,
                "number_of_people": number_of_people}
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scores(request, quiz_code):
    quiz = Quiz.objects.get(code=quiz_code)
    user_scores = []
    print(request.user.first_name)
    print(quiz.created_by.first_name)

    if request.user == quiz.created_by:
        print(request.user.first_name)
        print(quiz.created_by.first_name)
        scores = Score.objects.filter(quiz=quiz.id)
        for score in scores:
            user_scores.append({"user": f"{score.user.first_name} {score.user.last_name}",
                                "score": score.score,
                                "taken_on": score.date_taken.strftime('%Y-%m-%d %H:%M:%S')
                                })

        return Response(user_scores)
    return Response({"error": "Action not allowed"},status=status.HTTP_401_UNAUTHORIZED)


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
                    'id': question.id,  # Include question ID
                    'question': question.question_text,
                    'correct_answer': None,
                    'other_choices': []
                }
                choices = Choice.objects.filter(question=question)
                for choice in choices:
                    if choice.is_correct:
                        question_data['correct_answer'] = choice.choice_text
                    question_data['other_choices'].append({
                        'id': choice.id,  # Include choice ID
                        'choice_text': choice.choice_text,
                        'is_correct': choice.is_correct
                    })
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
    if request.user == quiz.created_by:
        Leaderboard = Score.objects.filter(quiz=quiz)
        for score in Leaderboard:
            print(score.score)

    questions = Question.objects.filter(quiz=quiz)
    quiz_creation_date = quiz.date_created.strftime('%Y-%m-%d')
    quiz_creator_name = f"{quiz.created_by.first_name} {quiz.created_by.last_name}"

    questions_data = []
    for question in questions:
        question_data = {
            'id': question.id,  # Include question ID
            'question': question.question_text,
            'choices': []
        }

        choices = Choice.objects.filter(question=question)
        for choice in choices:
            question_data['choices'].append({
                'id': choice.id,  # Include choice ID
                'choice_text': choice.choice_text,
                'is_correct': choice.is_correct
            })

        questions_data.append(question_data)

    response_data = {
        'response_code': status.HTTP_200_OK,
        'quiz_code': quiz.code,
        'title': quiz.title,
        'description': quiz.description,
        'questions': questions_data,
        'quiz_creation_date': quiz_creation_date,
        'quiz_creator_name': quiz_creator_name,
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def update_question(request, quiz_code):
    # Fetch the quiz based on the provided quiz code
    quiz = get_object_or_404(Quiz, code=quiz_code)

    data = request.data

    # Update questions and choices
    questions_data = data.get('questions', [])

    for question_data in questions_data:
        question_id = question_data.get('id', None)

        if question_id:
            # Update existing question
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            if 'question' in question_data:
                question.question_text = question_data['question']
                question.save()
        else:
            # Create new question
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_data.get('question', '')
            )

        # Update or add choices
        choices_data = question_data.get('choices', [])
        for choice_data in choices_data:
            choice_id = choice_data.get('id', None)
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id, question=question)
                choice.choice_text = choice_data.get('choice_text', choice.choice_text)
                choice.is_correct = choice_data.get('is_correct', choice.is_correct)
                choice.save()
            else:
                # Create new choice
                Choice.objects.create(
                    question=question,
                    choice_text=choice_data['choice_text'],
                    is_correct=choice_data.get('is_correct', False)
                )

    return Response({'message': 'Questions and choices updated successfully'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quiz(request, quiz_code):
    try:
        quiz = Quiz.objects.get(code=quiz_code)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    quiz.delete()
    return Response({"detail": "Quiz deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def results(request):
    quiz_code = request.data.get("quiz_code")
    score = request.data.get("score")

    if not quiz_code or score is None:
        return Response(
            {"error": "Quiz code and score are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quiz = get_object_or_404(Quiz, code=quiz_code)
        Score.objects.create(
            quiz=quiz,
            score=score,
            user=request.user
        )
        return Response({"message": "Score saved successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
