from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cskin.models import Patient, Image
from django.template.defaulttags import register

import datetime


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



def processImageUpload(request):
	patientEmail = request.POST.get('patientEmail')
	# date_taken = request.POST.get('dateTaken')
	image = request.FILES.get('image')
	patient = Patient.objects.get(email=patientEmail)
	new_image = Image.objects.create(date_taken=datetime.datetime.today(), patient=patient, image_file=image)
	return HttpResponse('saved')


def testUploadImage(request):
	return render(request, 'templates/testUploadImage.html')


@login_required
def seeImages(request):
	"""
		Tool for admin to see images for user, chronologically ordered
	"""
	patients = Patient.objects.all();
	images = {p.email: Image.objects.filter(patient=p) for p in patients}
	context = {}
	context['patients'] = patients
	context['images'] = images;
	# import pdb
	# pdb.set_trace()
	return render(request, 'templates/seeImages.html', context)
