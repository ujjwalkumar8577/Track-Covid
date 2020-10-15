import math
import os
import random
import re
import sys
import urllib.request, urllib.parse, urllib.error
import json
import string
from datetime import date
from matplotlib import pyplot as plt
import numpy as np

# Checks whether file1 is present or not
def file1IsPresent():
    try:
        now=str(date.today())
        fh=open('file1.txt')
        txt=fh.read()
        srch=re.search('([0-9]{4}\-[0-9]{2}\-[0-9]{2})',txt)
        time=srch.group(0)
        fh.close()

        if now==time:
            return True
        else:
            return False
    except:
        return False

# Checks whether file2 is present or not
def file2IsPresent():
    try:
        now=str(date.today())
        fh=open('file2.txt')
        txt=fh.read()
        srch=re.search('([0-9]{4}\-[0-9]{2}\-[0-9]{2})+',txt)
        time=srch.group(len(srch)-1)
        fh.close()

        if now==time:
            return True
        else:
            return False
    except:
        return False

# returns JSON object received from URL
def getjson(url):

    if url=='https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true':
        if file1IsPresent():
            fh=open('file1.txt')
            txt=fh.read()
            return json.loads(txt)
        else:
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            try:
                js = json.loads(data)
                file1 = open("file1.txt", "w")
                file1.writelines(data)
                file1.close()
            except:
                js = None
            return js
    else:
        if file2IsPresent():
            fh=open('file2.txt')
            txt=fh.read()
            return json.loads(txt)
        else:
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            try:
                js = json.loads(data)
                file2 = open("file2.txt", "w")
                file2.writelines(data)
                file2.close()
            except:
                js = None
            return js

# formats string by adding spaces
def pf(string,n):
    s=str(string)
    return s.ljust(n)

def fetchCases():
    js = getjson('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true')

    activeCases=js['activeCases']
    activeCasesNew=js['activeCasesNew']
    recovered=js['recovered']
    recoveredNew=js['recoveredNew']
    deaths=js['deaths']
    deathsNew=js['deathsNew']
    previousDayTests=js['previousDayTests']
    totalCases=js['totalCases']
    lastUpdated=js['lastUpdatedAtApify']

    print('Total activeCases     ','\t',activeCases)
    print('Total activeCasesNew  ','\t',activeCasesNew)
    print('Total recovered       ','\t',recovered)
    print('Total recoveredNew    ','\t',recoveredNew)
    print('Total deaths          ','\t',deaths)
    print('Total deathsNew       ','\t',deathsNew)
    print('Total previousDayTests','\t',previousDayTests)
    print('totalCases            ','\t',totalCases)
    print('lastUpdated           ','\t',lastUpdated)
    print()
    print()

def fetchRegion(region):
    js = getjson('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true')

    ind=-1
    for i in range(0,35):
        if js['regionData'][i]['region']==region:
            ind=i
            break

    if ind==-1:
        print('Region not found')
    else:
        region=js['regionData'][ind]['region']
        totalInfected=js['regionData'][ind]['totalInfected']
        newInfected=js['regionData'][ind]['newInfected']
        recovered=js['regionData'][ind]['recovered']
        newRecovered=js['regionData'][ind]['newRecovered']
        deceased=js['regionData'][ind]['deceased']
        newDeceased=js['regionData'][ind]['newDeceased']

        print('region       ','\t',region)
        print('totalInfected','\t',totalInfected)
        print('newInfected  ','\t',newInfected)
        print('recovered    ','\t',recovered)
        print('newRecovered ','\t',newRecovered)
        print('deceased     ','\t',deceased)
        print('newDeceased  ','\t',newDeceased)
    
    print()
    print()

def printTable():
    js = getjson('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true')

    print('- '*72)
    print('S.N.',pf('region',40),pf('totalInfected',16),pf('newInfected',16),pf('recovered',16),pf('newRecovered',16),pf('deceased',16),pf('newDeceased',16))
    print('- '*72)
    
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0

    for ind in range(0,35):
        
        sn=ind+1
        region=js['regionData'][ind]['region']
        totalInfected=js['regionData'][ind]['totalInfected']
        newInfected=js['regionData'][ind]['newInfected']
        recovered=js['regionData'][ind]['recovered']
        newRecovered=js['regionData'][ind]['newRecovered']
        deceased=js['regionData'][ind]['deceased']
        newDeceased=js['regionData'][ind]['newDeceased']
        print(pf(sn,4),pf(region,40),pf(totalInfected,16),pf(newInfected,16),pf(recovered,16),pf(newRecovered,16),pf(deceased,16),pf(newDeceased,16))

        s1=s1+int(totalInfected)
        s2=s2+int(newInfected)
        s3=s3+int(recovered)
        s4=s4+int(newRecovered)
        s5=s5+int(deceased)
        s6=s6+int(newDeceased)
        
    previousDayTests=js['previousDayTests']
    totalCases=js['totalCases']
    lastUpdated=js['lastUpdatedAtApify']

    print('- '*72)
    print(pf('',4),pf('',40),pf(s1,16),pf(s2,16),pf(s3,16),pf(s4,16),pf(s5,16),pf(s6,16))
    print('- '*72)
    print()
    print('lastUpdated     ','\t',lastUpdated)
    print()
    print()

def plotChart():
    js = getjson('https://api.apify.com/v2/datasets/58a4VXwBBF0HtxuQa/items?format=json&clean=1')
    print('Data Received')
    lst=list()
    print('Days : ',len(js))

    for ind in range(0,len(js)):
        if js[ind]['activeCases'] is not None:
            lst.append(int(js[ind]['activeCases']))

    courses = range(1,len(lst)+1)
    values = lst
    
    print('Plotting Chart...')

    fig = plt.figure(figsize = (1,100))
    plt.bar(courses, values, color ='maroon', width = 0.4)
    plt.xlabel("Day")
    plt.ylabel("Active Cases")
    plt.title("COVID 19 Active Cases")
    plt.show() 

if __name__ == '__main__':

    print()
    choice='1'
    while choice!='0':
        choice=input('Enter \n1 for All India \n2 for Particular State \n3 to print table \n4 to plot chart \n0 to Exit\n')

        if choice=='1':
            fetchCases()
        elif choice=='2':
            region=input('Enter Region\n')
            fetchRegion(region)
        elif choice=='3':
            printTable()
        elif choice=='4':
            plotChart()
        else:
            print('Exiting...')