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
from api.models import Quiz, Question, Choice
from django.contrib.auth.models import User
from functools import wraps


def jwt_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access')  # Assuming token is stored in a cookie

        if not token:
            return redirect('/login/')  # Redirect to login page if token is missing

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
            return render(request, "login.html", {"error_message": "Access denied"})  # Handle the error as needed

    return wrapper

def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, "login.html")


@jwt_auth_required
def dashboard(request):
    user = request.user
    quizzes = Quiz.objects.filter(created_by=user.id)
    print(user)
    return render(request, "dashboard.html", {"user": user.first_name,"quizzes":quizzes})


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
            quiz_data_json = json.dumps(quiz_data)
            print(quiz_data_json)
            print(type(quiz_data_json))

            # Example: POST to API (replace with your actual API endpoint)
            api_url = 'http://127.0.0.1:8000/api/create/'  # Adjust with your actual API endpoint

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
                    return render(request, 'quiz_code.html', {'quiz_code': quiz_code})
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
def display_quiz(request, quiz_code):
    access_token = request.COOKIES.get('access', '')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    api_url = f'{settings.BASE_URL}/api/quizzes/{quiz_code}/questions/'  # Adjust BASE_URL as per your settings
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        try:
            quiz_data = response.json()
            questions_data = quiz_data.get('questions', [])

            # Fetch quiz metadata using Quiz model
            quiz = get_object_or_404(Quiz, code=quiz_code)
            quiz_creation_date = quiz.date_created.strftime('%Y-%m-%d')  # Format creation date as needed
            quiz_creator_name = f"{quiz.created_by.first_name} {quiz.created_by.last_name}"  # Combine first and last name
            print(quiz.created_by.first_name)
            print(questions_data)
            for question in questions_data:
                correct_answer = question.pop('correct_answer')
                other_choices = question.pop('other_choices')
                choices= [correct_answer] + other_choices
                question["choices"]=choices
            print(questions_data)
            # Prepare context for rendering quiz display template
            context = {
                'quiz_code': quiz_code,
                'title':quiz.title,
                'description':quiz.description,
                'questions': questions_data,
                'quiz_creation_date': quiz_creation_date,
                'quiz_creator_name': quiz_creator_name
            }
            return render(request, 'quiz.html', context)
        except Exception as e:
            return HttpResponse(f"Error fetching or parsing quiz data: {e}", status=500)
    else:
        return HttpResponse(f"Failed to fetch quiz data. Status code: {response.status_code}", status=response.status_code)

def leaderboard(request):
    if request.method == 'POST':
        correct_answers = request.session.get('correct_answers')
        number_of_questions = int(request.session.get('number_of_questions', 0))
        correct_questions = 0# Iterate over each question and compare the selected answer with the correct answer
        for question, correct_answer in correct_answers.items():
            selected_answer = request.POST.get(question)
            if selected_answer == correct_answer:
                correct_questions += 1

            # Calculate the percentage of correct questions
            percentage = int((correct_questions / number_of_questions) * 100 if number_of_questions != 0 else 0)

            # Pass the score data to the template
            context = {
                'total_questions': number_of_questions,
                'correct_questions': correct_questions,
                'percentage': percentage
            }
            return render(request, 'finalscore.html', context)
        else:
         return render(request, 'index.html')  # R'''