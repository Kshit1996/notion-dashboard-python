#!/usr/bin/env python
# coding: utf-8

# In[1]:


from notion.client import NotionClient
client=NotionClient(token_v2="5eb906f0541e05cd563299dba7162e1b1aa9906d24daec7249a115201e8d103c6cf312e5d3db1cb513020a658a3015d43a26280183c9bae2dd3055dbc45d2ed19ac2fc081e172921326170973439")


# In[2]:


page = client.get_block("https://www.notion.so/greyamp/ae5eda0288324145834e92218849bcd8?v=83bd4754f4fb483994059ccfd41773a8")


# In[3]:


planningBoard = []
for row in page.collection.get_rows():
    
    assignees = []
    for user in row.assignee:
        assignees.append(user.full_name)
        
    if(row.due_date != None):
        dueDate = row.due_date.start
    else:
        dueDate = None
    if(row.end_date != None):
        endDate = row.end_date.start
    else:
        endDate = None
    if(row.start_date != None):
        startDate = row.start_date.start
    else:
        startDate = None
        
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
            "Due Date":dueDate,
            "End Date":endDate,
            "Last Edited Date":row.last_edited_date,
            "Lever":row.lever,
            "Priority":row.priority,
            "Sprint Planned For":row.sprint_planned_for,
            "Start Date":startDate,
            "Status":row.status,
            "Supporting Members":supportingMembers,
            "Track":row.track
           } 
    planningBoard.append(card)
    
    
print(planningBoard)


# In[4]:


import pandas as pd
import plotly.express as px
cardStatusData= {}
for card in planningBoard:
    if card["Status"] in cardStatusData:
        cardStatusData[card["Status"]] = cardStatusData[card["Status"]] + 1
    else:
        cardStatusData[card["Status"]] = 1
        
print(cardStatusData)
df = pd.DataFrame(list(cardStatusData.items()),columns = ['Status','Count'])
print(df)


# In[5]:


import chart_studio
username = 'kshit96'
api_key = 'koxCWL68bdDw2hy6r1mH'

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

fig = px.pie(df, values='Count', names='Status')
fig.update_traces(textposition='inside', textinfo='value+label')
fig.show()

import chart_studio.plotly as py
py.plot(fig, filename = 'card_statuses', auto_open=True)


# In[ ]:




