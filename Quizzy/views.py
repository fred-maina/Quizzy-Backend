from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json
import random
from . import user
from api.models import Quiz, Question, Choice
from django.contrib.auth.models import User
from functools import wraps


def jwt_auth_required(view_func, route="/login/"):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access')  # Assuming token is stored in a cookie

        if not token:
            return redirect(route)  # Redirect to login page if token is missing
        try:
            access_token = AccessToken(token)
            current_utc_timestamp = datetime.utcnow().timestamp()

            if access_token['exp'] < current_utc_timestamp:
                raise Exception('Token expired')

            user_id = access_token['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise Exception('User does not exist')

            request.user = user  # Attach the user object to the request

            return view_func(request, *args, **kwargs)

        except Exception as e:
            print(f"JWT verification failed: {e}")
            return redirect(route)

    return wrapper


def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


@jwt_auth_required
def dashboard(request):
    user = request.user
    quizzes = Quiz.objects.filter(created_by=user.id)
    return render(request,
                  "dashboard.html",
                  {"user": user.first_name, "quizzes": quizzes, "BASE_URL": settings.BASE_URL})


@jwt_auth_required
def add(request):
    if request.method == "GET":
        return render(request, "add.html")

    if request.method == 'POST':
        try:
            quiz_name = request.POST.get('quizName', '')
            quiz_description = request.POST.get('quizDescription', '')

            questions = []
            question_counter = 0
            while True:
                question_key = f'question-{question_counter}-text'
                if question_key not in request.POST:
                    break

                question_text = request.POST.get(question_key, '')
                choices = []
                choice_counter = 0
                while True:
                    choice_key_text = f'question-{question_counter}-choice-{choice_counter}-text'
                    choice_key_correct = f'question-{question_counter}-choice-{choice_counter}-correct'
                    if choice_key_text not in request.POST:
                        break

                    choice_text = request.POST.get(choice_key_text, '')
                    choice_correct = request.POST.get(choice_key_correct, '') == 'on'

                    choices.append({
                        'choice_text': choice_text,
                        'is_correct': choice_correct
                    })

                    choice_counter += 1

                questions.append({
                    'question_text': question_text,
                    'choices': choices
                })

                question_counter += 1

            # Prepare data to POST to API
            quiz_data = {
                'title': quiz_name,
                'description': quiz_description,
                'questions': questions
            }

            # Convert to JSON
            # Example: POST to API (replace with your actual API endpoint)
            api_url = f'{settings.BASE_URL}/api/create/'  # Adjust with your actual API endpoint

            # Get access token from cookies
            access_token = request.COOKIES.get('access', '')

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(api_url, headers=headers, json=quiz_data)

            # Check API response
            if response.status_code == 201:
                try:
                    api_response = response.json()
                    quiz_code = api_response.get('quiz_code', 'N/A')
                    return render(request, 'quiz_code.html', {'quiz_code': quiz_code, "BASE_URL": settings.BASE_URL})
                except json.JSONDecodeError as e:
                    return JsonResponse({'success': False, 'error': 'Invalid JSON response from API'})
            else:
                return JsonResponse({'success': False,
                                     'error': f'Failed to create quiz. API returned status code: {response.status_code}'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # Handle other HTTP methods or initial rendering of the form

    return render(request, 'add.html')


@jwt_auth_required
def quiz(request, quiz_code):
    access_token = request.COOKIES.get('access', '')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    api_url = f'{settings.BASE_URL}/api/quizzes/{quiz_code}/questions/'

    # Fetch quiz data
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        quiz_data = response.json()
        questions_data = quiz_data.get('questions', [])
        quiz_title = quiz_data['title']
        quiz_description = quiz_data['description']

        for question in questions_data:
            correct_answer = question.pop('correct_answer')
            other_choices = question.pop('other_choices')
            choices = [correct_answer] + other_choices
            random.shuffle(choices)
            question["correct_answer"] = correct_answer
            question["choices"] = choices

        if request.method == 'POST':
            # Handle quiz submission
            selected_choices = {}
            score = 0
            total_questions = len(questions_data)

            for question_data in questions_data:
                question_text = question_data['question']
                correct_answer = question_data['correct_answer']

                selected_answer = request.POST.get(question_text)

                if selected_answer:
                    selected_choices[question_text] = selected_answer
                    if selected_answer == correct_answer:
                        score += 1
            if total_questions == 0:
                total_questions = +1
            # Calculate the percentage score
            percentage_score = (score / total_questions) * 100

            return render(request, 'final_score.html', context={'percentage_score': percentage_score, 'quiz_code':quiz_code})

        # Prepare context for rendering quiz display template

        context = {
            'quiz_code': quiz_code,
            'title': quiz_title,
            'description': quiz_description,
            'questions': questions_data,
            'quiz_creation_date': quiz_data['quiz_creation_date'],
            'quiz_creator_name': quiz_data['quiz_creator_name']
        }
        return render(request, 'quiz.html', context)

    else:
        return HttpResponse(f"Failed to fetch quiz data. Status code: {response.status_code}",
                            status=response.status_code)
