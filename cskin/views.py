from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from cskin.models import Patient, Image, Session
from django.template.defaulttags import register
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from django.views.decorators.csrf import csrf_exempt

import random

import os
import datetime
import settings as settings
import logging


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def healthCheck(request):
    return HttpResponse('It\'s all good!')


def loginView(request):
    return render(request, 'templates/login.html')


# def getAppNonce(request):
# 	try:
# 		return AppNonce.objects.get(user=request.user)
# 	except AppNonce.DoesNotExist:
# 		return AppNonce.objects.create(user=request.user, nonce_value=generate_nonce())

# def generate_nonce():
# 	""" Generates a random string of bytes, base64 encoded """
# 	length = 32
# 	return ''.join([str(random.randint(0, 9)) for i in range(length)])


def createUser(request):
	name = request.POST.get('name')
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	isPatient = request.POST.get('isPatient')
	if fname and lname and username and email and password:
		# first save as a user (for authentication)
		user.objects.create_user(username, email, password)
		user.name = name
		user.save()
		# then save as a patient (for dbm)
		if isPatient:
			name = fname + ' ' + lname
			Patient.objects.create(email=email, name=name)
		return JsonResponse({'success': True})
	else:
		return JsonResponse({'success': False, 'error': 'A required field was not provided'})


def getUser(request):
	import pdb
	pdb.set_trace()
	return HttpResponse('lala')


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
    patientEmail = request.POST.get('patientEmail')
    print patientEmail
    date_taken = request.POST.get('dateTaken')
    print date_taken
    date_taken = datetime.datetime.strptime(
        date_taken, settings.DATE_FORMAT) if date_taken else datetime.datetime.now()
    date_submission = request.POST.get('dateSubmission')
    date_submission = datetime.datetime.strptime(
        date_submission, settings.DATE_FORMAT) if date_submission else datetime.datetime.now()
    print date_submission
    details = request.POST.get('details')
    print details
    numberOfImages = int(request.POST.get('nImages'))
    print numberOfImages
    patient = Patient.objects.get(email=patientEmail)
    session = Session.objects.create(
        patient=patient, dateTaken=date_taken, dateSubmission=date_submission, details=details)
    for i in range(numberOfImages):
        print i
        imagekey = 'image_%d' % i
        image = request.FILES.get(imagekey)
        print request.FILES
        print image
        if image:
            new_image = Image.objects.create(session=session, image_file=image)
        else:
            # TODO: put code here to process image

            print('no image')
            raise Exception('No image provided')
    return HttpResponse('saved')


@csrf_exempt
def getPatientImages(request):
    patientEmail = request.POST.get('patientEmail')
    response = []
    patient = Patient.objects.get(email=patientEmail)
    sessions = Session.objects.filter(patient=patient)
    for i in range(len(sessions)):
        s = sessions[i]
        images = Image.objects.filter(session=s)
        response.append({'dateTaken': datetime.datetime.strftime(s.dateTaken, settings.DATE_FORMAT), 'dateSubmission': datetime.datetime.strftime(
            s.dateSubmission, settings.DATE_FORMAT), 'details': s.details, 'images': [img.image_file.url for img in images]})
    return JsonResponse(response, safe=False)


def testUploadImage(request):
    return render(request, 'templates/testUploadImage.html')


@login_required
def seeImages(request):
    """
            Tool for admin to see images for user, chronologically ordered
    """
    patients = Patient.objects.all()
    sessions = {p.email: Session.objects.filter(patient=p) for p in patients}
    allSessions = Session.objects.all()
    images = {s.id: Image.objects.filter(session=s) for s in allSessions}
    context = {}
    context['patients'] = patients
    context['sessions'] = sessions
    context['images'] = images
    # import pdb
    # pdb.set_trace()
    return render(request, 'templates/seeImages.html', context)
