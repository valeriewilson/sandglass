# Gantt chart using Matplotlib, adapted from Clowers Research
# http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/

import json
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as font_manager
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
	ylabels = []
	customDates = []
	
	for epic in projects:
		epic_name = epic["name"]
	 	start_date = epic["start_date"]
		exp_end_date = epic["exp_end_date"]
		est_end_date = epic["est_end_date"]
		act_end_date = epic["act_end_date"]

		ylabels.append(epic_name)
		customDates.append([format_date(start_date),format_date(exp_end_date),format_date(est_end_date),format_date(act_end_date)])

	task_dates = {}
	for i,task in enumerate(ylabels):
		task_dates[task] = customDates[i]
	 
	# Initialise plot
	fig = plt.figure()
	ax = fig.add_subplot(111)

	# Set up legend
	calculated = mpatches.Patch(color="gold", label="Calculated")
	planned = mpatches.Patch(color="palegreen", label="Planned")
	behind = mpatches.Patch(color="lightcoral", label="Behind")
	actual = mpatches.Patch(color="palegoldenrod", label="Actual")

	colors = [calculated,planned,behind,actual]
	labels = [color.get_label() for color in colors]
	plt.legend(colors, labels)

	# Plot the data
	today = format_date(dt.date.today().strftime("%m/%d/%Y"))

	for i in range(-1,len(ylabels)-1):
		start_date,exp_end_date,est_end_date,act_end_date = task_dates[ylabels[i+1]]
		if start_date != "":
			if act_end_date == "":
				if est_end_date != "":
					ax.barh((i*0.5)+0.95, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75)
				if exp_end_date != "":
					ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='palegreen', alpha = 0.75)
					if today - exp_end_date > 0:
						ax.barh((i*0.5)+0.95, today - exp_end_date, left=exp_end_date, height=0.1, align='center', color='lightcoral', alpha = 0.75)
			else:
				ax.barh((i*0.5)+0.95, act_end_date - start_date, left=start_date, height=0.3, align='center', color='palegoldenrod', alpha = 0.75)
				if exp_end_date != "":
					ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='palegreen', alpha = 0.75)
					if act_end_date > exp_end_date:
						ax.barh((i*0.5)+0.95, act_end_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='lightcoral', alpha = 0.75)
				if est_end_date != "":
					ax.barh((i*0.5)+0.95, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75)
	 
	# Format the y-axis
	pos = arange(0.45,(len(ylabels) / 2),0.5)
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

generate_gantt_chart()
