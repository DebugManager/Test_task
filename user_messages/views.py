import json

from clerk import Client
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_messages.models import User, Message
from user_messages.serializers import MessageSerializer


# Create your views here.

class SendMessage(APIView):
    def post(self, request, format=None):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        message_text = request.data.get('message')

        # Validating if sender and receiver exist
        try:
            sender = User.objects.get(pk=sender_id)
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Sender or receiver does not exist."}, status=status.HTTP_404_NOT_FOUND)

        message = Message(sender=sender, receiver=receiver, message=message_text)
        message.save()

        # Optionally, you can return the created message using a serializer
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageBySender(APIView):
    def post(self, request):
        sender_id = request.data.get('sender')
        try:
            sender = User.objects.get(pk=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender does not exist."}, status=status.HTTP_404_NOT_FOUND)
        try:
            messages = Message.objects.filter(sender=sender)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "No user_messages found."}, status=status.HTTP_404_NOT_FOUND)


class MessageByReceiver(APIView):
    def post(self, request):
        receiver_id = request.data.get('receiver')
        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist."}, status=status.HTTP_404_NOT_FOUND)
        try:
            messages = Message.objects.filter(receiver=receiver)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "No user_messages found."}, status=status.HTTP_404_NOT_FOUND)


class GetUser(APIView):
    async def post(self, request):
        user_id = "client_2cOyS4of3ZJqIyRxS2xT3fB8uCd"#request.data.get('user_id')
        async with Client("sk_test_OXYddC61QTqHXTV8U4i8ixwPwwsR21Pm86SbRrsJeh") as client:
            users = await client.users.list()
            for user in users:
                print(f"user {user.id} name {user.first_name}")

        return Response("success")


        # try:
        #     user = User.objects.get(pk=user_id)
        # except User.DoesNotExist:
        #     return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        # try:
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # except User.DoesNotExist:
        #     return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

class GetWebHook(APIView):
    def post(self, request):
        webhook_data = json.loads(request.body.decode("utf-8"))
        return Response(webhook_data)
