from django.test import TestCase

# Create your tests here.
"""
@api_view(['GET'])
def concerns_quiz(request):
    data = dict()
    primary = request.GET.get('primary')
    category_choice = request.GET.getlist('checkbox')
    user_name = request.GET.get('user_name')
    test_code = request.GET.get('test_code')
    specific_concerns = [104, 105, 106]

    customer_obj = Customer.objects.get(employee_id=user_name)
    skin_test_obj = SkinTest.objects.get(code=test_code)
    
    if category_choice and primary:
        print(category_choice)
        #concerns_save.save()
        #for x in category_data:
        #    concerns_save.category.add(x)
        
        questions_data = Question.objects.filter(Q(category_id__in=category_choice) & ~Q(category__code__in=specific_concerns))
        if customer_obj.get_gender_display() == 'Male':
            questions_data = questions_data.filter(~Q(code=119)) #specific_concerns.append(119)

        if questions_data.exists():
            questions = questions_data.annotate(concern_sort=Case(When(category_id=primary, then=1), default=0, output_field=IntegerField()))
            questions.order_by('-concern_sort')
            data['quiz_type'] = 'concerns'
            question = Question.objects.all()
            serializer = QuestionSerializer(question, many=True)
            data['questions'] = serializer.data
    return Response(data)




@api_view(['GET'])
def question_list(request):
    if request.method =='GET':
        question = Question.objects.all()
        serializer  =QuestionSerializer(question, many=True)
        print(serializer.data)
        return Response(serializer.data)


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


"""