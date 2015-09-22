from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)


class Image(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient')
    date_taken = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(upload_to='patient_images/')
