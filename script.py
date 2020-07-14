#!/usr/bin/env python
# coding: utf-8

# In[2]:


from notion.client import NotionClient
import datetime
import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.express as px

username = 'kshit96'
api_key = 'koxCWL68bdDw2hy6r1mH'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

client=NotionClient(token_v2="5eb906f0541e05cd563299dba7162e1b1aa9906d24daec7249a115201e8d103c6cf312e5d3db1cb513020a658a3015d43a26280183c9bae2dd3055dbc45d2ed19ac2fc081e172921326170973439")
page = client.get_block("https://www.notion.so/greyamp/ae5eda0288324145834e92218849bcd8?v=83bd4754f4fb483994059ccfd41773a8")


# In[3]:


def date_format(date):
    if(date != None):
        if type(date) is datetime.datetime:
            return date.date()
        else:
            return date.start
    return None

def are_all_not_none(*args):
    for arg in args:
        if(arg == None):
            return False
    return True

def create_pie_chart(dataframe, filename, textinfo, title):
    fig = px.pie(dataframe, values='Count', names='Status', title=title)
    fig.update_traces(textposition='inside', textinfo='value+label',textfont_size=20)
    fig.show()

    py.plot(fig, filename = filename, auto_open=False)

def convert_to_dataframe_for_pi_chart(data):
    return pd.DataFrame(list(data.items()),columns = ['Status','Count'])


def card_completion_graph(cards,filename, title):

    cardCompletionData= {
        "Overdue": 0,
        "On Time":0,
        "Early": 0,
        "NA": 0
    }
    for card in cards:
        startDate = card['Start Date']
        endDate = card['End Date']
        dueDate = card['Due Date']
        if are_all_not_none(startDate,endDate,dueDate):
            if(endDate == dueDate):
                cardCompletionData["On Time"] = cardCompletionData["On Time"] +1 
            elif(endDate < dueDate):
                cardCompletionData["Early"] =  cardCompletionData["Early"] +1 
            elif(endDate > dueDate):
                cardCompletionData["Overdue"] =  cardCompletionData["Overdue"] +1 
        else:
            cardCompletionData["NA"] =  cardCompletionData["NA"] +1      
        

    df = convert_to_dataframe_for_pi_chart(cardCompletionData)

    create_pie_chart(df,filename, 'percent+label', title)
    
def card_incomplete_graph(cards,filename, title):

    cardCompletionData= {
        "Overdue": 0,
        "Due": 0,
        "NA": 0
    }
    for card in cards:
        startDate = card['Start Date']
        endDate = datetime.date.today()
        dueDate = card['Due Date']
        if are_all_not_none(startDate,dueDate): 
            if(endDate < dueDate):
                cardCompletionData["Due"] =  cardCompletionData["Due"] +1 
            elif(endDate > dueDate):
                cardCompletionData["Overdue"] =  cardCompletionData["Overdue"] +1 
        else:
            cardCompletionData["NA"] =  cardCompletionData["NA"] +1      
        

    df = convert_to_dataframe_for_pi_chart(cardCompletionData)

    create_pie_chart(df,filename, 'percent+label', title)


# In[4]:


planningBoard = []
for row in page.collection.get_rows():
    
    assignees = []
    for user in row.assignee:
        assignees.append(user.full_name)
        
    supportingMembers = []
    for user in row.supporting_members:
        supportingMembers.append(user.full_name)
        
    card = {"Name":row.name,
            "Assignee":assignees,
            "CM Stage":row.cm_stage,
            "Completed In Sprint":row.completed_in_sprint,
            "Created Date":row.created_date,
            "Current Sprint":row.current_sprint,
            "DoD":row.dod,
            "Due Date":date_format(row.planned_end_date),
            "End Date":date_format(row.actual_end_date),
            "Last Edited Date":date_format(row.last_edited_date),
            "Lever":row.lever,
            "Priority":row.priority,
            "Sprint Planned For":row.sprint_planned_for,
            "Start Date":date_format(row.start_date),
            "Status":row.status,
            "Supporting Members":supportingMembers,
            "Track":row.track
           } 
    planningBoard.append(card)


# In[5]:


cardStatusData= {}
for card in planningBoard:
    if card["Status"] in cardStatusData:
        cardStatusData[card["Status"]] = cardStatusData[card["Status"]] + 1
    else:
        cardStatusData[card["Status"]] = 1
        
df = convert_to_dataframe_for_pi_chart(cardStatusData)
create_pie_chart(df,'card-statuses', 'value+label', 'Overall Card Statuses')


# In[6]:


completed=[]
onHold=[]
inProgress=[]
waitingForClient=[]
inReview=[]

for card in planningBoard:
    status = card["Status"]

    if status == "Completed":
        completed.append(card)
    elif status == "On Hold":
        onHold.append(card)        
    elif status == "In Progress":
        inProgress.append(card)
    elif status == "Waiting For Client":
        waitingForClient.append(card)
    elif status == "In Review":
        inReview.append(card)
        
card_incomplete_graph(inProgress,'inProgress-card-completion','Time-Duration: In Progress Cards')
card_completion_graph(completed,'completed-card-completion','Time-Duration: Completed Cards')
card_incomplete_graph(onHold,'onHold-card-completion','Time-Duration: On Hold Cards')
card_incomplete_graph(waitingForClient,'waitingForClient-card-completion', 'Time-Duration: Waiting For Client Cards')
card_incomplete_graph(inReview,'inReview-card-completion', 'Time-Duration: In Review Cards')


# In[ ]:


import git
import shutil
import os
import io
import json
from git import Git

def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()

repo_url = 'git@github.com:Kshit1996/notion-database.git'
repo_dir = 'test'
work_file_name = 'CardHistory.json'
work_file = os.path.join(repo_dir, work_file_name)
if os.path.isdir(repo_dir):
    shutil.rmtree(repo_dir)
repo = git.Repo.clone_from(repo_url, repo_dir)

repo.git.pull()
new_file_path = os.path.join(repo.working_tree_dir, work_file_name)
   
json_object = json.dumps(planningBoard, default=default)  
print(json_object)

with io.open(new_file_path, 'w', encoding='utf-8') as f:
    f.write(json_object)
    f.close()
repo.index.add(new_file_path)
repo.index.commit(str(datetime.datetime.now()))

repo.git.push()
shutil.rmtree(repo_dir)


# In[ ]:




