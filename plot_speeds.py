#!/usr/bin/env python3
# coding:utf-8
"""
	Author:   ross.warren<at>pm<dot>me
	Purpose:  Plot speed test log in histogram.
	Created: 09/04/20
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_style('darkgrid')
import datetime

def read_speedLog(log_in):
    """read speed log file to dataframe."""
    # Read in log file, fixed width format :(
    logf = pd.read_fwf(log_in, colspecs=[(0, 31), (31, 91)], header=None, names=['Time', 'rest'])

    # Create some new columns
    logf.insert(1, "Ping", logf['rest'].str.split('"', expand=False)[0][1])
    logf.insert(2, "Download", logf['rest'].str.split('"', expand=False)[0][3])
    logf.insert(3, "Upload", logf['rest'].str.split('"', expand=False)[0][5])
    
    # drop all lines which record 'error'
    logf.drop(logf[logf['rest'] == 'error'].index, inplace=True)

    # Separate columns 'rest' by the speech marks
    logf['rest'].str.split('"', expand=False)

    # Convert Time column to python datetime object
    for i, row in logf.iterrows():
        logf['Time'][i] = logf['Time'][i].replace('[', '')
        logf['Time'][i]= logf['Time'][i].replace(']', '')
        logf['Time'][i]= logf['Time'][i].replace(' BST', '')
        logf['Time'][i]= logf['Time'][i].replace(' GMT', '')
        logf['Time'][i]= datetime.datetime.strptime(logf['Time'][i], '%a %d %b %H:%M:%S %Y')

        # Sort out ping column
        logf['Ping'][i] = logf['rest'].str.split('"', expand=False)[i][1]
        logf['Ping'][i] = logf['Ping'][i].replace(' ms', '')
        logf['Ping'][i] = float(logf['Ping'][i])

        # Sort out Download column
        logf['Download'][i] = logf['rest'].str.split('"', expand=False)[i][3]
        logf['Download'][i] = logf['Download'][i].replace(' Mbit/s', '')
        logf['Download'][i] = float(logf['Download'][i])
        
        # Sort out Upload column
        logf['Upload'][i] = logf['rest'].str.split('"', expand=False)[i][5]
        logf['Upload'][i] = logf['Upload'][i].replace(' Mbit/s', '')
        logf['Upload'][i] = logf['Upload'][i].replace(' Mbit/', '')  # catch lines of different length...
        logf['Upload'][i] = logf['Upload'][i].replace(' Mbit', '')  # catch lines of different length...
        logf['Upload'][i] = float(logf['Upload'][i])
        
    # Remove the 'rest' column
    logf = logf.drop(columns='rest')
    
    return logf


def plot_hist(logP):
    '''Plot histgram from speedtest logfile.'''

    fig, ax = plt.subplots(3, 1)

    sns.distplot(logP['Ping'], kde=False, hist_kws={"range": [0,1000]}, ax=ax[0])
    sns.distplot(logP['Download'], kde=False, hist_kws={"range": [0,20]}, ax=ax[1])
    sns.distplot(logP['Upload'], kde=False, hist_kws={"range": [0,5]}, ax=ax[2])

    ax[0].set_ylabel(r'Frequency')
    ax[1].set_ylabel(r'Frequency')
    ax[2].set_ylabel(r'Frequency')
    ax[0].set_xlabel(r'Ping ($ms$)')
    ax[1].set_xlabel(r'Download ($Mbit/s$)')
    ax[2].set_xlabel(r'Upload ($Mbit/s$)')

    fig.set_size_inches(4, (4 / 1.618) * 3)
    fig.subplots_adjust(hspace=0.4)
    fig.savefig('speed_histogram.png', pad_inches=0.1, bbox_inches='tight', dpi=300)

def plot_time(logP):
    '''Plot speed against time from speedtest logfile.'''

    fig, ax = plt.subplots(3, 1)

    # Conver datetime to just hours:mins.
    for i, row in logP.iterrows():
        # logP['Time'][i] = pd.to_datetime(logP['Time'][i]).strftime('%H:%M')
        logP['Time'][i] = pd.to_datetime(logP['Time'][i]).strftime('%H')
        # logP['Time'][i] = mdates.date2num(logP['Time'][i])
        #hour = logP['Time'][i].hour
        #mins = logP['Time'][i].minute
        #y = datetime.time(hour, mins)
        #x.append(y)
    #logP.insert(4, "Hours", x)

    x = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']
    ping_time = pd.DataFrame(columns=x)
    up_time = pd.DataFrame(columns=x)
    down_time = pd.DataFrame(columns=x)
    for i in x:
        ping_time[i] = logP.where(logP['Time'] == i)['Ping']
        down_time[i] = logP.where(logP['Time'] == i)['Download']
        up_time[i] = logP.where(logP['Time'] == i)['Upload']
    
    sns.boxplot(data = ping_time, ax=ax[0])
    sns.boxplot(data = down_time, ax=ax[1])
    sns.boxplot(data = up_time, ax=ax[2])

    # xformatter = mdates.DateFormatter('%H')
    # ax[0].xaxis.set_major_formatter(xformatter)
    
    ax[0].set_ylabel(r'Time ($ms$)')
    ax[1].set_ylabel(r'Download speed ($Mbit/s$)')
    ax[2].set_ylabel(r'Upload speed ($Mbit/s$)')
    ax[0].set_xlabel(r'Hour of day')
    ax[1].set_xlabel(r'Hour of day')
    ax[2].set_xlabel(r'Hour of day')
    ax[0].set_ylim(-10,400)
    ax[1].set_ylim(-0.5,15)
    ax[2].set_ylim(-0.1,3)

    fig.set_size_inches(4, (4 / 1.618) * 3)
    fig.subplots_adjust(hspace=0.4)
    fig.savefig('speed_v_time.png', pad_inches=0.1, bbox_inches='tight', dpi=300)

if __name__ == "__main__":
    logf = read_speedLog('speedtest.log')
    # plot_hist(logf)
    plot_time(logf)

