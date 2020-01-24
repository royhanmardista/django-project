from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .models import Profile
from .sereliazer import profileSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .validators import validateEmail
from datetime import datetime
from django.utils.dateparse import parse_date

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    if not username or not password or not email:
        return Response({'error': 'You need to provide username, email, password'}, status=HTTP_400_BAD_REQUEST)
    if not validateEmail(email) :
        return Response({'error': 'invalid email password'}, status=HTTP_400_BAD_REQUEST)
    if password == confirm_password:
        if User.objects.filter(username=username).exists():
            return Response({'error': 'username already exist'}, status=HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            return Response({'error': 'email already exist'}, status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({'message': 'Register success'}, status=HTTP_200_OK)
    else:
        return Response({'error': 'password not matched'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({'error': 'You need to provide both password and username'}, status=HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Wrong password'}, status=HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'login success'}, status=HTTP_200_OK)
    else:
        return Response({'error': 'Username not found'}, status=HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllProfiles(request):
    profiles = Profile.objects.all()
    serializer = profileSerializer(profiles, many=True)
    return Response({'profiles': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def createProfile(request, *args, **kwargs):
    user = request.user
    firstname = request.data.get("firstname")
    lastname = request.data.get("lastname")
    gender = request.data.get("gender")
    date_of_birth = parse_date(request.data.get("date_of_birth"))
    nationality = request.data.get("nationality")
    phone = request.data.get("phone")
    photo = request.data.get("photo")
    profile = Profile(user=user, firstname=firstname, lastname=lastname, gender=gender, date_of_birth=date_of_birth, nationality=nationality, phone=phone, photo=photo)
    profile.save()
    serializer = profileSerializer(profile)
    return Response(serializer.data)
