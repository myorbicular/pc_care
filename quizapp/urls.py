from django.urls import path
from quizapp import views
from quizapp import api

app_name = 'quizapp'

urlpatterns = [
    #api views
    path('', views.index, name='index'),
    path('dummy/', views.dummy, name='dummy'),
    path('skin_quiz/', views.skin_quiz, name='skin_quiz'),
    path('concerns_quiz/', views.concerns_quiz, name='concerns_quiz'),
    path('skin_concerns/<str:user_name>/<str:test_code>/', views.skin_concerns, name='skin_concerns'),
    path('products/<str:user_name>/<str:test_code>/', views.products, name='products'),
    path('test_info/<int:pk>/',views.test_info, name='test_info'),

    #api views
    path('create_customer/', api.create_customer, name='create_customer'),
    path('questions_list/', api.questions_list, name='questions_list'),
    path('quiz_answers/', api.quiz_answers, name='quiz_answers'),
    path('water_info/', api.water_info, name='water_info'),
]
