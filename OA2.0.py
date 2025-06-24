#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 16:06:57 2024

@author: diller
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os as os

slopeStrs = ['Liposome','NADH','CCCP','PierA']

#requestions number of trials and names from user 
#outputs the list of names of the excel sheet names form the user
def importData(): 
    dfList = []
    
    dataDir = str(input('\nWhat is the name of the data directory: '))
    cDir = os.getcwd()
    dataDir = cDir+'/'+dataDir
    os.chdir(dataDir)
    trialList = os.listdir(dataDir)
    os.chdir(dataDir)
    for i in trialList:
        if i != '.DS_Store':
            dfList.append(pd.read_excel(i))
    os.chdir(cDir)
    return dfList


def sectionData(df_it, n, sectionTimes):
      
    chemicalSlices = []
    
    for i in range(0,len(sectionTimes)):
        if i != (len(sectionTimes)-1):
            chemicalSlice = df_it.query('time >= @sectionTimes[@i] and time < @sectionTimes[@i+1]')
            chemicalSlices.append(chemicalSlice)
        else:
            chemicalSlice = df_it.query('time >= @sectionTimes[@i]')
            chemicalSlices.append(chemicalSlice)   
        
    return chemicalSlices

def plotLine(chemicalSlice, slopeName, n):
    res = stats.linregress(chemicalSlice['time'],chemicalSlice['Oxygen 1'])
    linefit = [i*res.slope + res.intercept for i in chemicalSlice['time']]
    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter(chemicalSlice['time'],chemicalSlice['Oxygen 1'],color='tab:brown',s=15,label='Data')
    ax.plot(chemicalSlice['time'],linefit,color='purple',linewidth=2.0,label='Trendline',linestyle='--')
    
    ax.tick_params(labelsize=15)
    ax.set_xlabel('Time(s)',fontsize=20)#plot settings
    ax.set_ylabel('Oxygen Concentration '+r'$\frac{nmol O_2}{mL}$',fontsize=20)
    xpos = chemicalSlice['time'].iloc[0] + 5
    ypos = chemicalSlice['Oxygen 1'].iloc[0] 
    ax.text(xpos, ypos, r'y = {:1.3f}x - {:3.1f} $r^2$= {:1.3f}'.format(res.slope,res.intercept,res.rvalue**2),fontsize=18)
    ax.set_title('Trial '+str(n + 1)+' '+slopeName,fontsize=20)
    ax.grid()
    ax.legend()
    plt.show()
    
def saveLine(chemicalSlice, slopeName, n):
    cwd = os.getcwd()
    newPath = cwd+'/Figures/Slopes'
    os.chdir(newPath)
    res = stats.linregress(chemicalSlice['time'],chemicalSlice['Oxygen 1'])
    linefit = [i*res.slope + res.intercept for i in chemicalSlice['time']]
    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter(chemicalSlice['time'],chemicalSlice['Oxygen 1'],color='tab:brown',s=15,label='Data')
    ax.plot(chemicalSlice['time'],linefit,color='purple',linewidth=2.0,label='Trendline',linestyle='--')
    
    ax.tick_params(labelsize=15)
    ax.set_xlabel('Time(s)',fontsize=20)#plot settings
    ax.set_ylabel('Oxygen Concentration '+r'$\frac{nmol O_2}{mL}$',fontsize=20)
    xpos = chemicalSlice['time'].iloc[0] + 5
    ypos = chemicalSlice['Oxygen 1'].iloc[0] 
    ax.text(xpos, ypos, r'y = {:1.3f}x - {:3.1f} $r^2$= {:1.3f}'.format(res.slope,res.intercept,res.rvalue**2),fontsize=18)
    ax.set_title('Trial '+str(n + 1)+' '+slopeName,fontsize=20)
    ax.grid()
    ax.legend()
    fig.savefig('T'+str(n + 1)+'_'+slopeName,dpi=600)
    plt.show()
    os.chdir(cwd)

def trimSlice(chemicalSlice, slopeName, n, slopeList):
    userBool = False
    
    while userBool == False:
        plotLine(chemicalSlice, slopeName, n)
        numLeft = int(input('How many points would you like to cut from left of '+'Trial '+str(n + 1)+' '+slopeName+': '))
        numRight = int(input('How many points would you like to cut from right of '+'Trial '+str(n + 1)+' '+slopeName+': '))
        if (numLeft + numRight) == 0:
            print('No change requested\n')
            userBool = True
            res1 = stats.linregress(chemicalSlice['time'],chemicalSlice['Oxygen 1'])
            slopeList.append(res1.slope)
            saveLine(chemicalSlice, slopeName, n)
            continue
        else:
            numFirstIndex = chemicalSlice.index[0] + numLeft
            numLastIndex = chemicalSlice.index[-1] - numRight
            chemicalSlice = chemicalSlice.query('index >= @numFirstIndex & index <= @numLastIndex')
            continue

    return slopeList
           
def barPlot(dfSlopes):
    
    colorlist = ['royalblue','darkorange','silver','gold','lightcoral']
    AvgSlopes = []
    standarderrors = []
    stdSlopes = []
    
    cwd = os.getcwd()
    newPath = cwd+'/Figures'
    os.chdir(newPath)
    
    for i in slopeStrs:
        rowSlice = dfSlopes.loc[i]
        AvgSlopes.append(abs(rowSlice.mean()))
        standarderrors.append(rowSlice.std()/len(dfSlopes.columns))
        stdSlopes.append(rowSlice.std())
    
    dfSlopes['Avg'] = AvgSlopes
    dfSlopes['std'] = stdSlopes
    dfSlopes['SE'] = standarderrors
    plt.figure(figsize=(10,10))
    plt.bar(slopeStrs,AvgSlopes, color=colorlist)
    plt.xticks(fontsize=18,fontname='Arial')
    plt.yticks(fontsize=18,fontname='Arial')
    plt.ylabel(r' Rate of $O_2$ Concentration Decay  $\frac{O_2 nmol}{mL\times s}$',fontsize=28,fontname='Arial')
    plt.title("Oxygen Depletion Rates",fontsize=30,fontname='Arial')
    plt.errorbar(slopeStrs,AvgSlopes,yerr=standarderrors,fmt='none',color='black',ecolor='black',capsize=4)
    plt.savefig('RespirationRatesBarChart.png',dpi=600)
    plt.show()
    
    os.chdir(cwd)
    return dfSlopes
    
def makeDirs():
    cwd = os.getcwd()
    figurePath = cwd+'/Figures'
    totalPath = cwd+'/Figures/Total'
    slopePath = cwd+'/Figures/Slopes'
    
    pathList = [figurePath, totalPath, slopePath]
    for i in pathList:
        os.mkdir(i)
        
def plotTotalOxygraph(dfList, sectionTimes):
    cwd = os.getcwd()
    newPath = cwd+'/Figures/Total'
    os.chdir(newPath)
    k = 1
    for i, df_it in enumerate(dfList):
        df_it = df_it.query('time >= 0')
        fig, ax = plt.subplots(figsize=(8,8))
        ax.plot(df_it['time'], df_it['Oxygen 1'],color='fuchsia')
        ax.set_xlabel('Time(s)',fontsize=20)
        ax.set_ylabel('Oxygen Concentration '+r'$\frac{nmol O_2}{mL}$',fontsize=20)
        ax.set_title('Entire SBP Respiration Trial '+str(k),fontsize=20)
        ax.grid()
        itTimes = sectionTimes[i]
        for i in range(0,len(itTimes)):
            xpos = itTimes[i]
            ypos = df_it.query('time == @xpos')['Oxygen 1'].values[0] - 1.15
            if slopeStrs[i]!= 'Piericidin A':
                ax.text(xpos, ypos, slopeStrs[i]+"→", rotation=90)
            else:
                ax.text(xpos, ypos,"PA→", rotation=90)
        
        fig.savefig('TotalOxygraph'+'_T'+str(k)+'.png',dpi=600)
        plt.show()
        k+=1
    os.chdir(cwd)
    
def fixTime(dfList):
    k = 0
    sectionTimes = []
    for df_it in dfList:
        df_temp = df_it[df_it['Label'].isin(slopeStrs)]
        timeStart = df_temp['Time'].iloc[0] - 10
        df_it['time'] = df_it['Time'] - timeStart
        df_temp = df_it[df_it['Label'].isin(slopeStrs)]
        df_it = df_it.query('time >= 0')
        sectionTimes.append(df_temp.time.tolist())
        dfList[k] = df_it
        k+=1
    return dfList, sectionTimes
                

def main():
    trialStrs = []
    print('\nHello welcome to the Oxygraph Scipt for the Letts Lab! \n\nPlease ensure you are in the correct directory and that you print file names verbose.')
    dfList = importData()
    
    makeDirs()
    dfList, sectionTimes = fixTime(dfList)
    for i in dfList:
        print(i.head())
    plotTotalOxygraph(dfList, sectionTimes)
    for i in range(1,len(dfList)+1):
        trialStrs.append(i)
        
    dfSlopes = pd.DataFrame(0,index=slopeStrs,columns=trialStrs)

    for i in range(0,len(dfList)):
        sliceList = sectionData(dfList[i], i,sectionTimes[i])
        slopeList = []
        for k in range(0,len(slopeStrs)):
            slopeList = trimSlice(sliceList[k],slopeStrs[k], i, slopeList)
        dfSlopes[i+1] = slopeList
       
    dfSlopes = barPlot(dfSlopes)
    dfSlopes.to_excel('slopes.xlsx')
    
    print('Thank you for using the Letts Lab Oxygraph Analysis script!\nSee file outputs in current working directory')
    
    
if __name__ == "__main__":
    main()
