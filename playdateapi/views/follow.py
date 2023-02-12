from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Follow, User

class FollowView(ViewSet):
    """Follow View"""
    def retrieve(self, request, pk):
        try:
            follow = Follow.objects.get(pk=pk)
            serializer = FollowSerializer(follow)
            return Response(serializer.data)
        except Follow.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        follows = Follow.objects.all()
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

    def create(self, request):
        follower = User.objects.get(id=request.data["follower_id"])
        followed = User.objects.get(id=request.data["followed_id"])
        follow = Follow.objects.create(
            follower = follower,
            followed = followed
          )
        serializer = FollowSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, pk):
        """Handle DELETE requests for a single follow"""
        follow = Follow.objects.get(pk=pk)
        follow.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class FollowSerializer(serializers.ModelSerializer):
    """serializer for follows"""
    class Meta:
        model = Follow
        depth = 1
        fields = ('id', 'follower', 'followed')
