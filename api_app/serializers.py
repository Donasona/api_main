from rest_framework import serializers
from api_app.models import *

class UserregisterSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["username","password","email"]

    def create(self,validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )    

        return user
    
class Productserializer(serializers.ModelSerializer):

    class Meta:

        model =Productmodel

        exclude = ('user',)  #name,price,color user >> authentication  

