from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Interest

class InterestView(ViewSet):
    """Interest View"""
    def retrieve(self, request, pk):
        try:
            interest = Interest.objects.get(pk=pk)
            serializer = InterestSerializer(interest)
            return Response(serializer.data)
        except Interest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        interest = Interest.objects.create(
            title=request.data["title"]
          )
        serializer = InterestSerializer(interest)
        return Response(serializer.data)
    
    def update(self, request, pk):
        interest = Interest.objects.get(pk=pk)
        interest.title = request.data["title"]
        interest.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Handle DELETE requests for a single interest"""
        interest = Interest.objects.get(pk=pk)
        interest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class InterestSerializer(serializers.ModelSerializer):
    """serializer for Interests"""
    class Meta:
        model = Interest
        depth = 1
        fields = ('id', 'title')
