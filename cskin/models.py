from django.db import models


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
