from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice
from .serializers import QuestionSerializer

@api_view(['GET', 'POST'])
def Questions(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        response_data = []

        for question in questions:
            serializer = QuestionSerializer(question)
            question_data = {
                "question": serializer.data['question_text'],
                "correct_answer": None,
                "other_choices": []
            }

            choices = Choice.objects.filter(question=question)

            if choices.exists():
                for choice in choices:
                    if choice.is_correct:
                        question_data['correct_answer'] = choice.choice_text
                    else:
                        question_data['other_choices'].append(choice.choice_text)

            response_data.append(question_data)

        return JsonResponse({"responsecode": 200, "results": response_data})

    elif request.method == 'POST':
        if isinstance(request.data, list):
            serializer = QuestionSerializer(data=request.data, many=True)
        else:
            serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
