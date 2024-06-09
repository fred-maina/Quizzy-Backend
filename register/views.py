from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer

@api_view(['GET', 'POST'])
def quizzes(request):
    if request.method == 'GET':
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        quiz_serializer = QuizSerializer(data=request.data)
        if quiz_serializer.is_valid():
            quiz = quiz_serializer.save()
            # Return code to avoid serialization issues
            return Response({'quiz_code': quiz.code}, status=status.HTTP_201_CREATED)
        else:
            return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def quiz_detail(request, quiz_code):  # Update argument name to match URL configuration
    try:
        quiz = Quiz.objects.get(code=quiz_code)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizSerializer(quiz)
    return Response(serializer.data)

@api_view(['GET'])
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
            'choices': []
        }
        
        choices = Choice.objects.filter(question=question)
        for choice in choices:
            choice_data = {
                'id': choice.id,
                'choice_text': choice.choice_text,
                'is_correct': choice.is_correct
            }
            question_data['choices'].append(choice_data)
            
        questions_data.append(question_data)
    
    response_data = {
        'response_code': status.HTTP_200_OK,
        'quiz_code': quiz.code,
        'questions': questions_data
    }
    return Response(response_data)
