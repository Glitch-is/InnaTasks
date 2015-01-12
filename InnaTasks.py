###
# Author: Glitch <Glitch@Glitch.is>
# Name: InnaTasks
# Description:
# Usage: Run the script with the following command 'python3 InnaTasks.py'. Enter your username and password and let the script do it's work, it will leave
# you with an iCalendar file 'Calendar.ics', now you can import that into the application of your choice such as Google Calendar.
#
# Report any bugs on GitHub <https://github.com/Glitch-is/InnaCalendar>
###

import os
import requests
from getpass import getpass
from icalendar import Calendar, Event

while True:
    u = input("Kennitala: ") # Prompt the user for their social security number
    p = getpass() # Prompt the user for their password wich doesn't get displayed thanks to the getpass module

    payload = {
        'Kennitala': u,
        'Lykilord': p,
        '_ROWOPERATION': 'Staðfesta'
    } # Initialize the login payload

    print("Attempting to log into inna.is")

    login = requests.post('https://www.inna.is/login.jsp', data=payload) # Login to the old Inna login system with the payload

    if("Innskráning tókst ekki" in login.text):
        print("Login Failed. Please try again...")
    else:
        print("Login Successful")
        break;


cookie = {"JSESSIONID": login.cookies["JSESSIONID"]} # Get the Session from the response cookie to use for next step of the login

oldInna = requests.get('https://www.inna.is/opna.jsp?adgangur=0', cookies=cookie) # Tell inna we want to use the new site so it will send us a token to skip the new inna authentication, how convienient?
activate = oldInna.text.split("'")[1] # Parse the link to the new inna with our token

newInna = requests.get(activate) # Activate our new session
newCookie = {"JSESSIONID": newInna.cookies["JSESSIONID"]} # Store our new session in a cookie

studentInfo = requests.get('https://nam.inna.is/inna11/api/UserData/GetLoggedInUser', cookies=newCookie) # Get the student info
studentId = studentInfo.json()['studentId'] # Parse the studentId from the studentInfo

print("Fetching Assignments...")

assignment = requests.get("https://nam.inna.is/inna11/api/GetAssignments/GetStudentAssignments?control=0&group_id=&module_id=&order=0&type=", cookies=newCookie) # Get the user assignments
assjs = assignment.json() # Store our JSON Object

print("Fetching Homework...")

homework = requests.get("https://nam.inna.is/inna11/api/Homework/GetStudentHomework?group_id=", cookies=newCookie) # Get the user homework
homejs = homework.json() # Store our JSON Object

print("Fetching Tests...")

tests = requests.get("https://nam.inna.is/inna11/api/Timetable/GetStudentExamSchedule?studentId=", cookies=newCookie) # Get the user tests
testsjs = tests.json() # Store our JSON Object

# Combine all the items

print("Adding Items to TaskWarrior")

print("Finished")
