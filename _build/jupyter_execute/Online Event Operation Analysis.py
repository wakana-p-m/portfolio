#!/usr/bin/env python
# coding: utf-8

# # Online Event Optimization 🎟️
# 
# To improve the resource efficiency, performed A/B testins to make decisions on reducing frequency and changing schedules while maintaining the total number of attendees. I was able to reduce the frequency without reducing the total number of attendees, which resulted in saving over 40% of labor costs.
# 
# ---------------
# 
# ### Background
# Online events have been one of the most effective lead conversion campaigns, and my team have managed over 150 events (about 2 events per week) since the COVID-19 pandemic started and (March, 2020).  However, running events was extremely labor and resource intensive, and some events required overtime and working on weekends. My company runs one weekday event and 2 weekend events (morning and afternoon sessions).
# 
# 
# ### Objective
# Change the online event time, day of a week, and/or frequency to eliminate or reduce events conducted outside of the regular business hour and/or weekend operations without negatively affecting the performance.
# 
# 
# ### Measure of Success
# The success of the event campaigns are measured by the number of RSVPs, # of attendees, and  show rate (# of attendees / RSVP). 
# 
# 
# ### Method/Models
# Performed A/B test (paired T test) to evaluate if the change of event start times, weekend v.s. weekday, and 1 session vs. 2 sessions make a significant difference in the KPIs (the number of RSVPs, # of attendees, and showrate.)
# 
# 
# ### Data Source
# The raw data was exported from Salesforce using Salesforce Object Query Language (SOQL). Data associated with event objects and prospective student opportunities objects are imported and combined with the primary key, unique user ID. 
# 
# 
# ### Resutls
# - Hosting events on weekday did made a statistically significant improvement in show rate, however there is no significant difference in the RSVP count.
# - Hosting event on 11AM and 3PM did not make a significant difference in the number of RSVP and showarete.
# - There is no significant difference in the total number of attendees when hosting 1 session per day and 2 sessions par day. 
# 
# 
# ### Business Actions
# Continued to host online events on weekend because the test proved that having event on weekends generates more attendees. However, we decided to get rid of 3PM session because there was no significant difference in the show rate between 11AM and 3PM and the combined number of attendees from 11AM and 3PM sessions were not significantly different from the total number of attendees when hosting just 1 session par day. Having two options would be convenient for attendees but it ended up splitting attendees into two sessions. 
# 
# 
# ### Business Impact
# Getting rid of 3 PM session enabled the company to cut 40% of labor cost while maintaining the same number of attendees.
