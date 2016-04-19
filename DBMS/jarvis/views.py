from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from django.http import *
import cx_Oracle
import math

# Create your views here.
#def search_form(request):
#   return render(request, 'search_form.html')


def home(request):
	return render(request, 'home.html',{})

def signup_confirm(request):
	return render(request, 'signup_confirm.html',{})	

def login(request):
	request.session.flush()
	context = {}
	if(request.method == 'GET'):
		return render(request, "login.html" ,context)
	context = {"checked" : 0}

	if(request.method == 'POST'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		user = request.POST.get("un")
		password = request.POST.get("pass")

		passwordFetchCursor = connection.cursor()
		passwordFetchCursor.execute('Select password from Person where username = \'' + user + '\'')
		returnedPass = None
		try:
			returnedPass = passwordFetchCursor.fetchone()[0]
		except:
			context = {"checked" : 1}	
		print returnedPass	
		passwordFetchCursor.close()
		connection.close()
		if(not returnedPass == None) and (password == returnedPass):
			print "hasta la vista baby"
			request.session['uid'] = user
			request.session['pass'] = password
			context = {"name" :user}
			#return redirect ('dashboard')
			return HttpResponseRedirect('../dashboard')
		else:
			context = {
				"template_title" : "Wrong Username/password"
			}
			return render(request, "login.html", context)	
			#return render(request, "Dashboard.html", context )
			



def signup(request):

	#request is whenever you're changing contexts.
	#It contains information about get and post.

	#if(request.method == "POST"):
		#print request.POST

	#form = PersonForm(request.POST or None) #In case there's no information in the post data, don't send through the validator

	context={}

	if(request.method == 'GET'):
		return render(request,"signup.html",context)
	if(request.method == 'POST'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		preloadUsersCursor = connection.cursor()
		preloadUsersCursor.execute('Select * from Person order by p_id desc')
		top = preloadUsersCursor.fetchone()[0]
		person_id = top+1
		print person_id
		user = request.POST.get("un")
		name = request.POST.get("name")
		mob_no = request.POST.get("phone")
		email = request.POST.get("email")
		gender = request.POST.get("gender")
		password = request.POST.get("password")
		print person_id
		newUser = [person_id, user, name, mob_no, email, gender, password]
		preloadUsersCursor.close()

		insertCursor = connection.cursor()
		flag =0
		insertCursor.execute('SELECT * from Person where username = \''+str(user)+'\'')
		allUsernames = insertCursor.fetchall()
		l = len(allUsernames)
		if (l>0):
			context = {
			"template_title" : "Username already Exists !"
			}
			flag = 1
			return render (request, "signup.html",context)

		if flag==0:
			insertCursor.execute('INSERT into person (p_id,username,name,mob_no, email, gender, password) values (:1, :2, :3, :4, :5, :6, :7)',newUser)
			connection.commit()
			insertCursor.close()

			context = {
				"template_title" : "Thanks for Signing Up !"
			}

			return render (request, "signup.html",context)	

#def dashboard(request):


def dashboard(request):
	sessionCheck = request.session.get('uid', None)
	
	if sessionCheck:
		return render(request, "dashboard.html", {"name" : sessionCheck})
	else:
		return HttpResponseRedirect('../login')		
	if(request.method == 'GET'):
		return render(request, "dashboard.html", {"name" : username})



def enqj(request):
	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')
	
	if(request.method == 'GET'):
 		return render(request,"enqj.html",{})
 	if(request.method == 'POST'):

 		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
 		cursor = connection.cursor()
 		start = request.POST.get("inputStart")
 		end = request.POST.get("inputEnd")
 		cursor.execute('SELECT Train.Train_id, Train.name from TRAIN, Station, Train_route where Station.s_name =\''+start+'\' and Train_route.Train_id = TRAIN.Train_id and Train_route.s_id = Station.s_id order by Train.Train_id')
 		# , Train_route.exp_arrival, Train_route.exp_depature
 		starts = cursor.fetchall()
 		cursor.execute('SELECT TRAIN.Train_id, Train.name from TRAIN, Station, Train_route where Station.s_name =\''+end+'\' and Train_route.Train_id = TRAIN.Train_id and Train_route.s_id = Station.s_id order by Train.Train_id')
 		ends = cursor.fetchall()
 		reqd = list(set(ends).intersection(starts))
 		l = len(reqd)
 		arrivals=[]
 		deps =[]
 		for i in range(0,l):
			 # SELECT Train_route.exp_arrival from  Station, Train_route where Station.s_name LIKE 'New Orleans' and Train_route.Train_id =10022 and Train_route.s_id = Station.s_id;
			cursor.execute('SELECT Train_route.exp_arrival from  Station, Train_route where Station.s_name =\''+start+'\' and Train_route.Train_id = \''+str(reqd[i][0])+'\' and Train_route.s_id = Station.s_id' )
 			arrivals.append(cursor.fetchone()[0])
 			cursor.execute('SELECT Train_route.exp_arrival from  Station, Train_route where Station.s_name =\''+end+'\' and Train_route.Train_id = \''+str(reqd[i][0])+'\' and Train_route.s_id = Station.s_id' )
 			deps.append(cursor.fetchone()[0])
 			
 		connection.commit()
 		cursor.close()
 		connection.close()
 		finarray = zip(reqd,arrivals,deps)
 		print finarray
 		#uid = request.session.GET('uid',None)
 		#pwd = request.session.GET('pass',None)
 		context = {
			"trains" : reqd,
			"start"	: start,
			"end" : end,
			"finarray" : finarray
		}
 		return render (request, "enqj.html",context)

# def enqj(request):

# 	if(request.method == 'GET'):
# 		return render(request,"enqj.html",{})
# 	if(request.method == 'POST'):
		
# 		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
# 		sourceStation = request.POST.get("source")
# 		destStation = request.POST.get("dest")		
# 		numberOfSeats = request.POST.get("seats")	
# 		journeyDate = request.POST.get("doj")	
# 		enquiryCursor = connection.cursor()
# 		enquiryQuery = 'SELECT '


# 	return render(request, "enquiry.html", {})
def enqt(request):

	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')

	if(request.method == 'GET'):
 		return render(request,"enqt.html",{})

 	if(request.method == 'POST'):

 		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
 		cursor = connection.cursor()
 		tname = request.POST.get("inputTname")
 		cursor.execute('SELECT Train.Name, Station.s_name, Train_route.exp_arrival, Train_route.exp_depature from Train_route, Train, Station WHERE Train.Name=\'' +tname+ '\' and Train.Train_id=Train_route.Train_id and Train_route.s_id=Station.s_id ORDER BY Train_route.order_no')
 		route = cursor.fetchall()
 		connection.commit()
 		cursor.close()
 		connection.close()
 		

 		context = {
 			"routes" : route
 		}
 		return render(request, "enqt.html",context)


def booking(request):
	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')

	if(request.method == 'GET'):
 		return render(request,"booking.html",{})

 	if(request.method == 'POST'):

 		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
 		cursor = connection.cursor()
 		start = str(request.POST.get("inputStart"))
 		end = str(request.POST.get("inputEnd"))
 		seats = int(request.POST.get("inputSeats"))
 		doj =  str(request.POST.get("inputDate"))
 		cursor.execute('SELECT s_id from station where s_name = \'' +(start)+ '\'')
 		x = cursor.fetchone()
 		request.session['start_pt'] = x[0]
 		cursor.execute('SELECT s_id from station where s_name = \'' +(end)+ '\'')
 		y = cursor.fetchone()
 		request.session['end_pt'] = y[0]
 		request.session['seats'] = seats
		request.session['date'] = doj
		cursor.execute('SELECT Train.Train_id, Name from Train, station, Train_route where station.s_name=\'' +start+ '\' and Train_route.Train_id=Train.Train_id and Train_route.s_id=station.s_id')
		a=cursor.fetchall()
		cursor.execute('SELECT Train.Train_id, Name from Train, station, Train_route where station.s_name=\'' +end+ '\' and Train_route.Train_id=Train.Train_id and Train_route.s_id=station.s_id')
		b=cursor.fetchall()
		reqd = list(set(a).intersection(b))
		print reqd
		final = []
		for train in reqd:
			cursor.execute('SELECT count(*) from Availability where Train_id=' +str(train[0])+ ' and DOJ= \''+str(doj)+'\'')
			counter = cursor.fetchone()[0]
			if int(counter) > 0:
				cursor.execute('SELECT order_no from Train_route,Station WHERE Train_route.Train_id=\'' +str(train[0])+ '\' and Station.s_name=\'' +start+ '\' and Train_route.s_id=station.s_id')
				ostart=cursor.fetchone()[0]
				cursor.execute('SELECT order_no from Train_route,Station WHERE Train_route.Train_id=\'' +str(train[0])+ '\' and Station.s_name=\'' +end+ '\' and Train_route.s_id=station.s_id')
				oend = cursor.fetchone()[0]
				if oend<ostart:
					oend, ostart = ostart, oend
				cursor.execute('SELECT distinct s_id, Seats_Available from Availability where train_id =\'' +str(train[0])+ '\' and s_id in(SELECT s_id from Train_route WHERE Train_id=\'' +str(train[0])+ '\'and order_no BETWEEN \'' +str(ostart)+ '\' and \'' +str(oend)+ '\')') 
				path = cursor.fetchall()
				print path
				possible = True
				for pform in path:
					if (pform[1]<int(seats)):
						possible = False
						break
				if possible == True:	
					final.append(train)	
			else:	
				cursor.execute('SELECT s_id from Train_route where train_id =\'' +str(train[0])+ '\'')		
				ids = cursor.fetchall()
				for pid in ids:
					newArray = [train[0],pid[0],doj,750]
					cursor.execute('INSERT into Availability(Train_id,s_id,doj,Seats_Available) VALUES (:1, :2, :3, :4)',newArray)
				final.append(train)
		connection.commit()
		cursor.close()
		connection.close()
		request.session['final'] = final
		l=len(final)
		list2 = []
		for i in range(0,l):
			list2.append(i)
		context ={
			"finals":final,
			"length":list2
		}
		print list2
   		return render (request, "booktrain.html",context)

def booktrain(request):

	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')

	if(request.method == 'GET'):
 		return render(request,"booktrain.html",{})

 	if(request.method == 'POST'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		cursor = connection.cursor()
		final = request.session.get("final",None)
		print final
		ind = int(request.POST.get("submit"))
		print ind
		ind = ind-1
		sid = int(request.session.get("start_pt",None))
		eid = int(request.session.get("end_pt",None))
		uname = str(request.session.get("uid",None))
		date = str(request.session.get("date",None))	
		seats = int(request.session.get("seats",None))
		cursor.execute('SELECT count(PNR) from Journey_details order by PNR desc')
		counter = cursor.fetchone()[0]
		if int(counter) == 0:
			pnr = 2016242452
		else:	
			cursor.execute('SELECT PNR from Journey_details order by PNR desc')
			pnrtop = cursor.fetchone()[0]
			pnr = pnrtop+1

		cursor.execute('SELECT xcoord from Station where s_id = \''+str(sid) + '\'')
		sx = cursor.fetchone()[0]
		cursor.execute('SELECT ycoord from Station where s_id = \''+str(sid) + '\'')
		sy = cursor.fetchone()[0]
		cursor.execute('SELECT xcoord from Station where s_id = \''+str(eid) + '\'')
		ex = cursor.fetchone()[0]
		cursor.execute('SELECT ycoord from Station where s_id = \''+str(eid) + '\'')
		ey = cursor.fetchone()[0]	
		dist = math.sqrt( math.pow(abs(sx-ex),2) + math.pow(abs(sy-ey),2))
		cursor.execute('SELECT base_fare from Pricing where train_id = \''+str(final[ind][0])+'\'')
		basef = cursor.fetchone()[0]
		cursor.execute('SELECT per_km from Pricing where train_id = \''+str(final[ind][0])+'\'')
		pk = cursor.fetchone()[0]
		cost = seats*(basef + (dist*pk))
		# Query = 'INSERT into journey_details (pnr, train_id, username, start_id, last_id, no_of_seats, cost) values (:1, :2, :3, :5, :6, :7, :8)'
		cursor.execute('INSERT into journey_details (pnr, train_id, username, date_of_journey, start_id, last_id, no_of_seats, cost) values (:p, :t, :u, :d, :s, :l, :n, :c)', {
			'p' : pnr, 
			't' : final[ind][0],
			'u' : uname,
			'd' : date,
			's' : sid,
			'l' : eid,
			'n' : seats,
			'c' : cost,
			})
		cursor.execute('SELECT order_no from Train_route where train_id =\'' +str(final[ind][0])+ '\' and s_id = \'' +str(sid)+ '\'')
		ostart = cursor.fetchone()[0]
		cursor.execute('SELECT order_no from Train_route where train_id =\'' +str(final[ind][0])+ '\' and s_id = \'' +str(eid)+ '\'')
		oend = cursor.fetchone()[0]
		if oend<ostart:
			oend,ostart = ostart,oend
		cursor.execute('SELECT s_id from Train_route where train_id =\'' +str(final[ind][0])+ '\' and order_no BETWEEN \'' +str(ostart)+ '\' and \'' +str(oend)+ '\'')	
		pforms = cursor.fetchall()
		for pform in pforms:
			cursor.execute('UPDATE Availability set Seats_Available = Seats_Available- \'' +str(seats)+ '\' where Train_id = \'' +str(final[ind][0])+ '\' and s_id = \'' +str(pform[0])+ '\' and doj =\'' +str(date)+ '\'')
		connection.commit()
		cursor.close()
		connection.close()
		request.session.flush()
		request.session['uid'] = uname
		return render (request, "dashboard.html",{})




def cancel(request):
	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')	

	if(request.method == 'GET'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		cursor = connection.cursor()
		uid = request.session.get('uid',None)
		print uid
		cursor.execute('SELECT * from Journey_details where username =\'' +str(uid)+ '\'')
		tickets = cursor.fetchall()
		length = len(tickets)
		print tickets
		connection.commit()
		cursor.close()
		connection.close()
		list2 = []
		for i in range(0,length):
			list2.append(i)	
		if length>0:
			context ={
				"tickets" : tickets,
				"length":list2,
			}
		else:
			context={
				"tickets" : tickets,
				"template_title": "No Tickets Found"
			}	
		

		return render (request, "cancel.html",context)

	if(request.method == 'POST'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		cursor = connection.cursor()	
		uid = request.session.get('uid',None)
		cursor.execute('SELECT * from Journey_details where username =\'' +str(uid)+ '\'')
		tickets = cursor.fetchall()
		ind = int(request.POST.get("submit"))
		print ind
		ind = ind - 1
		print ind
		pnr = tickets[ind][0]
		sid=tickets[ind][4]
		lid=tickets[ind][5]
		doj=tickets[ind][3]
		tnum=tickets[ind][1]
		seats = tickets[ind][6]
		cursor.execute('SELECT order_no from Train_route where Train_id = \'' +str(tnum)+ '\' and s_id = \'' +str(sid)+ '\'')
		ostart = cursor.fetchone()[0]
		cursor.execute('SELECT order_no from Train_route where Train_id = \'' +str(tnum)+ '\' and s_id = \'' +str(lid)+ '\'')
		oend = cursor.fetchone()[0]
		if oend<ostart:
			oend, ostart = ostart, oend
		cursor.execute('SELECT s_id from Train_route where Train_id =  \'' +str(tnum)+ '\' and order_no BETWEEN \'' +str(ostart)+ '\' and\'' +str(oend)+ '\' ')
		pforms = cursor.fetchall()
		for pform in pforms:
			cursor.execute('UPDATE Availability set Seats_Available = Seats_Available+ \'' +str(seats)+ '\' where Train_id = \'' +str(tnum)+ '\' and s_id = \'' +str(pform[0])+ '\' and doj = \'' +str(doj)+ '\' ')
		cursor.execute('DELETE from Journey_details where PNR = \'' +str(pnr)+ '\'')
		connection.commit()
		cursor.close()
		connection.close()
		context = {
			"template_title" :"Cancellation Succesful"
		}

		return render(request, "cancel.html",context)

def history(request):
	# if(request.method == 'GET'):
 # 		return render(request,"history.html",{})
 	sessionCheck = request.session.get('uid', None)
	
	if not sessionCheck:
		return HttpResponseRedirect('../login')

 	if(request.method == 'GET'):
		connection = cx_Oracle.connect('dbms/dbms@localhost/orcl')
		cursor = connection.cursor()
		uid = request.session.get('uid',None)
		cursor.execute('SELECT * from Journey_details where username =\'' +str(uid)+ '\'')
		tickets = cursor.fetchall()
		print tickets
		l = len(tickets)
		connection.commit()
		cursor.close()
		connection.close()
		if l>0:
			context = {
			"length" : 1,
			"tickets" : tickets
			}
		
		else:
			context = {
			"tickets" : tickets
			}

		return render (request, "history.html",context)