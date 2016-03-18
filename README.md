# sandglass
Project tracking tool that integrates with Jira data to estimate project length.

I. File List
-------------------------
* sandglass.py - Executable file that asks for new/updated project information and returns timeline-based metrics
* projects.txt - Project list in json format based on user inputs when running sandglass.py
* README - You're looking at it!

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
* Project in this context are epic-based
* Incomplete projects assume consistent resources (time and human)
* Business day calculations do not bear in mind holidays, just weekends
* I use "project" and "epic" interchangeably, even though *technically* they are quite different in Jira (I mean "epic" in both cases)

IV. TL;DR (Installation)
-------------------------
Download Jira: sudo pip install jira --upgrade --ignore-installed six
Run the program: python sandglass.py
