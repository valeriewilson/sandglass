# Gantt chart using Matplotlib, adapted from Clowers Research
# http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/

# NOTE: Currently uses manually-entered values

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
from pylab import *
 
def create_date(month,day,year):
	date = dt.datetime(int(year), int(month), int(day))
	mdate = matplotlib.dates.date2num(date)
	return mdate
 
def generate_gantt_chart():
	# Data
	pos = arange(0.5,5.5,0.5)
	 
	ylabels = []
	ylabels.append('EPIC-1')
	ylabels.append('EPIC-2')
	ylabels.append('EPIC-3')
	ylabels.append('EPIC-4')
	ylabels.append('EPIC-5')
	ylabels.append('EPIC-6')
	ylabels.append('EPIC-7')
	 
	effort = []
	 
	customDates = []
	customDates.append([create_date(9,24,2015),create_date(3,14,2016),create_date(3,22,2016), 0])
	customDates.append([create_date(12,7,2015),create_date(3,16,2016),create_date(4,4,2016), 0])
	customDates.append([create_date(2,29,2016),create_date(3,25,2016),create_date(3,25,2016), 0])
	customDates.append([create_date(1,25,2016),create_date(3,28,2016),create_date(3,31,2016), 0])
	customDates.append([create_date(9,24,2015),create_date(3,28,2016),create_date(7,18,2016), 0])
	customDates.append([create_date(2,9,2016),create_date(4,25,2016),create_date(7,22,2016), 0])
	customDates.append([create_date(11,15,2015),create_date(3,9,2016),0,create_date(3,11,2016)])

	task_dates = {}
	for i,task in enumerate(ylabels):
		task_dates[task] = customDates[i]
	 
	# Initialise plot
	fig = plt.figure()
	ax = fig.add_subplot(111)

	#Plot the data
	today = dt.date.today()
	today_date = create_date(today.month,today.day,today.year)

	start_date,exp_end_date,est_end_date,act_end_date = task_dates[ylabels[0]]
	ax.barh(0.45, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75, label = "Calculated")
	ax.barh(0.45, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='dodgerblue', alpha = 0.75, label = "Planned")
	ax.barh(0.45, today_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='red', alpha = 0.75, label = "Behind")
	ax.barh(0.45, exp_end_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='silver', alpha = 0.75, label = "Actual")
	for i in range(0,len(ylabels)-1):
		start_date,exp_end_date,est_end_date,act_end_date = task_dates[ylabels[i+1]]
		if act_end_date == 0:
			ax.barh((i*0.5)+0.95, est_end_date - start_date, left=start_date, height=0.3, align='center', color='gold', alpha = 0.75)
			ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='dodgerblue', alpha = 0.75)
			if today_date - exp_end_date > 0:
				ax.barh((i*0.5)+0.95, today_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='red', alpha = 0.75)
		else:
			ax.barh((i*0.5)+0.95, act_end_date - start_date, left=start_date, height=0.3, align='center', color='silver', alpha = 0.75)
			ax.barh((i*0.5)+0.95, exp_end_date - start_date, left=start_date, height=0.1, align='center', color='dodgerblue', alpha = 0.75)
			if act_end_date > exp_end_date:
				ax.barh((i*0.5)+0.95, act_end_date - exp_end_date, left=exp_end_date, height=0.1, align='center', color='red', alpha = 0.75)
	 
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
	font = font_manager.FontProperties(size='small')
	ax.legend(loc=1,prop=font)
	 
	# Finish up
	ax.invert_yaxis()
	fig.autofmt_xdate()
	return plt.show()