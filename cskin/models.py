from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)


class Session(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient')
    details = models.TextField()
    dateSubmission = models.DateTimeField(auto_now=True)
    dateTaken = models.DateTimeField(auto_now=True)


def image_directory_path(instance, filename):
	return 'patient_images/sessionid_{0}/{1}'.format(instance.session.id, filename)	


class Image(models.Model):
    session = models.ForeignKey(Session, related_name='session')
    image_file = models.ImageField(upload_to=image_directory_path)


# class AppNonce(models.Model):
# 	user = models.ForeignKey(User, related_name='user')
# 	create_time = models.DateTimeField(auto_now=True)
# 	nonce_value = last_name = models.CharField(max_length=64)
# 	class Meta:
# 		unique_together = (('user', 'create_time'),)