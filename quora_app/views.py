from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from quora_app.models import Question , Like , Answer


# Authentications :-
def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password , first_name = first_name)
        
        return redirect('quora_app:login')
    return render(request, 'auth/registration.html')

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quora_app:user_dashboard')
        else:
            messages.error(request, 'Username or password is incorrect.')
    
    return render(request, 'auth/login.html')


def user_logout(request):
    logout(request)
    return redirect('quora_app:login')




def user_dashboard(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        
        if request.user.is_authenticated:
            for answer in answers:
                if answer.like_set.filter(user=request.user).exists():
                    answer.liked = True
                else:
                    answer.liked = False
                    
        questions = Question.objects.all()
        
        context = {
                "answers" : answers ,
                "questions" : questions , 
        }
        return render(request , "users/user_dashboard.html" , context)

    questions = Question.objects.all()

    context = {
        "questions" : questions , 
       
    }
    
    return render(request , "users/user_dashboard.html" , context)


@csrf_exempt
def save_question_details(request):
    if request.method == 'POST':
        try:
            user = request.user  
            text = request.POST.get('text', '')
            if text:
                question = Question(user=user, text=text)
                question.save()
                response_data = {'success': True, 'message': 'Question saved successfully.'}
            else:
                response_data = {'success': False, 'message': 'Question text is required.'}
        except Exception as e:
            response_data = {'success': False, 'message': str(e)}
    else:
        response_data = {'success': False, 'message': 'Invalid request method.'}

    return JsonResponse(response_data)


def add_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer_text')
        try:
            answer = Answer(user=request.user, question_id=question_id, text=answer_text)
            answer.save()
            return JsonResponse({'status': 'success', 'message': 'Answer added successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


from django.http import JsonResponse

def get_answers(request):
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        try:
            # Retrieve the last answer by ordering in descending order by ID
            last_answer = Answer.objects.filter(question_id=question_id).order_by('-id').first()
            
            if last_answer is not None:
                answer_data = {'text': last_answer.text}
                return JsonResponse(answer_data)
            else:
                return JsonResponse({}, safe=False)
        except Answer.DoesNotExist:
            return JsonResponse({}, safe=False)
    
    return JsonResponse({}, safe=False)




@login_required
def like_unlike_answer(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        user = request.user
        try:
            
            like = Like.objects.get(user=user, answer=answer)
            
            like.delete()
            liked = False
        except Like.DoesNotExist:

            Like.objects.create(user=user, answer=answer)
            liked = True
        
        
        return JsonResponse({'liked': liked})
    
    



