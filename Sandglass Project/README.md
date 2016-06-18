# sandglass
Project tracking tool that integrates with Jira data to estimate project length.

I. File List
-------------------------
* sandglass.py - Executable file that asks for new/updated project information and returns timeline-based metrics
* projects.txt - Project list in json format based on user inputs when running sandglass.py
* README - You're looking at it!
* gantt_chart.py - Script that generates a Gantt chart

![Example Gantt Chart](example_gantt_chart.png?raw=true "Example Gantt Chart")

II. Epic Metrics
-------------------------
User-provided values:
* Project name: epic name
* Start date: beginning of the epic
* Expected end date: epic completion date

Calculated values:
* Expected business days elapsed: expected end - start date
* Estimated end date: based on story points estimated & completed within the epic
* Estimated business days remaining: estimated end - start date
* Estimated project completion: story points completed / total
* Accuracy of estimate: tickets with story points / total
* Business days elapsed to date: today - start date
* Business days behind schedule: today - expected end date (if today > expected end date)

III. Notes / Limitations
-------------------------
* I use "project" and "epic" interchangeably, even though *technically* they are quite different in Jira (I mean "epic" in both cases)
* Incomplete projects assume consistent resources (time and human)
* Business day calculations do not bear in mind holidays, just weekends

IV. TL;DR (Installation)
-------------------------
* Install Jira: sudo pip install jira --upgrade --ignore-installed six
* Install Matplotlib: sudo pip install matplotlib
* Run the program: python sandglass.py
* Generate the Gantt chart: python gantt_chart.py