from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from playdateapi.models import Pet
from playdateapi.models import User

class PetView(ViewSet):
    """Pet View"""
    def retrieve(self, request, pk):
        try:
            pet = Pet.objects.get(pk=pk)
            serializer = PetSerializer(pet)
            return Response(serializer.data)
        except Pet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        owners = User.objects.all()
        pets = Pet.objects.all()
        # city = self.request.query_params.get("city", None)
        # print(city)
        # owners = owners.filter(city=city)
        # print(owners[id])
        # if city is not None:
        #     owners = owners.filter(city=city)
        #     pets = pets.filter(owner in owners)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        owner = User.objects.get(id=request.data["id"])
        pet = Pet.objects.create(
            owner=owner,
            name=request.data["name"],
            about=request.data["about"],
            profile_image=request.data["profile_image"],
            breed=request.data["breed"]
          )
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    
    def update(self, request, pk):
        pet = Pet.objects.get(pk=pk)
        pet.name = request.data["name"]
        pet.about = request.data["about"]
        pet.profile_image = request.data["profile_image"]
        pet.breed = request.data["breed"]
        pet.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Handle DELETE requests for a single post"""
        pet = Pet.objects.get(pk=pk)
        pet.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PetSerializer(serializers.ModelSerializer):
    """serializer for trips"""
    class Meta:
        model = Pet
        depth = 1
        fields = ('id', 'name', 'about', 'profile_image', 'breed', 'owner')
