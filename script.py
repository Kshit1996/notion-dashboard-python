#!/usr/bin/env python
# coding: utf-8

# In[42]:


from notion.client import NotionClient
import datetime
client=NotionClient(token_v2="5eb906f0541e05cd563299dba7162e1b1aa9906d24daec7249a115201e8d103c6cf312e5d3db1cb513020a658a3015d43a26280183c9bae2dd3055dbc45d2ed19ac2fc081e172921326170973439")


# In[43]:


page = client.get_block("https://www.notion.so/greyamp/ae5eda0288324145834e92218849bcd8?v=83bd4754f4fb483994059ccfd41773a8")

def date_format(date):
    if(date != None):
        if type(date) is datetime.datetime:
            return date.date()
        else:
            return date.start
    return None


# In[44]:


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
            "Due Date":date_format(row.due_date),
            "End Date":date_format(row.end_date),
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
    
print(planningBoard)


# In[45]:


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


# In[46]:


import chart_studio
username = 'kshit96'
api_key = 'koxCWL68bdDw2hy6r1mH'

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

fig = px.pie(df, values='Count', names='Status')
fig.update_traces(textposition='inside', textinfo='value+label')
fig.show()

import chart_studio.plotly as py
py.plot(fig, filename = 'card_statuses', auto_open=True)


# In[21]:





# In[ ]:




