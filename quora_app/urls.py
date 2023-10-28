from django.urls import path
from quora_app import views

app_name = "quora_app"

urlpatterns = [
    path('Register/', views.registration, name='register'),
    path('', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    
    
    path('Dashboard/', views.user_dashboard, name='user_dashboard'),
    
    path('save_question_details/', views.save_question_details, name='save_question_details'),
    path('get_answers/', views.get_answers, name='get_answers'),
    
    path('add_answer/', views.add_answer, name='add_answer'),
    
    path('like-unlike-answer/<int:answer_id>/', views.like_unlike_answer, name='like_unlike_answer'),

]
