from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Chat
        
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
    
class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    
    class Meta:
        model = Chat
        fields = 'question',