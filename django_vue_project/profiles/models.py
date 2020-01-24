from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
# use pillow to resize image
from PIL import Image


# Create your models here.
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, blank=True)
    lastname = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_pic', null=True)
    GENDER_CHOICES = models.TextChoices('GENDER_CHOICES', 'male female other')
    gender = models.CharField(max_length=6 ,choices=GENDER_CHOICES.choices, blank=True)
    date_of_birth = models.DateField(blank=True)
    nationality = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=13, unique=True)


    def __str__ (self): 
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs) :
        if self.date_of_birth > datetime.date.today():
            return ValidationError("Birth Date cannot be in the future!")
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300 :
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)