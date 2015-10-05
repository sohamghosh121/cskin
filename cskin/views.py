from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cskin.models import Patient, Image, Session
from django.template.defaulttags import register
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from django.views.decorators.csrf import csrf_exempt

import os
import datetime
import prod_settings as settings
import logging



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def healthCheck(request):
	return HttpResponse('It\'s all good!')


def loginView(request):
	return render(request, 'templates/login.html')


def processLogin(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(to='/seeImages')
            # Redirect to a success page.
        else:
        	return HttpResponse('disabled account')
            # Return a 'disabled account' error message
    else:
    	return HttpResponse('invalid')
        # Return an 'invalid login' error message.


def processLogout(request):
    logout(request)


@csrf_exempt
def processImageUpload(request):
	print '---------- here'
	patientEmail = request.POST.get('patientEmail')
	print request.POST.items()
	print settings.DATE_FORMAT
	date_taken = request.POST.get('dateTaken')
	date_taken = datetime.strptime(date_taken, settings.DATE_FORMAT) if date_taken else datetime.datetime.now()
	print 'date taken was ok'
	date_submission = request.POST.get('dateSubmission')
	date_submission = datetime.strptime(date_submission, settings.DATE_FORMAT) if date_submission else datetime.datetime.now()
	print 'date submission was ok'
	details = request.POST.get('details')
	numberOfImages = int(request.POST.get('nImages'))
	patient = Patient.objects.get(email=patientEmail)
	session = Session.objects.create(patient=patient, dateTaken=date_taken, dateSubmission=date_submission, details=details)
	for i in range(numberOfImages):
		imagekey = 'image_%d' % i
		image = request.FILES.get(imagekey)
		if image:
			new_image = Image.objects.create(session=session, image_file=image)
		else:
			# TODO: put code here to process image
			print 'exception'
			raise Exception('No image provided')
	return HttpResponse('saved')


def testUploadImage(request):
	return render(request, 'templates/testUploadImage.html')


@login_required
def seeImages(request):
	"""
		Tool for admin to see images for user, chronologically ordered
	"""
	patients = Patient.objects.all();
	sessions = {p.email: Session.objects.filter(patient=p) for p in patients}
	allSessions = Session.objects.all()
	images = {s.id: Image.objects.filter(session=s) for s in allSessions}
	context = {}
	context['patients'] = patients
	context['sessions'] = sessions
	context['images'] = images;
	# import pdb
	# pdb.set_trace()
	return render(request, 'templates/seeImages.html', context)
