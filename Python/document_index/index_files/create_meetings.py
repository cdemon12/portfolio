from bs4 import BeautifulSoup
import xmltodict
from collections import namedtuple

with open(r"C:\Users\Cole Schnell\Desktop\Summer\Learn\project-2\CPS_doc_scrapper\GetMeetingListing.xml", "r") as f:
     data_dict = xmltodict.parse(f.read())

datatable = data_dict['DataTable']

meetings = datatable['diffgr:diffgram']['NewDataSet']['Table']

meeting_info = namedtuple("meeting_info", ['date', 'type', 'id', 'url'])

meetings_with_minutes = []

for meeting in meetings:
     if meeting['CanPrintMinutes'] == "1":
          url =f"https://assistive.eboardsolutions.com/SB_Meetings/ViewMeeting.aspx?S=42&MID={meeting['Master_MeetingID']}"
          container = meeting_info(meeting['MM_DateTime'], meeting['MM_MeetingTitle'], meeting['Master_MeetingID'], url)
          meetings_with_minutes.append(container)

