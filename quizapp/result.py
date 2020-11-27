from django.db.models import Q, F, Count, Sum, Avg
from django.core.exceptions import ObjectDoesNotExist
from quizapp.models import Choice, Question, PersonalCare, Category, QuizModal, Customer, Hydration, Skin_profile


def get_strip_sum(customer_id):
    skin = QuizModal.objects.filter(Q(choice__question__category__code=100) & Q(customer=customer_id))
    obj_sum = skin.filter(choice__question__code__in=[100,101]).aggregate(strip_score=Sum('choice__marks'))
    return obj_sum

def getStatus(cat_code, score):
    print(type(score))
    #obj = Skin_profile.objects.filter(Q(category__code=cat_code) & Q(from_score=from_arg) & Q(to_score=to_arg))
    obj = Skin_profile.objects.filter(Q(category__code=cat_code) & Q(from_score__lte=5) & Q(to_score__gte=5))
    obj1 = Skin_profile.objects.filter(category__code=cat_code)
    obj2 = obj1.filter(from_score__gte=5)
    obj3 = obj2.filter(to_score__gte=5)
    #Item.objects.filter(price__range=(min_price, max_price))
    return obj3