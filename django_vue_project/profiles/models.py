from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField


def dateValidator(date) :
    if date > datetime.date.today():
        raise ValidationError("Birth Date cannot be in the future!")

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, validators=[
                                 MinLengthValidator(3)])
    lastname = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(default='default.jpg',
                              upload_to='profile_pic/', null=False, blank=False)
    GENDER_CHOICES = models.TextChoices('GENDER_CHOICES', 'male female other')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES.choices)
    date_of_birth = models.DateField(validators=[dateValidator])
    nationality = CountryField(blank=False, null=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     if self.date_of_birth > datetime.date.today():
    #         return ValidationError("Birth Date cannot be in the future!")
    #     super().save(*args, **kwargs)  
          

