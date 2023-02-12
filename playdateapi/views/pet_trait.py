from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Pet, Trait, PetTrait

class PetTraitView(ViewSet):
    """Pet Trait View"""
    def retrieve(self, request, pk):
        try:
            pet_trait = PetTrait.objects.get(pk=pk)
            serializer = PetTraitSerializer(pet_trait)
            return Response(serializer.data)
        except PetTrait.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        pet_traits = PetTrait.objects.all()
        serializer = PetTraitSerializer(pet_traits, many=True)
        return Response(serializer.data)

    def create(self, request):
        pet_trait = PetTrait.objects.create(
            pet = Pet.objects.get(id=request.data["pet_id"]),
            pet_trait = Trait.objects.get(id=request.data["pet_trait_id"])
          )
        serializer = PetTraitSerializer(pet_trait)
        return Response(serializer.data)

    def delete(self, request, pk):
        """Handle DELETE requests for a single pet trait"""
        pet_trait = PetTrait.objects.get(pk=pk)
        pet_trait.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PetTraitSerializer(serializers.ModelSerializer):
    """serializer for Pet Traits"""
    class Meta:
        model = PetTrait
        depth = 1
        fields = ('id', 'pet', 'pet_trait')
