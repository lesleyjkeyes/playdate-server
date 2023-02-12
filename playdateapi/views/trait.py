from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Trait

class TraitView(ViewSet):
    """Trait View"""
    def retrieve(self, request, pk):
        try:
            trait = Trait.objects.get(pk=pk)
            serializer = TraitSerializer(trait)
            return Response(serializer.data)
        except Trait.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        traits = Trait.objects.all()
        serializer = TraitSerializer(traits, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        trait = Trait.objects.create(
            title=request.data["title"]
          )
        serializer = TraitSerializer(trait)
        return Response(serializer.data)
    
    def update(self, request, pk):
        trait = Trait.objects.get(pk=pk)
        trait.title = request.data["title"]
        trait.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Handle DELETE requests for a single trait"""
        trait = Trait.objects.get(pk=pk)
        trait.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TraitSerializer(serializers.ModelSerializer):
    """serializer for traits"""
    class Meta:
        model = Trait
        depth = 1
        fields = ('id', 'title')
