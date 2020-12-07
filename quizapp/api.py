from .serializers import (ChoiceSerializer, QuestionSerializer, CustomerSerializer,
                            TestSerializer, QuizAnsSerializer, HydrationSerializer)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import Http404
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


def get_customer_obj(uname):
    try:
        return Customer.objects.get(employee_id=uname)
        #return Customer.objects.filter(employee_id=uname)
    except Customer.DoesNotExist:
        raise Http404

def get_test_code():
    try:
        top = SkinTest.objects.all().order_by('-code')[0]
        #top = SkinTest.objects.filter(customer=user_info).order_by('-code')[0]
        if top:
            test_code = top.code + 1
    except IndexError:
        test_code = 1
    return test_code


# Response Function
def responsedata(status, message, code, data={}):
    if status:
        return {"success":status,"data":data,"code":code,"message":message}
    else:
        return {"success":status,"data":{},"code":code,"message":message}

#first api
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('employee_id',)    


#second api
class Quiz1(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(category__personalcare_id=1).order_by('-category_id')#[:3]



class SkinTestCreate(generics.ListCreateAPIView):
    queryset = SkinTest.objects.all()
    serializer_class = SkinTestSerializer


class CreateListModelMixin(object):

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


class QuizAnswers(CreateListModelMixin, generics.ListCreateAPIView):
    queryset = QuizModal.objects.all()
    serializer_class = QuizAnsSerializer


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


class HydrationInfo(generics.ListCreateAPIView):
    queryset = Hydration.objects.all()
    serializer_class = HydrationSerializer


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



class Quiz2(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(category__personalcare_id=1).order_by('-category_id')



#class CompanyContactViewSet(viewsets.ModelViewSet):
class SkinTestCreate3(generics.ListCreateAPIView):
    serializer_class = SkinTestSerializer


    def create(self, validated_data):
        serializer = self.get_serializer(data=self.request.data)
        uname =  self.request.data.pop('user_name')
        #customer_instance = Customer.objects.filter(employee_id=uname).first()
        customer_instance = Customer.objects.get(employee_id=uname)
        
        if not serializer.is_valid():
            #print(serializer.errors)
            print("data :", serializer.data)
            data = serializer.validated_data
            serializer.save(customer=customer_instance)
            #headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)