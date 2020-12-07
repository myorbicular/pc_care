from .models import Question, Choice, Customer, SkinTest, QuizModal, Hydration
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

    """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Access self.context here to add contextual data into ret
        ret['foo'] = self.context['foo']
        return ret
    """

class TestSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)



class SkinTestSerializer(serializers.ModelSerializer):
    #skintests = CustomerSerializer(many=False, read_only=True)
    #print(skintests.data)
    #category_employee_id = serializers.RelatedField(source='Customer', read_only=True)
    #skintests = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    #customer = CustomerSerializer()
    #customer = CustomerSerializer()
    #customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    
    class Meta:
        model = SkinTest
        fields = '__all__'
        #fields = ('code', 'customer')
    

    """
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        return response
    """


class QuizAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizModal
        fields = '__all__'


class HydrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hydration
        fields = '__all__'

