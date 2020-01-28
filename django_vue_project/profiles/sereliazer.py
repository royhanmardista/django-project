from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator
from dateutil.relativedelta import *
import re
from phonenumber_field.modelfields import PhoneNumberField
import PIL

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, min_length=3)
    password = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")        
        extra_kwargs = {'password': {'write_only': True}}              

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer) :
    user = serializers.ReadOnlyField(source='user.id')
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=False)
    GENDER_CHOICES = [('female', 'female'), ('male', 'male'), ('other', 'other')]
    gender = serializers.ChoiceField(GENDER_CHOICES, required=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    photo = serializers.ImageField(required=True, allow_empty_file=False)
    date_of_birth = serializers.DateField(required=True)
    nationality = CountryField(blank=False, null=False)

    def validate_date_of_birth(self, value):        
        now = datetime.datetime.utcnow()
        now = now.date()
        age = relativedelta(now, value)
        age = age.years

        if value > datetime.date.today():
            raise serializers.ValidationError("Birth Date cannot be in the future!")
        elif age > 100 :
            raise serializers.ValidationError("Age cannot be older then 100 years")
        return value   

    def validate_firstname(self, value) :
        if len(value) < 3 :
            raise serializers.ValidationError('Min Length is 3 Characters')
        if not re.match('^[a-zA-Z]+$', value):
            raise serializers.ValidationError('Can Only enter alphabet')
        return value

    class Meta:
        model = Profile    
        fields = '__all__'        

    def create(self, validated_data):        
        print('asssssssssssssssssssssssssssssssssssssssssss===============================================')        
        validated_data['user'] = self.context['request'].user    
        obj = Profile.objects.create(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.nationality = validated_data.get('nationality', instance.nationality)

        instance.save()
        return instance

    