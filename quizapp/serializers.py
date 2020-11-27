from .models import Question, Choice, Customer
from rest_framework import serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True,many=True)
    class Meta:
        model = Question
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TestSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)