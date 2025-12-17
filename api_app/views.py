from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from api_app.models import *
from api_app.serializers import UserregisterSerializer,Productserializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
class UserregisterView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):

        user_serializer = UserregisterSerializer(data=request.data)

        if user_serializer.is_valid():

            user = user_serializer.save()

            return Response(user_serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Loginview(APIView):

    authentication_classes = [BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self,request):

        user = request.user

        refresh = RefreshToken.for_user(user)

        # token,created = Token.objects.get_or_create(user=user)
        
        return Response({"message":"login success",
                         "access":str(refresh.access_token),
                         "refresh":str(refresh)
                        },                         
                        status=status.HTTP_200_OK
                        )

                        #  "token":token.key},

        # print(user.username)
        
        # print(request.user)

class Productaddlistview(APIView):

    authentication_classes =[JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self,request):

        serializer = Productserializer(data = request.data)

        if serializer.is_valid():

            serializer.save(user = request.user)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#Basic authentication
#list all the product

    def get(self,request):

        data = Productmodel.objects.filter(user = request.user)

        serializer = Productserializer(data,many = True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductRetrieveUpdateDelete(APIView):

    authentication_classes =[TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self,request,**kwargs):

        id = kwargs.get('pk')

        product = get_object_or_404(Productmodel,id =id,user = request.user)

        serializer = Productserializer(product,many = False)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,**kwargs):

        id = kwargs.get('pk')

        product = get_object_or_404(Productmodel,id =id,user = request.user)

        serializer = Productserializer(product,data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,**kwargs):

        id = kwargs.get('pk')

        product =  get_object_or_404(Productmodel,id=id)

        product.delete()

        return Response({"message :Product Deleted Successfully"},status=status.HTTP_200_OK)

class Productfilterbycolorview(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self,request):

        color = request.query_params.get('color')

        products = Productmodel.objects.filter(user = request.user)

        data = products.filter(product_color__icontains =color)

        serializer = Productserializer(data,many = True)

        return Response(serializer.data,status=status.HTTP_200_OK)



