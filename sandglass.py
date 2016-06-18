import json
from jira.client import GreenHopper
import datetime as dt
import numpy as np
import gantt_chart

class Epic(object):
	def __init__(self, name, link, start_date, exp_end_date, act_end_date, est_end_date, exp_days_elapsed, days_elapsed, bus_days_behind, est_days_remaining, est_perc_compl, accuracy):
		self.name = name
		self.link = link
		self.start_date = start_date
		self.exp_end_date = exp_end_date
		self.act_end_date = act_end_date
		self.est_end_date = est_end_date
		self.exp_days_elapsed = exp_days_elapsed
		self.days_elapsed = days_elapsed
		self.bus_days_behind = bus_days_behind
		self.est_days_remaining = est_days_remaining
		self.est_perc_compl = est_perc_compl
		self.accuracy = accuracy
	
	def create_project(self):
		projects.append({
			"name": self.name,
			"link": self.link,
			"start_date": self.start_date,
			"exp_end_date": self.exp_end_date,
			"act_end_date": self.act_end_date,
			"est_end_date": "",
			"exp_days_elapsed": "",
			"days_elapsed": "",
			"bus_days_behind": "",
			"est_days_remaining": "",
			"est_perc_compl": "",
			"accuracy": ""
			})
		print "---New entry---"
		print "Project name: " + self.name
		print "Epic link: " + self.link
		print "Start date: " + self.start_date
		print "Planned end date: " + self.exp_end_date
		print "Actual end date: " + self.act_end_date
	
	def update_project(self,epic,field,value):
		for p in projects:
			if p["link"] == epic:
				p[field] = new_value
	
	def display_project(self,display_stats):
		print "Project name: " + self.name
		print "Start date: " + self.start_date
		print "Planned end date: " + self.exp_end_date
		if self.act_end_date != "":
			print "Actual end date: " + self.act_end_date
		print "Epic link: " + self.link
		if display_stats and self.start_date != "":
			if self.exp_end_date != "":
				project.metrics_expected(self.start_date, self.exp_end_date)
			if self.act_end_date != "":
				project.metrics_actual(self.start_date, self.exp_end_date, self.act_end_date)
			else:
				project.metrics_calculated(self.link,self.start_date,self.exp_end_date,self.act_end_date, gh)
		print "----------------"
	
	def metrics_expected(self,start_date,exp_end_date):
		start = dt.date(int(start_date.split("/")[2]), int(start_date.split("/")[0]), int(start_date.split("/")[1]))
		exp_end = dt.date(int(exp_end_date.split("/")[2]), int(exp_end_date.split("/")[0]), int(exp_end_date.split("/")[1]))
		self.exp_days_elapsed = np.busday_count(start,exp_end)
		print "Expected business days elapsed: %i" % self.exp_days_elapsed
	
	def metrics_actual(self,start_date,exp_end_date,act_end_date):
		start = dt.date(int(start_date.split("/")[2]), int(start_date.split("/")[0]), int(start_date.split("/")[1]))
		exp_end = dt.date(int(exp_end_date.split("/")[2]), int(exp_end_date.split("/")[0]), int(exp_end_date.split("/")[1]))
		act_end = dt.date(int(act_end_date.split("/")[2]), int(act_end_date.split("/")[0]), int(act_end_date.split("/")[1]))
		self.act_days_elapsed = np.busday_count(start,act_end)
		if act_end > exp_end:
			self.bus_days_behind = np.busday_count(exp_end,act_end)
		else:
			self.bus_days_behind = 0
		print "Actual business days elapsed: %i" % self.act_days_elapsed
		print "Business days behind schedule: %i" % self.bus_days_behind
	
	def metrics_calculated(self,link,start_date,exp_end_date,act_end_date, gh):
		start = dt.date(int(start_date.split("/")[2]), int(start_date.split("/")[0]), int(start_date.split("/")[1]))
		exp_end = dt.date(int(exp_end_date.split("/")[2]), int(exp_end_date.split("/")[0]), int(exp_end_date.split("/")[1]))
		today = dt.date.today()
		project.estimate_percent_complete(link,gh)
		self.est_perc_compl = project.estimate_percent_complete(link, gh)[0] * 100
		self.accuracy = project.estimate_percent_complete(link, gh)[1] * 100
		
		if start <= today and self.act_end_date == "" and self.est_perc_compl != 0:
			days_elapsed = np.busday_count(start,today)
			est_total_days = days_elapsed * 100 / self.est_perc_compl
			est_end = project.estimate_end_date(start,est_total_days)
			self.est_end_date = est_end.strftime("%m/%d/%Y")
			self.est_days_remaining = np.busday_count(today,est_end)
			print "Estimated end date: %s" % self.est_end_date
			print "Estimated business days remaining: %i" % self.est_days_remaining
			print "Estimated project completion: %i%%" % self.est_perc_compl
			print "Accuracy of estimate: %i%%" % self.accuracy
		else:
			days_elapsed = 0
		print "Business days elapsed to date: %i" % days_elapsed

		if today > exp_end:
			 self.bus_days_behind = np.busday_count(exp_end,today)
		else:
			self.bus_days_behind = 0
		print "Business days behind schedule: %i" % self.bus_days_behind
	
	def estimate_percent_complete(self,link,gh_cred):
		search_query = '"Epic Link"=' + link
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
	
	def estimate_end_date(self,start_date, days_remaining):
	    est_business_days = days_remaining
	    est_end_date = start_date
	    while est_business_days > 0:
	        est_end_date += dt.timedelta(days=1)
	        weekday = est_end_date.weekday()
	        if weekday >= 5:
	            continue
	        est_business_days -= 1
	    return est_end_date

def jira_login():
	username = raw_input("Jira username: ")
	password = raw_input("Jira password: ")
	company = raw_input("Company (as used in Jira URL): ")
	jira_url = "https://" + company + ".jira.com"
	options = {'server': jira_url}
	gh = GreenHopper(options, basic_auth=(username, password))
	return gh

with open("new_format.txt") as project_file:
	project_file = project_file.read()
	projects = json.loads(project_file)

while(True):
	response = raw_input('Do you want to add information about a new or existing project, or are you done with the program? (type "n" for new, "e" for existing, or "d" for done): ')
	if response == "n":
		new_epic_name = raw_input("What is the project name?: ")
		new_epic = raw_input("What is the epic link?: ")
		new_start_date = raw_input("What is the start date (MM/DD/YYYY)?: ")
		new_exp_end_date = raw_input("What is the planned end date (MM/DD/YYYY)?: ")
		new_act_end_date = raw_input("What is the actual end date (MM/DD/YYYY)?: ")
		new_project = Epic(new_epic_name, new_epic, new_start_date, new_exp_end_date, new_act_end_date, "", "", "", "", "", "", "").create_project()
	elif response == "e":
		print "--- Epic information ---"
		for p in projects:
			project = Epic(p["name"], p["link"], p["start_date"], p["exp_end_date"], p["act_end_date"], p["est_end_date"], p["exp_days_elapsed"], p["days_elapsed"], p["bus_days_behind"], p["est_days_remaining"], p["est_perc_compl"], p["accuracy"])
			project.display_project(display_stats=False)
		epic = raw_input("What is the epic link?: ")
		field = raw_input("Which field would you like to update?: ")
		if field in ("name", "link", "start_date", "exp_end_date", "act_end_date"):
			for p in projects:
				if p["link"] == epic:
					edit_project = Epic(p["name"], p["link"], p["start_date"], p["exp_end_date"], p["act_end_date"], p["est_end_date"], p["exp_days_elapsed"], p["days_elapsed"], p["bus_days_behind"], p["est_days_remaining"], p["est_perc_compl"], p["accuracy"])
					print "Current value: %s" %p[field]
					new_value = raw_input("New value: ")
					edit_project.update_project(epic, field, new_value)
		else:
			print "Invalid input."
	elif response == "d":
		gh = jira_login()
		break
	else:
		print "Invalid input. Please try again."

for p in projects:
	project = Epic(p["name"], p["link"], p["start_date"], p["exp_end_date"], p["act_end_date"], p["est_end_date"], p["exp_days_elapsed"], p["days_elapsed"], p["bus_days_behind"], p["est_days_remaining"], p["est_perc_compl"], p["accuracy"])
	project.display_project(display_stats=True)

with open("projects.txt","w") as project_file:
	json.dump(projects, project_file)