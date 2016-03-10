# sandglass.py - The executable file that prompts the user to input information for new or existing projects and displays statistics about each project on exiting

# Planned additions: 
#   1. Invoke the Jira API to retrieve information about epic status
#   2. Display statistics on each epic after the user exits the program
#   3. Use the information obtained through the prompt to display epic information in a GUI
#   4. Sort projects by exp_end_date

import json
import numpy as np
import datetime as dt
from datetime import date
import time

def display_project_list(epic_list,display_stats):
	print "Epic information:"
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
	if "start_date" in projects[epic]:
		start = dt.date(int(projects[epic]["start_date"].split("/")[2]), int(projects[epic]["start_date"].split("/")[0]), int(projects[epic]["start_date"].split("/")[1]))
		
		# Expected business days elapsed
		if "exp_end_date" in projects[epic]:
			end = dt.date(int(projects[epic]["exp_end_date"].split("/")[2]), int(projects[epic]["exp_end_date"].split("/")[0]), int(projects[epic]["exp_end_date"].split("/")[1]))
			print "Expected business days elapsed: %i" % np.busday_count(start,end)
		
		# Actual business days elapsed (using act_end_date if project is completed)
		if "act_end_date" in projects[epic]:
			end = dt.date(int(projects[epic]["act_end_date"].split("/")[2]), int(projects[epic]["act_end_date"].split("/")[0]), int(projects[epic]["act_end_date"].split("/")[1]))
			print "Actual business days elapsed: %i" % np.busday_count(start,end)
		else:
			today = dt.date.today()
			print "Business days elapsed to date: %i" % np.busday_count(start,today)

		# Business days behind schedule
			# If actual end date is given
			# 	If > planned end date: (actual end date) - (planned end date)
			# 	Else: 0
			# If actual end date is not given
			# 	If today > planned end date: (today) - (planned end date)
			# 	Else: 0

		# Jira epic % complete
			# [epicStats][percentageCompleted]

		# Accuracy of Jira estimate
			# [epicStats][percentageEstimated] value in percentage format (integer)

		# Jira expected end date - simple model
			# start_date + [(today) - (start date)] / [epicStats][percentageCompleted]

		# Jira remaining time elapsed
			# If actual end date is given: 0
			# If actual end date is not given: (Jira expected end date) - (today)

def create_project(epic_list):
	projects.update({new_epic:{}})
	print "--New entry--"
	print "Epic link: " + new_epic
	if new_epic_name != "":
		projects[new_epic].update({"epic_name":new_epic_name})
		print "Project name: " + new_epic_name
	if new_start_date != "":
		projects[new_epic].update({"start_date":new_start_date})
		print "Start date: " + new_start_date
	if new_exp_end_date != "":
		projects[new_epic].update({"exp_end_date":new_exp_end_date})
		print "Planned end date: " + new_exp_end_date
	if new_act_end_date != "":
		projects[new_epic].update({"act_end_date":new_act_end_date})
		print "Actual end date: " + new_act_end_date

def edit_project(epic,field):
	if field in ("epic_name","start_date","exp_end_date","act_end_date"):
		if field in projects[epic].keys():
			print "Current value: %s" % projects[epic][field]
			new_value = raw_input("What is the new value?: ")
		else:
			new_value = raw_input("What is the value for this field?: ")
		projects[epic][field] = new_value
		print "New value: %s" % projects[epic][field]
	else:
		print "%s is an invalid field option." % field

with open("projects.txt") as project_file:
	project_file = project_file.read()
	projects = json.loads(project_file)

while(True):
	response = raw_input('Do you want to add information about a new or existing project, or are you done with the program? (type "n" for new, "e" for existing, or "d" for done): ')
	if response == "n":
		# Prompt user for information about new project
		new_epic = raw_input("What is the epic link?: ")
		new_epic_name = raw_input("What is the project name?: ")
		new_start_date = raw_input("What is the start date (MM/DD/YYYY)?: ")
		new_exp_end_date = raw_input("What is the planned end date (MM/DD/YYYY)?: ")
		new_act_end_date = raw_input("What is the actual end date (MM/DD/YYYY)?: ")
		
		# Add information to projects variable (if provided) and display information added
		create_project(projects)
	
	elif response == "e":
		# Display all projects
		epic_list = projects.keys()
		display_project_list(epic_list,display_stats=False)
		
		# Prompt user for the field to edit and display current entry
		edit_epic = raw_input("Which epic would you like to edit? (type the epic link): ")
		edit_field = raw_input('Which field would you like to add or update - epic_name, start_date, exp_end_date, or act_end_date?: ')
		
		# Allow the user to input the new/updated value, save to projects variable, and output value
		edit_project(edit_epic,edit_field)

	elif response == "d":
		# Exit the program
		break
	else:
		print "Invalid input. Please try again."

# Display the new contents of projects.txt
epic_list = projects.keys()
display_project_list(epic_list,display_stats=True)

with open("projects.txt","w") as project_file:
	# Update projects.txt with new content
	json.dump(projects, project_file)