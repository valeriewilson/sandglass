# sandglass.py - The executable file that prompts the user to input information for new or existing projects and displays statistics about each project on exiting

# Planned additions: 
#   1. Use the information obtained through the prompt to display epic information in a GUI
#   2. Sort projects by exp_end_date

import json
import numpy as np
import datetime as dt
import datetime
import time
from jira.client import GreenHopper

def jira_login():
	username = raw_input("Jira username: ")
	password = raw_input("Jira password: ")
	company = raw_input("Company (as used in Jira URL): ")
	jira_url = "https://" + company + ".jira.com"
	options = {
		'server': jira_url
	}
	gh = GreenHopper(options, basic_auth=(username, password))
	return gh

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
			display_project_stats(epic,gh)
		else:
			print "Epic link: " + epic
		print "----------------"

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

def display_project_stats(epic,gh_cred):
	if "start_date" in projects[epic]:
		start = dt.date(int(projects[epic]["start_date"].split("/")[2]), int(projects[epic]["start_date"].split("/")[0]), int(projects[epic]["start_date"].split("/")[1]))
		today = dt.date.today()	
		percent_completed = estimate_percent_complete(epic, gh_cred)[0] * 100
		percent_estimated = estimate_percent_complete(epic, gh_cred)[1] * 100

		# Expected business days elapsed
		if "exp_end_date" in projects[epic]:
			exp_end = dt.date(int(projects[epic]["exp_end_date"].split("/")[2]), int(projects[epic]["exp_end_date"].split("/")[0]), int(projects[epic]["exp_end_date"].split("/")[1]))
			print "Expected business days elapsed: %i" % np.busday_count(start,exp_end)
		
		# Actual business days elapsed (using act_end_date if project is completed)
		if "act_end_date" in projects[epic]:
			exp_end = dt.date(int(projects[epic]["exp_end_date"].split("/")[2]), int(projects[epic]["exp_end_date"].split("/")[0]), int(projects[epic]["exp_end_date"].split("/")[1]))
			act_end = dt.date(int(projects[epic]["act_end_date"].split("/")[2]), int(projects[epic]["act_end_date"].split("/")[0]), int(projects[epic]["act_end_date"].split("/")[1]))
			print "Actual business days elapsed: %i" % np.busday_count(start,act_end)
			if act_end > exp_end:
				days_behind = np.busday_count(exp_end,act_end)
			else:
				days_behind = 0
		else:
			exp_end = dt.date(int(projects[epic]["exp_end_date"].split("/")[2]), int(projects[epic]["exp_end_date"].split("/")[0]), int(projects[epic]["exp_end_date"].split("/")[1]))
			if start <= today and percent_completed != 0:
				days_elapsed = np.busday_count(start,today)
				est_total_days = days_elapsed * 100 / percent_completed
				est_end = estimate_end_date(start,est_total_days)
				est_days_remaining = np.busday_count(today,est_end)
				print "Estimated end date: %s" % est_end.strftime("%m/%d/%Y")
				print "Estimated business days remaining: %i" % est_days_remaining
				print "Estimated project completion: %i%%" % (percent_completed)
				print "Accuracy of estimate: %i%%" % (percent_estimated)
			else:
				days_elapsed = 0
			
			print "Business days elapsed to date: %i" % days_elapsed

			if today > exp_end:
				 days_behind = np.busday_count(exp_end,today)
			else:
				days_behind = 0
		
		print "Business days behind schedule: %i" % days_behind

def estimate_percent_complete(epic_link,gh_cred):
	search_query = '"Epic Link"=' + epic_link
	issues_in_epic = gh.search_issues(search_query)
	total_story_points = 0
	completed_story_points = 0
	estimated_tickets = 0
	unestimated_tickets = 0

	for ticket in issues_in_epic:
		issue_details = gh.issue(ticket).fields
		
		if "customfield_10013" in dir(issue_details):
			story_points = issue_details.customfield_10013
			if story_points is not None:
				total_story_points += story_points
				estimated_tickets += 1
				if issue_details.status.name in ['Resolved','Closed','Done']:
					completed_story_points += story_points
			else:
				unestimated_tickets += 1

	percentage_completed = completed_story_points / total_story_points
	percentage_scoped = float(estimated_tickets) / (estimated_tickets + unestimated_tickets)
	return (percentage_completed,percentage_scoped)

def estimate_end_date(start_date, days_remaining):
    est_business_days = days_remaining
    est_end_date = start_date
    while est_business_days > 0:
        est_end_date += datetime.timedelta(days=1)
        weekday = est_end_date.weekday()
        if weekday >= 5:
            continue
        est_business_days -= 1
    return est_end_date

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
		gh = jira_login()
		break
	else:
		print "Invalid input. Please try again."

# Display the new contents of projects.txt
epic_list = projects.keys()
display_project_list(epic_list,display_stats=True)

with open("projects.txt","w") as project_file:
	# Update projects.txt with new content
	json.dump(projects, project_file)