import json
from django.db.models import Case, When, IntegerField
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Choice, Question, PersonalCare, Category, QuizModal, Customer
from .forms import CustomerForm
from .serializers import ChoiceSerializer, QuestionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q, F, Count, Sum


def index(request):
    """wellcome page"""
    context = {
        'form': CustomerForm()
    }
    return render(request, 'quizapp/index.html', context)


@csrf_exempt
def create_customer(request):
    """create_customer """
    data = dict()
    if request.method == "POST":
        emp_id = request.POST.get('employee_id')
        if Customer.objects.filter(employee_id=emp_id).exists():
            user_info = Customer.objects.get(employee_id=emp_id)
            data['exists'] = user_info.employee_id
            data['html_data'] = render_to_string('quizapp/customer_info.html',
            {'user_info': user_info}, request=request)
        else:
            form = CustomerForm(request.POST)
            if form.is_valid():
                fs = form.save()
                data['form_is_valid'] = True
                data['user_info'] = fs.employee_id
            else:
                data['form_is_valid'] = False
        return JsonResponse(data, safe=False)


def skin_quiz(request):
    primary = request.GET.get('primary')
    # category_choice_list = request.GET.getlist('checkbox')
    category_choice = request.GET.getlist('checkbox')
    # category_choice.remove(primary)

    if category_choice and primary:
        questions = Question.objects.filter(category_id__in=category_choice).annotate(
            concern_sort=Case(When(category_id=primary, then=1), default=0, output_field=IntegerField()))
        questions.order_by('-concern_sort')
    else:
        #questions = Question.objects.filter(category__personalcare_id=1).order_by('code')
        questions = Question.objects.filter(category__personalcare_id=1).order_by('code')
        #questions.order_by('code')
        #print(questions.values('code'))
    if primary:
        next_quiz = False
    else:
        next_quiz = True
    context = {
        'questions': questions,
        'next_quiz' : next_quiz
    }
    return render(request, 'quizapp/skin_quiz.html', context)


def skin_concerns(request):
    pc_data = get_object_or_404(PersonalCare, id=2)
    category = Category.objects.filter(personalcare_id=pc_data.id)
    context = {
        'category': category,
        'pc_data': pc_data
    }
    return render(request, 'quizapp/skin_concerns.html', context)


@csrf_exempt
def quiz_answers(request):
    data = dict()
    user_name = request.GET.get('user_name')
    user_choice = request.GET.get('user_choice')
    try:
        customer_obj = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_obj = None

    res = json.loads(user_choice)
    print(res)

    if res:
        for x in res:
            try:
                choice_obj = Choice.objects.get(pk=x)
                quiz_save = QuizModal()
                quiz_save.choice = choice_obj
                quiz_save.customer = customer_obj
                quiz_save.save()
            except ObjectDoesNotExist:
                pass
                #choice_obj = get_object_or_404(Choice, pk=x)
    data = {
        'saved': True
    }
    return JsonResponse(data, safe=False)


STATEMENT  = [
    ("1", "Oily Skin"),
    ("2", "Combination Skin (Slightly Oily)"),
    ("3", "Normal Skin"),
    ("4", "Dry Skin")
]

def quality(q):
    for k,v in STATEMENT:
        if v == q:
            return q


def products(request, user_name):
    try:
        customer_id = Customer.objects.get(employee_id=user_name)
    except ObjectDoesNotExist:
        customer_id = None

    #CustomUser.objects.filter(username__in=created_by).values_list('email', flat=True)
    skin = QuizModal.objects.filter(Q(choice__question__category__code=100) & Q(customer=customer_id))
    #strip_score_sum = skin.filter(choice__question__code__in=[100,101]).aggregate(Sum('choice__marks'))
    strip_score = skin.filter(choice__question__code__in=[100,101]).aggregate(Sum('choice__marks'))['choice__marks__sum'] or 0.00
    print('strip_score: ',strip_score)
    #strip_score = strip_score_sum['choice__marks__sum']
    skin_anls1 = ''
    if strip_score:
        if 7 <= strip_score <= 8:
            skin_anls1 = STATEMENT[0][1]
        elif 5 <= strip_score <= 6:
            skin_anls1 = STATEMENT[1][1]
        elif 3 <= strip_score <= 4:
            skin_anls1 = STATEMENT[2][1]
        elif 1 <= strip_score <= 2:
            skin_anls1 = STATEMENT[3][1]
    
    skin_data2 = QuizModal.objects.filter(Q(choice__question__category__code=100) & ~ Q (choice__question__code__in=[100,101]))
    skin_data2_sum = skin_data2.aggregate(Sum('choice__marks'))
    marks2 = skin_data2_sum['choice__marks__sum']
    skin_anls2 = ''
    
    if marks2:
        if 16 <= marks2 <= 20:
            skin_anls2 = STATEMENT[0][1]
        elif 12 <= marks2 <= 15:
            skin_anls2 = STATEMENT[1][1]
        elif 8 <= marks2 <= 11:
            skin_anls2 = STATEMENT[2][1]
        elif 5 <= marks2 <= 7:
            skin_anls2 = STATEMENT[3][1]

    if skin_anls1 == skin_anls2:
        final_output = skin_anls1
    #Oily Skin
    elif skin_anls1 == STATEMENT[0][1] and skin_anls2 == STATEMENT[1][1]:
        final_output = STATEMENT[0][1] #Oily Skin
    elif skin_anls1 == STATEMENT[0][1] and skin_anls2 == STATEMENT[2][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    elif skin_anls1 == STATEMENT[0][1] and skin_anls2 == STATEMENT[3][1]:
        final_output = STATEMENT[3][1]
    
    #Combination Skin
    elif skin_anls1 == STATEMENT[1][1] and skin_anls2 == STATEMENT[0][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif skin_anls1 == STATEMENT[1][1] and skin_anls2 == STATEMENT[2][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif skin_anls1 == STATEMENT[1][1] and skin_anls2 == STATEMENT[3][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    
     #Normal Skin
    elif skin_anls1 == STATEMENT[2][1] and skin_anls2 == STATEMENT[0][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    elif skin_anls1 == STATEMENT[2][1] and skin_anls2 == STATEMENT[1][1]:
        final_output = STATEMENT[1][1] #Combination Skin
    elif skin_anls1 == STATEMENT[2][1] and skin_anls2 == STATEMENT[3][1]:
        final_output = STATEMENT[2][1] #Normal Skin
    
    #Dry Skin
    elif skin_anls1 == STATEMENT[3][1] and skin_anls2 == STATEMENT[0][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    elif skin_anls1 == STATEMENT[3][1] and skin_anls2 == STATEMENT[1][1]:
        final_output = STATEMENT[3][1] #Dry Skin
    elif skin_anls1 == STATEMENT[3][1] and skin_anls2 == STATEMENT[3][1]:
        final_output = STATEMENT[2][1] #Normal Skin

    context = {
        'skin':skin,
        'strip_score': strip_score,
        'skin_anls1':skin_anls1,
        'marks2':marks2,
        'skin_anls2':skin_anls2,
        'final_output':final_output,
    }
    return render(request, 'quizapp/products.html', context)


@api_view(['GET'])
def question_list(request):
    if request.method =='GET':
        question = Question.objects.all()
        serializer  =QuestionSerializer(question, many=True)
        print(serializer.data)
        return Response(serializer.data)