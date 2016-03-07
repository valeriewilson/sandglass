# sandglass.py - The executable file that prompts the user to input information for new or existing projects

# Planned additions: 
#   1. Allow the user to edit existing projects
#   2. Invoke the Jira API to retrieve information about epic status
#   3. Display statistics on each epic after the user exits the program
#   4. Use the information obtained through the prompt to display epic information in a GUI

import json

with open("projects.txt") as project_file:
	project_file = project_file.read()
	projects = json.loads(project_file)

while(True):
	response = raw_input('Do you want to add information about a new project, or are you done with the program? (type "n" for new or "d" for done): ')
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
			projects[l].update({"n":n})
			print "Epic name: " + n
		if s != "":
			projects[l].update({"s":s})
			print "Start date: " + s
		if e != "":
			projects[l].update({"e":e})
			print "Planned end date: " + e
		if a != "":
			projects[l].update({"a":a})
			print "Actual end date: " + a
	elif response == "d":
		# Allow user to exit the program
		break
	else:
		print "Invalid input. Please try again."

with open("projects.txt","w") as project_file:
	# Update projects.txt with new content
	json.dump(projects, project_file)