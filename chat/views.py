from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChatSerializer, QuestionSerializer
from rest_framework import status
from django.shortcuts import render
from .models import Chat
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

def generate_answer(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response["choices"][0]["text"]

class ChatView(APIView):
    def get(self, request):
        chats = Chat.objects.all()
        data = ChatSerializer(chats, many=True)
        return render(request, 'chat/chat.html', {'data': data.data})
    
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save()
            answer = generate_answer(chat.question)
            chat.answer = answer
            chat.save()
            chats = Chat.objects.all()
            data = ChatSerializer(chats, many=True)
            return render(request, 'chat/chat.html', {'data': data.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
