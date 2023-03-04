from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Conversation
from playdateapi.models import User

class ConversationView(ViewSet):
    """Conversation View"""
    def retrieve(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist as ex:
            return Response({'conversation': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        conversations = Conversation.objects.all()
        user_id = self.request.query_params.get("user_id", None)

        if user_id is not None:
            conversations = Conversation.objects.raw(
                "select * from playdateapi_conversation where user_one_id = %s or user_two_id = %s", 
                [user_id, user_id]
                )

        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_one = User.objects.get(id=request.data["id"])
        user_two = User.objects.get(id=request.data["id"])
        conversation = Conversation.objects.create(
            user_one=user_one,
            user_two=user_two
          )
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

class ConversationSerializer(serializers.ModelSerializer):
    """serializer for conversations"""
    class Meta:
        model = Conversation
        depth = 1
        fields = ('id', 'user_one', 'user_two')
