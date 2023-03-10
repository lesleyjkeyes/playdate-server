from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Pet, Trait, PetTrait, User
from django.db.models import Count

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
        
        pet_id = self.request.query_params.get("pet_id", None)
        if pet_id is not None:
            pet_traits = pet_traits.filter(pet_id=pet_id)
            
        pets = self.request.query_params.get("pets", None)
        if pets is not None:
            pet_traits = pet_traits = PetTrait.objects.raw("select * from playdateapi_pettrait pt group by pt.pet_id")
            
        pet_trait_id = self.request.query_params.get("pet_trait_id", None)
        if pet_trait_id is not None:
            pet_traits = pet_traits.filter(pet_trait_id=pet_trait_id)
        
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


class UserSerializer(serializers.ModelSerializer):
    """serializer for trips"""
    class Meta:
        model = User
        depth = 1
        fields = ('uid', 'id', 'first_name', 'last_name', 'about', 'profile_image', 'email', 'city', 'state', 'country')
        
class PetSerializer(serializers.ModelSerializer):
    """serializer for pets"""
    owner = UserSerializer()
    class Meta:
        model = Pet
        depth = 1
        fields = ('id', 'name', 'about', 'profile_image', 'breed', 'owner')
class PetTraitSerializer(serializers.ModelSerializer):
    """serializer for Pet Traits"""
    pet = PetSerializer()
    class Meta:
        model = PetTrait
        depth = 2
        fields = ('id', 'pet', 'pet_trait')
