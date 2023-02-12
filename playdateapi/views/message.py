from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Message
from playdateapi.models import User

class MessageView(ViewSet):
    """Message View"""
    def retrieve(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        sender = User.objects.get(id=request.data["id"])
        receiver = User.objects.get(id=request.data["id"])
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=request.data["content"],
            created_on=request.data["created_on"]
          )
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    
    def update(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.content = request.data["content"]
        message.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Handle DELETE requests for a single post"""
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class MessageSerializer(serializers.ModelSerializer):
    """serializer for trips"""
    class Meta:
        model = Message
        depth = 1
        fields = ('id', 'sender', 'receiver', 'content', 'created_on')
