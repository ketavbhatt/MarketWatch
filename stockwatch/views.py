# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render,redirect
from django.http import HttpResponse

#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.globalstockquotes import GlobalStockQuotes
import json
#from pprint import pprint

#from nsetools import Nse
from nasdaq_stock_quote import Share

from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from email.MIMEMultipart import MIMEMultipart
from .safe import usermail,upassword
from email.MIMEText import MIMEText
import smtplib
import hashlib
import ast
import datetime
from django.http import JsonResponse



# Create your views here.


def home(request):
	#gsq = TimeSeries(key='EODCNM4ZVVCTQPY0')
	# data, meta_data = gsq.get_intraday(symbol='NSE:INFY')
	# pprint(data)
    if request.user.is_authenticated():





		a =[
			# "DDD",
			# "MMM",
			# "WBAI",
			# "WUBA",
			# "AHC",
			# "ATEN",
			# "AAC",
			# "AIR",
			# "AAN",
			# "ABB",
			# "ABT",
			# "ABBV",
			# "ANF",
			# "GCH",
			# "JEQ",
			# "SGF",
			# "ABM",
			# "AKR",
			# "ACN",
			# "ACCO",
			# "ATV",
			# "ATU",
			# "AYI",
			# "GOLF",
			# "ADX",
			# "PEO",
			# "AGRO",
			# "ADNT",
			# "ATGE",
			# "AAP",
			# "ADSW",
			# "WMS",
			# "ASX",
			# "ASIX",
			# "AAV",
			# "AVK",
			# "AGC",
			# "LCM",
			# "ACM",
			# "ANW",
			# "AEB",
			# "AED",
			# "AEG",
			# "AEH",
			# "AEK",
			# "AER",
			# "HIVE",
			# "AJRD",
			# "AET",
			# "AMG",

		] 
		for i in a:
			share = Share(i)
			price = share.get_price()
			name = share.get_name()
			volume = share.get_volume()
			perct = share.get_percent_change()
			high = share.get_day_high()
			low = share.get_day_low()

			if Stock.objects.filter(name=i).exists():
				stock = Stock.objects.filter(name=i).update(name=name,price=price,volume=volume,perct=perct,high=high,low=low)
			else:

				stock = Stock.objects.create(name=name,price=price,volume=volume,perct=perct,high=high,low=low)
				stock.save()


		stock = Stock.objects.all()
		
			


			

		# nse = Nse()

		# all_stock_codes = nse.get_stock_codes()
		# top_gainers = nse.get_top_gainers()
		# top_gainers = json.dumps(top_gainers)
		# print top_gainers
		return render(request,"home.html",{'stock':stock})


def register(request):
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		password = request.POST['password']
		
		hash=hashlib.sha1()
                now=datetime.datetime.now()
                hash.update(str(now)+email+'asdasdas')
                tp=hash.hexdigest()
                print tp
		
		user = tempUser.objects.create(fname=fname,lname=lname,email=email,password=password,tp=tp)
		
		user.save()
		print user

		fromaddr=usermail
                toaddr=email
                print fromaddr
                print toaddr
                msg=MIMEMultipart()
                msg['From']=fromaddr
                msg['To']=toaddr
                msg['Subject']='Confirmational Email'
                domain = request.get_host()
                scheme = request.is_secure() and "https" or "http"
                body = "Please Click On The Link To complete registration: {0}://{1}/{2}/registeration_comp".format(scheme,domain,tp) 
                part1 = MIMEText(body, 'plain')
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, upassword)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                return HttpResponse('Verification Link has been sent')
	else:

		return render(request,"login.html")

def login_site(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username = email, password = password)
		if user:
			login(request, user)
			return redirect('/home/')
		else:
			return HttpResponse('invalid')

	else:	
		return render(request, 'login.html')
	
def registeration_comp(request,p):
	tp=p
	u = tempUser.objects.get(tp=tp)
	user = User.objects.create(username=u.email,first_name=u.fname,last_name=u.lname,email=u.email)
	user.set_password(u.password)
	user.save()
	tempUser.objects.filter(tp=tp).delete()

	return redirect('/home/')


def wishlisttable(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			s = json.loads(request.body.decode('utf-8'))
			name = s['name']
			stock = Stock.objects.get(name=name)
			print stock
			print request.user
			if wishlist.objects.filter(stock=stock,user=request.user).exists():
				pass
			else:
				Wishlist = wishlist.objects.create(user=request.user,stock=stock)
				Wishlist.save()
			return JsonResponse({'success' : 'true'})
		else:
			return HttpResponse("dfgdghdh")
	else:
		return redirect('/login_site/')

def watchlist(request):
	if request.user.is_authenticated():
		print request.user
		Wishlist = wishlist.objects.filter(user=request.user)
		
		return render(request,"watchlist.html",{'wishlist' : Wishlist})

	else:
		return redirect('/login_site/')





