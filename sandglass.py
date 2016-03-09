# sandglass.py - The executable file that prompts the user to input information for new or existing projects

# Planned additions: 
#   1. Invoke the Jira API to retrieve information about epic status
#   2. Display statistics on each epic after the user exits the program
#   3. Use the information obtained through the prompt to display epic information in a GUI

import json
import numpy as np
import datetime as dt
from datetime import date
import time

def display_project_list(epic_list,display_stats):
	print "Epic information"
	for epic in epic_list:
		if "epic_name" in projects[epic]:
			print "Project name: " + projects[epic]["epic_name"]
		if "start_date" in projects[epic]:
			print "Start date: " + projects[epic]["start_date"]
		if "exp_end_date" in projects[epic]:
			print "Expected end date: " + projects[epic]["exp_end_date"]
		if "act_end_date" in projects[epic]:
			print "Actual end date: " + projects[epic]["act_end_date"]
		if display_stats:
			display_project_stats(epic)
		else:
			print "Epic link: " + epic
		print "----------------"

def display_project_stats(epic):
	if "start_date" in projects[epic] and "exp_end_date" in projects[epic]:
		start = dt.date(int(projects[epic]["start_date"].split("/")[2]), int(projects[epic]["start_date"].split("/")[0]), int(projects[epic]["start_date"].split("/")[1]))
		end = dt.date(int(projects[epic]["exp_end_date"].split("/")[2]), int(projects[epic]["exp_end_date"].split("/")[0]), int(projects[epic]["exp_end_date"].split("/")[1]))
		print "Expected business days elapsed: %i" % np.busday_count(start,end)
	if "start_date" in projects[epic] and "act_end_date" in projects[epic]:
		start = dt.date(int(projects[epic]["start_date"].split("/")[2]), int(projects[epic]["start_date"].split("/")[0]), int(projects[epic]["start_date"].split("/")[1]))
		end = dt.date(int(projects[epic]["act_end_date"].split("/")[2]), int(projects[epic]["act_end_date"].split("/")[0]), int(projects[epic]["act_end_date"].split("/")[1]))
		print "Actual business days elapsed: %i" % np.busday_count(start,end)

with open("projects.txt") as project_file:
	project_file = project_file.read()
	projects = json.loads(project_file)

while(True):
	response = raw_input('Do you want to add information about a new or existing project, or are you done with the program? (type "n" for new, "e" for existing, or "d" for done): ')
	if response == "n":
		# Prompt user for information about new project
		l = raw_input("What is the epic link?: ")
		n = raw_input("What is the project name?: ")
		s = raw_input("What is the start date (MM/DD/YYYY)?: ")
		e = raw_input("What is the planned end date (MM/DD/YYYY)?: ")
		a = raw_input("What is the actual end date (MM/DD/YYYY)?: ")
		
		# Add information to projects variable (if provided) and display information added
		projects.update({l:{}})
		print "--New entry--"
		print "Epic link: " + l
		if n != "":
			projects[l].update({"epic_name":n})
			print "Project name: " + n
		if s != "":
			projects[l].update({"start_date":s})
			print "Start date: " + s
		if e != "":
			projects[l].update({"exp_end_date":e})
			print "Planned end date: " + e
		if a != "":
			projects[l].update({"act_end_date":a})
			print "Actual end date: " + a
	
	elif response == "e":
		# Display all projects
		epic_list = projects.keys()
		display_project_list(epic_list,False)
		
		# Prompt user for the field to edit and display current entry
		edit_project = raw_input("Which epic would you like to edit? (type the epic link): ")
		edit_field = raw_input('Which field would you like to add or update - epic_name, start_date, exp_end_date, or act_end_date?: ')
		
		# Allow the user to input the new/updated value, save to projects variable, and output value
		if edit_field in ("epic_name","start_date","exp_end_date","act_end_date"):
			if edit_field in projects[edit_project].keys():
				print "Current value: %s" % projects[edit_project][edit_field]
				new_value = raw_input("What is the new value?: ")
			else:
				new_value = raw_input("What is the value for this field?: ")
			projects[edit_project][edit_field] = new_value
			print "New value: %s" % projects[edit_project][edit_field]
		else:
			print "%s is an invalid field option." % edit_field
	elif response == "d":
		# Exit the program
		break
	else:
		print "Invalid input. Please try again."

# Display the new contents of projects.txt
epic_list = projects.keys()
display_project_list(epic_list,True)

with open("projects.txt","w") as project_file:
	# Update projects.txt with new content
	json.dump(projects, project_file)