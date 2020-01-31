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
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN
)
from .models import Profile
from .sereliazer import ProfileSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.permissions import IsAuthenticated
from PIL import Image
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_countries import countries


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")
    if password == confirm_password:
        if User.objects.filter(username=username).exists():
            return Response({'error': 'username already exist'}, status=HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            return Response({'error': 'email already exist'}, status=HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'you have successfully registered', 'user': serializer.data}, status=HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
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
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user = get_object_or_404(User, username=username)
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({'token': token, 'message': 'login success', 'user': user_serializer.data}, status=HTTP_200_OK)
    else:
        return Response({'error': 'Username not found'}, status=HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes((AllowAny, ))
def getAllUsers(request):
    users = User.objects.all()
    sereliazer = UserSerializer(users, many=True)
    return Response({'users': sereliazer.data}, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def getAllProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(
        profiles, many=True,  context={'request': request})
    return Response({'profiles': serializer.data}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def createProfile(request, *args, **kwargs):

    if Profile.objects.filter(user=request.user.id).exists():
        return Response({'error': 'You already created a profile'}, status=HTTP_400_BAD_REQUEST)

    user_serializer = UserSerializer(
        request.user, context={'request': request})
    serializer = ProfileSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'profile': serializer.data, 'user': user_serializer.data, 'message': 'profile succesfully created'}, status=HTTP_201_CREATED)
    else:
        return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def profileRUD(request, pk):

    try:
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=pk)
    except:
        return Response({'error': 'profile not found'}, status=HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(user)
    if request.method == 'GET':
        profile_serializer = ProfileSerializer(
            profile,  context={'request': request})
        return Response({'profile': profile_serializer.data, 'user': user_serializer.data}, status=HTTP_200_OK)

    elif request.method == 'PUT':
        if profile.user_id == request.user.id:
            serializer = ProfileSerializer(
                instance=profile, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'profile has been updated', 'profile': serializer.data, 'user': user_serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'error': 'you are not authorized to update this profile'}, status=HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if profile.user_id == request.user.id:
            serializer = ProfileSerializer(profile)
            profile.delete()
            return Response({'message': 'profile has been deleted', 'profiles': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'error': 'you are not authorized to delete this profile'}, status=HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getCountries(request):

    return Response({'countries': countries}, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def findLoggedUser(requset):
    serializer = UserSerializer(requset.user)
    return Response({'user': serializer.data}, status=HTTP_200_OK)
