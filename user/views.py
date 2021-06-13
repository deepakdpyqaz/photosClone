from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

@api_view(['GET','POST'])
def login(request):
    username = request.data['email']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        response = user_serializer.data
        response['token']=token.key
        return Response(response,status=200)
    else:
        return Response({"status":"fail","message":"Either username or password is incorrect"},status=400)

@api_view(['GET','POST'])
def signup(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']
    try:
        user = User.objects.create_user(email,email,password)
        user.first_name = name
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        response = user_serializer.data
        response['token']=token.key
        return Response(response,status=200)
        return Response({"status":"success"},status=201)
    except IntegrityError as e:
        return Response({"status":"fail","message":"Username is not available"},status=400)
    except Exception as e:
        return Response({"status":"fail","message":str(e)},status=500)

@api_view(["GET"])
def logout(request):
    if request.user:
        try:
            token = Token.objects.filter(user=request.user.id).first()
            if token:
                token.delete()
        except Exception as e:
            return Response({"status":"fail","message":str(e)},status=500)
    return Response({"status":"success"},status=200)