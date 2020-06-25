# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:04:55 2020

@author: chengjw
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import numpy as np
from datetime import date, timedelta

#%% Create AWS client with credentials provided, access DynamoDB tables

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id= '',
    aws_secret_access_key= '',
    region_name = 'ap-southeast-1'
    )

tableE = dynamodb.Table('environment')

#%% Query table, load into dataframe

today = date.today() + timedelta(days=1)
last  = today - timedelta(days=10)

start = last.strftime("%Y-%m-%d") + 'T00:00:00'
end = today.strftime("%Y-%m-%d") + 'T00:00:00'

response = tableE.query(
    KeyConditionExpression=Key('location').eq('greenwall') & Key('timestamp').between(start, end)
    #KeyConditionExpression=Key('location').eq('greenwall') 
)

items = response['Items']
data = pd.DataFrame(items)

#%% Change datatypes, set timestamp as index, count number of days

data = data.astype({'timestamp': 'datetime64','humidity': 'float64','temp': 'float64' })

#date_rng = pd.date_range(start='3/21/2018', end='3/24/2018', freq='H')

data.set_index('timestamp', inplace = True)
data.drop('location',axis = 1, inplace = True)

#data = data['2020-03-24T00:00:00':'2020-04-04T00:00:00']

dates = list(np.unique(data.index.date).astype(str))


#%% Plot ridgeline

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import seaborn as sns

env_data = 'temp'

def ax_settings(ax, var_name):
    ax.patch.set_facecolor('none') #Set background transparent
    
    #Set number of ticks
    #ax.yaxis.set_major_locator(plt.MaxNLocator(2))
    
    #Remove axes
               
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    #See only bottom axis
    
    ax.spines['bottom'].set_edgecolor('#444444')
    ax.spines['bottom'].set_linewidth(2)
    
    ax.grid(b = None)
    
    #Set labels for each ridgeline
    
    ax.text(0.01, 0.07, var_name, fontsize=14, fontweight="bold", transform = ax.transAxes) 
    return None

#Create figure object
    
fig = plt.figure(figsize=(18,8))

fig.suptitle("TEMPERATURE", fontsize = 16, fontweight = 'bold', x = 0.18, y = 0.9, color = '#444444')

#Setup grid to arrange individual ridgeline plots in a stack

gs = gridspec.GridSpec(nrows=len(dates), #Number of figures = number of unique dates
                       ncols=1, 
                       figure=fig, 
                       wspace=0.1, 
                       hspace=-0.4 #Top overlap for each figure
                      )

#Generate Seaborn palette in hex values, number of colors = number of unique dates

#palette = sns.cubehelix_palette(len(dates), start=.5, rot=-.75).as_hex()
palette = sns.color_palette("BrBG_r", len(dates)).as_hex()

#Generate axes objects

ax = [None]*(len(dates) + 1)

for i in range(len(dates)):
    
    #Add a ridgeline plot to the grid
    ax[i] = fig.add_subplot(gs[i, 0])
    
    ax_settings(ax[i], str(dates[i]))   
    
    #Change Python datetime64 to Matplotlib datetime format
    x_data = mdates.date2num(data[dates[i]].index)
    
    ax[i].set_xlim(np.floor(min(x_data)), np.ceil(max(x_data)))
    
    #Plot each ridgeline
    sns.lineplot(x = x_data, 
                 y=data[dates[i]][env_data], 
                 color='#FFFFFF')
    
    #Fill under ridgeline
    l1 = ax[i].lines[0]
    ymin, ymax = ax[i].get_ylim()
    x1 = l1.get_xydata()[:,0]
    y1 = l1.get_xydata()[:,1]
    ax[i].fill_between(x1, ymin, y1, color=palette[i], alpha=0.9)
    
    #Draw line at mean
    y_mean = np.round(data[dates[i]][env_data].mean(),decimals=1)
    ax[i].axhline(y = y_mean, color = palette[i], alpha = 0.3)
  
    #Set x-axis ticks to 24-hour mode
    if i == (len(dates)-1):
        locator = mdates.HourLocator(interval = 1)
        formatter = mdates.DateFormatter('%H')
        ax[i].xaxis.set_major_locator(locator)
        ax[i].xaxis.set_major_formatter(formatter)
        ax[i].tick_params(axis="x", labelsize=14)
        ax[i].set_xlabel('Hour', fontsize = 14)
                    
    #Set y-axis ticks and labels
    ax[i].set_yticks([y_mean])
    ax[i].tick_params(axis="y", colors = palette[i], labelsize=14, right = True, labelright = True)
    ax[i].set_ylabel('')
    
    #Remove x-axis ticks for upper ridgeline plots
    if i < (len(dates)-1): 
        ax[i].set_xticks([])
        ax[i].set_xlabel('')
        

plt.show()

