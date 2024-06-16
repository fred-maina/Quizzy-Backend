from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json

def jwt_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access')  # assuming token is stored in cookie

        if not token:
            return redirect('/login/')  # Redirect to login page if token is missing

        try:
            access_token = AccessToken(token)
            current_utc_timestamp = datetime.utcnow().timestamp()

            if access_token['exp'] < current_utc_timestamp:
                raise AccessToken.DoesNotExist

            # Optionally, validate user permissions or other checks here
            # Example: user = User.objects.get(id=access_token['user_id'])

            return view_func(request, *args, **kwargs)

        except Exception as e:
            print(f"JWT verification failed: {e}")
            return render(request, "login.html", {"error_message": "Access denied"})  # Render an error page or handle the error as needed

    return wrapper


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, "login.html")

@jwt_auth_required
def dashboard(request):
    return render(request, "dashboard.html")


def add(request):
    if request.method =="GET":
        render(request,"add.html")
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
            
            response = requests.post(api_url, json=quiz_data)
            
            # Check API response
            if response.status_code == 201:
                try:
                    api_response = response.json()
                    quiz_code = api_response
                    return render(request, 'quiz_code.html', {'quiz_code': quiz_code})
                except json.JSONDecodeError as e:
                    return JsonResponse({'success': False, 'error': 'Invalid JSON response from API'})
            
            else:
                return JsonResponse({'success': False, 'error': f'Failed to create quiz. API returned status code: {response.status_code}'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Handle other HTTP methods or initial rendering of the form
    return render(request, 'add.html')