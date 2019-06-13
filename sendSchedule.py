'''
	Script to send email of schedule and todos for today
	To be triggered by crontab at 9am each morning
'''

import datetime
import smtplib

def sendEmail(apts, todos):
	"""Send email of todays schedule
	
	Args:
	    apts (str): str containing all appoinntments, formatted
	    todos (str): str containing all todo, formatted
	"""
	gmail_user = 'YOUR EMAIL ADDRESS HERE'  
	gmail_password = 'YOUR PASSWORD HERE'

	sent_from = gmail_user  
	to = ['EMAIL ADDRESS TO RECEIVE SCHEDULE HERE']  
	subject = 'Daily Schedule'  

	email_text = "\nFrom: {}\nTo: {}\nSubject: {}\n\n| --------------- Daily Schedule --------------- |\n\n{}\n| -------------------- Todo -------------------- |\n\n{}".format(sent_from, ", ".join(to), subject, apts, todos)

	print(email_text)

	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, email_text)
		server.close()

		print('Email sent!')
	except Exception as e: 
		print(e)
		print('Something went wrong...')

def apptMessage(apps):
	"""Generate string portion of email for the appointments today
	
	Args:
	    apps (list<tuple<name, datetime, datetime>>): appointments today
	
	Returns:
	    String: message for the appointment portion of the email
	"""
	msg = ""

	for app in apps:
		name, start, end = app
		msg += "{:25}   {} -> {}\n\n".format(name, str(start.time()), 
				str(end.time()))

	return msg

def todoMessage(todos):
	"""Generate the string message for the todo portion of the email
	
	Args:
	    todos (list<tuple<int, str>>): list of todos and their weight
	
	Returns:
	    TYPE: Description
	"""

	todos.sort()
	msg = ""

	for todo in todos:
		msg += "[{}]   {}".format(todo[0], todo[1])
	return msg

def parseApts():
	"""Parse the appointments file
	
	Returns:
	    List<tuple<str, datetime, datetime>>: list of tuples holding name, 
	    	start and end time
	"""
	apts = open('PATH TO .calcurse/apts', 'r') # Will generally be ~/.calcurse/apts on mac
	appointmentsToday = []

	for line in apts :
		splitName = line.split("|")
		if len(splitName) != 2:
			splitName = line.split("!")

		if len(splitName) != 2:
			continue

		name = splitName[1][:-1]

		splitTime = splitName[0].split(" -> ")
		
		start = splitTime[0][:18]
		end = splitTime[1][:18]
		start = datetime.datetime.strptime(start, '%m/%d/%Y @ %H:%M')
		end = datetime.datetime.strptime(end, '%m/%d/%Y @ %H:%M')

		if start.date() == datetime.datetime.today().date():
			appointmentsToday.append((name, start, end))

	apts.close()
	appointmentsToday = sorted(appointmentsToday, key=lambda x: x[1])
	return appointmentsToday

def parseTodo():
	"""Parse the Todo file
	
	Returns:
	    List<Tuple<int, str>>: list of tuples containing the weight and name
	"""
	file = open('PATH TO.calcurse/todo', 'r') # Will generally be ~/.calcurse/todo on Mac
	todos = []

	for line in file :
		l = line.split(" ", 1)
		weight = int(l[0][1:-1])
		name = l[1]
		todos.append((weight, name))

	return todos


def main():

	# Get lists
	appointments = parseApts()
	todos = parseTodo()

	# Turn into string for email
	aMsg = apptMessage(appointments)
	tMsg = todoMessage(todos)

	# Send Email
	sendEmail(aMsg, tMsg)

main()
