from django.db import models

from django.contrib.auth.models import User

import uuid

class BaseClass(models.Model):


    uuid = models.UUIDField(default=uuid.uuid4,unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class Category(BaseClass):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name

    class Meta:

        verbose_name_plural = "Categories"        


class Doctor(BaseClass):

    profile = models.OneToOneField( 'accounts.Profile',on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='doctor_photos/')

    contact_number = models.CharField(max_length=13)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    experience = models.IntegerField()

    def __str__(self):

        return f'{self.name}-{self.category.name}' 
    
    class Meta:

        verbose_name_plural = "Doctors"


class Availability(BaseClass):

    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    def __str__(self):

        return f'{self.doctor.name}-{self.date}'  

    class Meta:

        verbose_name_plural = "Availabilities"      

