from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Pet, Interest, PetInterest, User

class PetInterestView(ViewSet):
    """Pet Interest View"""
    def retrieve(self, request, pk):
        try:
            pet_interest = PetInterest.objects.get(pk=pk)
            serializer = PetInterestSerializer(pet_interest)
            return Response(serializer.data)
        except PetInterest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        pet_interests = PetInterest.objects.all()
        
        pet_id = self.request.query_params.get("pet_id", None)
        if pet_id is not None:
            pet_interests = pet_interests.filter(pet_id=pet_id)
        
        pets = self.request.query_params.get("pets", None) 
        if pets is not None:
            pet_interests = pet_interests = PetInterest.objects.raw("select * from playdateapi_petinterest pi group by pt.pet_id")
            
        pet_interest_id = self.request.query_params.get("pet_interest_id", None)
        if pet_interest_id is not None:
            pet_interests = pet_interests.filter(pet_interest_id=pet_interest_id)
        
        serializer = PetInterestSerializer(pet_interests, many=True)
        return Response(serializer.data)

    def create(self, request):
        pet_interest = PetInterest.objects.create(
            pet = Pet.objects.get(id=request.data["pet_id"]),
            pet_interest = Interest.objects.get(id=request.data["pet_interest_id"])
          )
        serializer = PetInterestSerializer(pet_interest)
        return Response(serializer.data)

    def delete(self, request, pk):
        """Handle DELETE requests for a single pet interest"""
        pet_interest = PetInterest.objects.get(pk=pk)
        pet_interest.delete()
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
class PetInterestSerializer(serializers.ModelSerializer):
    """serializer for Pet Interests"""
    pet = PetSerializer
    class Meta:
        model = PetInterest
        depth = 2
        fields = ('id', 'pet', 'pet_interest')
        
        
