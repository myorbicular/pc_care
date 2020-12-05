from .serializers import ChoiceSerializer, QuestionSerializer, CustomerSerializer, TestSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
#from rest_framework.exceptions import ValidationError, ObjectDoesNotExist
#from django_filters import rest_framework as filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
import json
from .models import *
from .serializers import *
#from .models import Choice, Question, PersonalCare, Category, QuizModal, Customer, Hydration, Concerns, Products, Skin_profile, SkinTest


@api_view(['GET','POST'])
def create_customer(request):
    data = dict()
    if request.method == "GET":
        emp_id = request.query_params['employee_id']
        if Customer.objects.filter(employee_id=emp_id).exists():
            user_info = Customer.objects.get(employee_id=emp_id)
            serializer = CustomerSerializer(user_info)
            data['user_info'] = serializer.data
            try:
                top = SkinTest.objects.filter(customer=user_info).order_by('-code')[0]
                if top:
                    data['test_code'] = top.code + 1
            except IndexError:
                data['test_code'] = 1
        return Response(data)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['user_name'] = request.data['employee_id']
            data['test_code'] = 1
            data['status'] = status.HTTP_201_CREATED
        else:
            data['status'] = status.HTTP_400_BAD_REQUEST
    return Response(data)


@api_view(['GET'])
def questions_list(request):
    data = dict()
    #print("request.headers :", request.headers)
    
    if request.method == "GET":
        user_name = request.GET['user_name']
        test_code = request.GET['test_code']
        
        dummy = request.headers.get('test_code')
        print(dummy)
        customer_obj = Customer.objects.get(employee_id=user_name)
        
        if user_name:
            skin_test_obj = SkinTest()
            skin_test_obj.code = test_code
            skin_test_obj.customer = customer_obj
            skin_test_obj.save()
            questions = Question.objects.filter(category__personalcare_id=1).order_by('code')
            serializer = QuestionSerializer(questions, many=True)
            data['questions'] = serializer.data
            data['quiz_type'] = 'skin'
            return Response(data)


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


@api_view(['GET'])
def questions_test(request):
    data = dict()

    if request.method == "GET":
        user_name = request.GET['user_name']
        test_code = request.GET['test_code']
        query_p1 = request.query_params['test_code']
        #dummy = request.headers.get('test_code')
        #print(request.headers)
        print("query_p1 :", query_p1)
        customer_obj = Customer.objects.get(employee_id=user_name)
        
        return Response(data)

        """
        if user_name:
            questions = Question.objects.filter(category__personalcare_id=1).order_by('code')
            serializer = QuestionSerializer(questions, many=True)
            data['questions'] = serializer.data
            data['quiz_type'] = 'skin'
            return Response(data)
        """

"""
class QuestionsTest(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_fields = ('id',)


class QuestionsTest(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('id', 'category',)
    search_fields = ['id']
    ordering_fields = ['id']

"""
#questions = Question.objects.filter(category__personalcare_id=1).order_by('-category_id')

class QuestionsTest1(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('category__personalcare_id',)    
    ordering_fields = ['id']
    ordering = ['-category_id']


class Quiz1(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(category__personalcare_id=1).order_by('-category_id')


class Quiz2(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(category__personalcare_id=1).order_by('-category_id')