import json
from django.db.models import Case, When, IntegerField
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Choice, Question, PersonalCare, Category, QuizModal, Customer, Hydration, Concerns, Products, Skin_profile, SkinTest
from .forms import CustomerForm
from .serializers import ChoiceSerializer, QuestionSerializer, CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q, F, Count, Sum, Avg
from .result import *
from .score import oil_dry_anls, sen_res_anls, acne_anls, pigmentation_anls, ageing_anls, product_info

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
            data['user_name'] = user_info.employee_id
            question = Customer.objects.all()
            serializer = CustomerSerializer(user_info)
            data['user_info'] = serializer.data
            try:
                top = SkinTest.objects.filter(customer=user_info).order_by('-code')[0]
                print('CODE:',top.code)
                if top:
                    data['test_code'] = top.code + 1
            except IndexError:
                data['test_code'] = 1
            context = {
                'user_info': user_info,
                'test_code': data['test_code']
            }
            data['html_data'] = render_to_string('quizapp/customer_info.html', context, request=request)
        else:
            form = CustomerForm(request.POST)
            if form.is_valid():
                fs = form.save()
                data['form_is_valid'] = True
                data['user_name'] = fs.employee_id
                data['test_code'] = 1
            else:
                data['form_is_valid'] = False
        return JsonResponse(data, safe=False)


def skin_quiz(request, user_name, test_code):
    data = dict()
    customer_obj = Customer.objects.get(employee_id=user_name)

    if user_name:
        skin_test_obj = SkinTest()
        skin_test_obj.code = test_code
        skin_test_obj.customer = customer_obj
        skin_test_obj.save()
        data['questions'] = Question.objects.filter(category__personalcare_id=1).order_by('code')
        #questions = Question.objects.filter(code__in=[107,108,109]).order_by('code')
        data['quiz_type'] = 'skin'
    return render(request, 'quizapp/skin_quiz.html', data)


def skin_concerns(request, user_name, test_code):
    pc_data = get_object_or_404(PersonalCare, id=2)
    oil_dry_ctx = oil_dry_anls(test_code)
    skin_type = oil_dry_ctx['oil_dry_analysis']

    if skin_type in ['Combination Skin (Slightly Oily)', 'Oily Skin']:
        category = Category.objects.filter(Q(personalcare_id=pc_data.id) & ~Q(code=104))
    elif skin_type in ['Dry Skin', 'Normal Skin']:
        category = Category.objects.filter(Q(personalcare_id=pc_data.id) & ~Q(code=105))
    else:
        category = Category.objects.filter(personalcare_id=pc_data.id)
        
    
    context = {
        'category': category,
        'pc_data': pc_data,
        'oil_dry_ctx' : oil_dry_ctx
    }
    return render(request, 'quizapp/skin_concerns.html', context)


def concerns_quiz(request):
    primary = request.GET.get('primary')
    category_choice = request.GET.getlist('checkbox')
    user_name = request.GET.get('user_name')
    test_code = request.GET.get('test_code')
    specific_concerns = [104, 105, 106]

    customer_obj = Customer.objects.get(employee_id=user_name)
    skin_test_obj = SkinTest.objects.get(code=test_code)

    if category_choice and primary:
        category_data  = Category.objects.filter(pk__in=category_choice)
        concerns_save = Concerns()
        concerns_save.customer = customer_obj
        concerns_save.is_primary = Category.objects.get(pk=primary)
        concerns_save.skin_test = skin_test_obj
        concerns_save.save()
        for x in category_data:
            concerns_save.category.add(x)
        
        questions_data = Question.objects.filter(Q(category_id__in=category_choice) & ~Q(category__code__in=specific_concerns))
        if customer_obj.get_gender_display() == 'Male':
            questions_data = questions_data.filter(~Q(code=119)) #specific_concerns.append(119)

        if questions_data.exists():
            questions = questions_data.annotate(concern_sort=Case(When(category_id=primary, then=1), default=0, output_field=IntegerField()))
            questions.order_by('-concern_sort')
        else:
            return redirect('quizapp:products', user_name=customer_obj.employee_id, test_code=test_code)

    context = {
        'questions': questions,
        'quiz_type': 'concerns'
    }
    return render(request, 'quizapp/skin_quiz.html', context)


@csrf_exempt
def quiz_answers(request):
    data = dict()
    user_name = request.GET.get('user_name')
    user_choice = request.GET.get('user_choice')
    test_code = request.GET.get('test_code')
    choice_data = json.loads(user_choice)

    customer_obj = Customer.objects.get(employee_id=user_name)
    skin_test_obj = SkinTest.objects.get(code=test_code)

    if choice_data:
        for x in choice_data:
            try:
                choice_obj = Choice.objects.get(pk=x)
                quiz_save = QuizModal()
                quiz_save.choice = choice_obj
                quiz_save.customer = customer_obj
                quiz_save.skin_test = skin_test_obj
                quiz_save.save()
            except ObjectDoesNotExist:
                pass
                #choice_obj = get_object_or_404(Choice, pk=x) 
    data = {
        'saved': True
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def water_info(request):
    data = dict()
    if request.method == "POST":
        test_code = request.POST.get('test_code')
        user_name = request.POST.get('user_name')
        weight = request.POST.get('weight')
        physical_activity = request.POST.get('physical_activity')
        water_intake = request.POST.get('water_intake')
        status = request.POST.get('status')
        
        if Customer.objects.filter(employee_id=user_name).exists():
            customer_obj = Customer.objects.get(employee_id=user_name)
            skin_test_obj = SkinTest.objects.get(code=test_code)
            water_save = Hydration()
            water_save.customer = customer_obj
            water_save.weight = weight
            water_save.physical_activity = physical_activity
            water_save.water_intake = water_intake
            water_save.status = status
            water_save.skin_test = skin_test_obj
            water_save.save()
            data['is_valid'] = True
        else:
           data['is_valid'] = False
    return JsonResponse(data, safe=False)

def products(request, user_name, test_code):            
    oil_dry_ctx = oil_dry_anls(test_code)
    sen_res_ctx = sen_res_anls(test_code)
    acne_anls_ctx = acne_anls(test_code)
    pigmentation_anls_ctx = pigmentation_anls(test_code)
    ageing_anls_ctx = ageing_anls(test_code)
    concern_obj = Concerns.objects.get(skin_test__code=test_code)
    product_data = product_info(test_code, concern_obj, oil_dry_ctx, sen_res_ctx, acne_anls_ctx)
    test_data = SkinTest.objects.filter(customer__employee_id=user_name)

    context = {
        'oil_dry_ctx' : oil_dry_ctx,
        'sen_res_ctx' : sen_res_ctx,
        'acne_anls_ctx' : acne_anls_ctx,
        'pigmentation_anls_ctx' : pigmentation_anls_ctx,
        'ageing_anls_ctx' : ageing_anls_ctx,
        'concerns' : concern_obj,
        'pro_obj' : product_data,
        'test_data' : test_data,
        'user_name' : user_name
    }
    return render(request, 'quizapp/products.html', context)


def test_info(request, pk):
    skin_test_obj = SkinTest.objects.get(pk=pk)
    print(skin_test_obj.id)
    oil_dry_ctx = oil_dry_anls(skin_test_obj.code)
    sen_res_ctx = sen_res_anls(skin_test_obj.code)
    acne_anls_ctx = acne_anls(skin_test_obj.code)
    pigmentation_anls_ctx = pigmentation_anls(skin_test_obj.code)
    ageing_anls_ctx = ageing_anls(skin_test_obj.code)
    concern_obj = Concerns.objects.get(skin_test=skin_test_obj.pk)
    product_data = product_info(skin_test_obj.code, concern_obj, oil_dry_ctx, sen_res_ctx, acne_anls_ctx)

    context = {
        'oil_dry_ctx' : oil_dry_ctx,
        'sen_res_ctx' : sen_res_ctx,
        'acne_anls_ctx' : acne_anls_ctx,
        'pigmentation_anls_ctx' : pigmentation_anls_ctx,
        'ageing_anls_ctx' : ageing_anls_ctx,
        'concerns' : concern_obj,
        'pro_obj' : product_data,
        'test_data' : skin_test_obj
    }
    return render(request, 'quizapp/test_info.html', context)