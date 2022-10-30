from bs4 import BeautifulSoup
import xmltodict
from collections import namedtuple

# PARSES XML to get the complete list of meetings that have documents to scrape

# Opens manually scraped xml with all meetings
with open(r"C:\Users\Cole Schnell\Desktop\Summer\Learn\project-2\meetings.xml", "r") as f:
     data_dict = xmltodict.parse(f.read())

datatable = data_dict['DataTable']

meetings = datatable['diffgr:diffgram']['NewDataSet']['Table']

# Creates named tuple to hold meeting information
meeting_info = namedtuple("meeting_info", ['date', 'type', 'id'])

meetings_with_minutes = []

for meeting in meetings:
     if meeting['CanPrintMinutes'] == "1":
          container = meeting_info(meeting['MM_DateTime'], meeting['MM_MeetingTitle'], meeting['Master_MeetingID'])
          meetings_with_minutes.append(container)

#print(meetings_with_minutes[0].id)

# Test
for meeting in meetings:
    if meeting['Master_MeetingID'] == "10214":
        print(meeting)