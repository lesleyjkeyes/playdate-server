from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import User

class UserView(ViewSet):
    """User View"""
    def retrieve(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            profile_image=request.data["profile_image"],
            about=request.data["about"],
            email=request.data["email"],
            city=request.data["city"],
            state=request.data["state"],
            country=request.data["country"]
          )
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.profile_image = request.data["profile_image"]
        user.about = request.data["about"]
        user.email = request.data["email"]
        user.city = request.data["city"]
        user.state = request.data["state"]
        user.country = request.data["country"]
        user.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Handle DELETE requests for a single post"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """serializer for trips"""
    class Meta:
        model = User
        depth = 1
        fields = ('id', 'first_name', 'last_name', 'about', 'profile_image', 'email', 'city', 'state', 'country')
