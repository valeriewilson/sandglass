# Gantt chart using Matplotlib, adapted from Clowers Research
# http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/

import json
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
from pylab import *
 
def format_date(input_date):
	if input_date != "":
		month = input_date.split("/")[0]
		day = input_date.split("/")[1]
		year = input_date.split("/")[2]
		date = dt.datetime(int(year), int(month), int(day))
		mdate = matplotlib.dates.date2num(date)
	else:
		mdate = ""
	return mdate
 
def generate_gantt_chart():
	# Data
	pos = arange(0.5,7.5,0.5)
	 
	ylabels = []
	customDates = []
	
	for epic in projects:
		epic_name = projects[epic]["epic_name"]
	 	start_date = projects[epic]["start_date"]
		exp_end_date = projects[epic]["exp_end_date"]
		est_end_date = projects[epic]["est_end_date"]
		act_end_date = projects[epic]["act_end_date"]

		ylabels.append(epic_name)
		customDates.append([format_date(start_date),format_date(exp_end_date),format_date(est_end_date),format_date(act_end_date)])

	task_dates = {}
	for i,task in enumerate(ylabels):
		task_dates[task] = customDates[i]
		print task_dates[task]
	 
	# Initialise plot
	fig = plt.figure()
	ax = fig.add_subplot(111)

	#Plot the data
	today = dt.date.today().strftime("%m/%d/%Y")
	today_date = format_date(today)

	start_date,exp_end_date,est_end_date,act_end_date = task_dates[ylabels[0]]
	ax.barh(0.45, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75, label = "Calculated")
	ax.barh(0.45, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='palegreen', alpha = 0.75, label = "Planned")
	if today_date - exp_end_date > 0:
		ax.barh(0.45, today_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='lightcoral', alpha = 0.75, label = "Behind")
	ax.barh(0.45, exp_end_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='palegoldenrod', alpha = 0.75, label = "Actual")
	for i in range(0,len(ylabels)-1):
		start_date,exp_end_date,est_end_date,act_end_date = task_dates[ylabels[i+1]]
		if start_date != "":
			if act_end_date == "":
				if est_end_date != "":
					ax.barh((i*0.5)+0.95, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75)
				if exp_end_date != "":
					ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='palegreen', alpha = 0.75)
					if today_date - exp_end_date > 0:
						ax.barh((i*0.5)+0.95, today_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='lightcoral', alpha = 0.75)
			else:
				ax.barh((i*0.5)+0.95, act_end_date - start_date, left=start_date, height=0.3, align='center', color='palegoldenrod', alpha = 0.75)
				if exp_end_date != "":
					ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='palegreen', alpha = 0.75)
					if act_end_date > exp_end_date:
						ax.barh((i*0.5)+0.95, act_end_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='lightcoral', alpha = 0.75)
				if est_end_date != "":
					ax.barh((i*0.5)+0.95, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75)
	 
	# Format the y-axis
	locsy, labelsy = yticks(pos,ylabels)
	plt.setp(labelsy, fontsize = 14)
	 
	# Format the x-axis
	max_value = 1 + (len(ylabels) / 2)
	ax.axis('tight')
	ax.set_ylim(ymin = -0.1, ymax = max_value)
	ax.grid(color = 'g', linestyle = ':')
	 
	ax.xaxis_date()
	 
	rule = rrulewrapper(MONTHLY, interval=1)
	loc = RRuleLocator(rule)
	formatter = DateFormatter("%b '%y")
	 
	ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	labelsx = ax.get_xticklabels()
	plt.setp(labelsx, rotation=30, fontsize=12)
	 
	# Format the legend
	font = font_manager.FontProperties(size='medium')
	ax.legend(loc=1,prop=font)
	 
	# Finish up
	ax.invert_yaxis()
	fig.autofmt_xdate()
	return plt.show()

with open("projects.txt") as project_file:
   project_file = project_file.read()
   projects = json.loads(project_file)