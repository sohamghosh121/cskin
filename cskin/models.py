from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)


class Session(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient')
    details = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Image(models.Model):
    session = models.ForeignKey(Session, related_name='session')
    image_file = models.ImageField(upload_to='patient_images/')
