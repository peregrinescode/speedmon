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
sns.set_style('ticks')
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
        logf['Time'][i]= logf['Time'][i].replace(' CEST', '')
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
        logf['Upload'][i] = logf['Upload'][i].replace(' Mbi', '')  # catch lines of different length...
        logf['Upload'][i] = logf['Upload'][i].replace(' Mb', '')  # catch lines of different length...
        logf['Upload'][i] = float(logf['Upload'][i])
        
    # Remove the 'rest' column
    logf = logf.drop(columns='rest')
    #print(logf)
    
    return logf


def plot_hist(logP):
    '''Plot histgram from speedtest logfile.'''

    fig, ax = plt.subplots(3, 1)

    sns.histplot(logP['Ping'], kde=True, kde_kws=dict(cut=1), ax=ax[0])
    sns.histplot(logP['Download'], kde=True, kde_kws=dict(cut=1), ax=ax[1])
    sns.histplot(logP['Upload'], kde=True, kde_kws=dict(cut=1), ax=ax[2])

    ax[0].set_ylabel(r'Frequency')
    ax[1].set_ylabel(r'Frequency')
    ax[2].set_ylabel(r'Frequency')
    ax[0].set_xlabel(r'Ping time ($ms$)')
    ax[1].set_xlabel(r'Download speed ($Mbit/s$)')
    ax[2].set_xlabel(r'Upload speed ($Mbit/s$)')

    sns.despine(fig)
    fig.set_size_inches(8, (5 / 1.618) * 3)
    fig.subplots_adjust(hspace=0.4)
    fig.savefig('speed_histogram.png', pad_inches=0.1, bbox_inches='tight', dpi=120)

def plot_time(logP):
    '''Plot speed against time from speedtest logfile.'''

    fig, ax = plt.subplots(3, 1)

    
    # Group times in to hour bins
    for i, row in logP.iterrows():
        logP['Time'][i] = pd.to_datetime(logP['Time'][i]).strftime('%H')
        #logP['Time'][i] = pd.to_datetime(logP['Time'][i])
        
    # sort by time
    logP.sort_values('Time', inplace=True)    

    print(logP)
    
    sns.boxplot(data=logP,x='Time', y='Ping', ax=ax[0], palette="deep")
    sns.boxplot(data=logP,x='Time', y='Download', ax=ax[1], palette="deep")
    sns.boxplot(data=logP,x='Time', y='Upload', ax=ax[2], palette="deep")
    
    #sns.lineplot(data=logP, x='Time', y='Ping', errorbar='sd')
    #sns.scatterplot(data=logP, x='Time', y='Ping', hue='Ping', palette='flare', ax=ax[0])
    #sns.scatterplot(data=logP, x='Time', y='Download', hue='Download', palette='flare_r', ax=ax[1])
    #sns.scatterplot(data=logP, x='Time', y='Upload', hue='Upload', palette='flare_r', ax=ax[2])

    
    
    ax[0].set_ylabel(r'Ping time ($ms$)')
    ax[1].set_ylabel(r'Download speed ($Mbit/s$)')
    ax[2].set_ylabel(r'Upload speed ($Mbit/s$)')
    ax[2].set_xlabel(r'Time (hh:mm)')
    #ax[0].set_ylim(-10,400)
    #ax[1].set_ylim(-0.5,15)
    #ax[2].set_ylim(-0.1,3)
    
    ax[0].axes.xaxis.set_visible(False)
    ax[1].axes.xaxis.set_visible(False)
    
    #ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #for label in ax[2].get_xticklabels():
        #label.set_rotation(45)
        #label.set_ha('right')
        
    #for a in ax:
        #a.get_legend().remove()

    sns.despine(fig)
    fig.set_size_inches(10, (5 / 1.618) * 3)
    fig.subplots_adjust(hspace=0.25)
    fig.savefig('speed_v_time.png', pad_inches=0.1, bbox_inches='tight', dpi=120)

if __name__ == "__main__":
    logf = read_speedLog('speedtest.log')
    plot_hist(logf)
    plot_time(logf)

