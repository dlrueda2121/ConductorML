import pandas as pd
from math import log

#Contains 81 features extracted from 21263 superconductors along with the critical temperature in the 82nd column
train = pd.read_csv('./../../Project/superconduct/train.csv')

#Contains the chemical formula broken up for all the 21263 superconductors from the train.csv file.
#The last two columns have the critical temperature and chemical formula.
formula = pd.read_csv('./../../Project/superconduct/unique_m.csv')

#Assumes numeric value is first in each column entry
#Returns the series with only the numeric value, and converted to numeric series
def getNumeric(input_series):
    new_series = input_series.str.split(n=1)
    for i in range(0,len(input_series)):
        new_series[i] = new_series[i][0]
    return pd.to_numeric(new_series)

wolfram_data = pd.read_csv('./../../Project/superconduct/wolfram_element_data.csv')
fie_data = pd.read_csv('./../../Project/superconduct/fie.csv')

wolfram_data['atomic_mass'] = getNumeric(wolfram_data['atomic_mass'])
wolfram_data['atomic_radius'] = getNumeric(wolfram_data['atomic_radius'])
wolfram_data['Density'] = getNumeric(wolfram_data['Density'])
wolfram_data['ElectronAffinity'] = getNumeric(wolfram_data['ElectronAffinity'])
wolfram_data['FusionHeat'] = getNumeric(wolfram_data['FusionHeat'])
wolfram_data['ThermalConductivity'] = getNumeric(wolfram_data['ThermalConductivity'])
# wolfram_data.head()

element_data = wolfram_data
element_data.insert(3, "fie", fie_data,True)
element_data = element_data.set_index('Abbreviation')
element_data = element_data.drop(['Atomic_Number'],axis=1)
element_data['ElectronAffinity'] += 1.5
# print(element_data.head())

#!Parsing!
#Check if input string is valid
def checkValid(value):
    for i in range(0,len(value)):
        if(not ((value[i].isupper()) or (value[i].islower()) or (value[i].isdigit()) or (value[i] == '.'))):
            return -1

#Adds missing ones after abbreviations
#HO2 -> H1O2
def addOnes(input_string):
    tempString = ""
    for i in range(0,len(input_string)):
        tempString += input_string[i]
        if(input_string[i].isupper() or input_string[i].islower()):
            if(i+1 == len(input_string) or input_string[i+1].isupper()):
                tempString += '1'
    return tempString

#Adds spaces after tokens
#H2O1 -> H 2 O 1
def addSpaces(input_string):
    tempString = ""
    
    for i in range(0,len(input_string)-1):
        tempString += input_string[i]
        if(input_string[i].isupper() or input_string[i].islower()):
            if(input_string[i+1].isdigit()):
                tempString += ' '
        elif(input_string[i].isdigit()):
            if(input_string[i+1].isupper()):
                tempString += ' '
    tempString += input_string[len(input_string)-1]
    return tempString

#Parse string into two lists
#List of abbreviations and list of numbers
def parseInput(input_string):
    checkValid(input_string)
    parsedString = addOnes(input_string)
    parsedString = addSpaces(parsedString)
    parsedList = parsedString.split(' ')
    
    abbreviations = []
    numbers = []
    for i in range(0,len(parsedList)):
        if(i%2 == 0):
            abbreviations.append(parsedList[i])
        else:
            numbers.append(float(parsedList[i]))
    
    return abbreviations, numbers


##Functions for creating a sample from our parsed element data

##Ratios of each element 
#H2O -> H - 0.66 O - 0.33
def getRatios(input_list):
    total = sum(input_list)
    ratios = []
    for i in range(0,len(input_list)):
        ratios.append(input_list[i]/total)

    return ratios

def getValues(input_list,new_dataframe,colname):
    newlist = []
    for i in range(0,len(input_list)):
        newlist.append(element_data.loc[new_dataframe['Abb'][i]][colname])
    return newlist

def getW(input_list):
    total = sum(input_list)
    wlist = []
    for i in range(0,len(input_list)):
        wlist.append(input_list[i]/total)
    return wlist
        
def getInt(p,w):
    total = 0
    intList = []
    for i in range(0,len(p)):
        total += p[i]*w[i]
    for i in range(0,len(p)):
        intList.append((p[i]*w[i])/total)
    return intList
    
def mean(input_list,n):
    total = sum(input_list)/n

    return total
    
def weightedMean(input_list,p):
    total = 0
    for i in range(0,len(input_list)):
        total += input_list[i]*p[i]
    
    return total
    
def geometricMean(input_list,n):
    total = 1
    for i in range(0,len(input_list)):
        total = total*input_list[i]
    total = pow(total,1/n)

    return total
    
def weightedGeometricMean(input_list,p):
    total = 1
    for i in range(0,len(input_list)):
        total = total*pow(input_list[i],p[i])
    
    return total
    
def entropy(wList):
    total = 0
    for i in range(0,len(wList)):
        # print(wList[i])
        total -= (wList[i]*log(wList[i]+0.000001))
    
    return total
    
def weightedEntropy(input_list):
    total = 0
    for i in range(0,len(input_list)):
        total = total - (input_list[i]*log(input_list[i]+0.000001))
        
    return total
    
def getRange(input_list):
    maximum = max(input_list)
    minimum = min(input_list)
    
    return maximum - minimum
    
def getWeightedRange(input_list,p):
    tempList = []
    for i in range(0,len(input_list)):
        tempList.append(p[i]*input_list[i])
    maximum = max(tempList)
    #max_index = input_list.index(maximum)
    minimum = min(tempList)
    #min_index = input_list.index(minimum)
    
    return maximum - minimum
    
def stdDev(input_list,mean,n):
    total = 0
    for i in range(0,len(input_list)):
        total += pow((input_list[i]-mean),2)
    total = (1/n)*total
    total = pow(total,0.5)
    
    return total
    
def weightedStdDev(input_list,p,wtdMean):
    total = 0
    for i in range(0,len(input_list)):
        total += p[i]*pow((input_list[i]-wtdMean),2)
    total = pow(total,0.5)
    
    return total

#Pass in return from parseInput
def makeSample(data):
    new_dataframe = pd.DataFrame(data)
    new_dataframe = new_dataframe.T
    new_dataframe.columns = ['Abb','Num']
    ratios = getRatios(new_dataframe['Num'])
    numValues = new_dataframe.shape[0]
    
    sampleList = []
    sampleList.append(numValues)
    
    #len(element_data.columns)
    for i in range(0,len(element_data.columns)):
        valueList = getValues(new_dataframe['Abb'],new_dataframe,element_data.columns[i])
        wList = getW(valueList)
        intList = getInt(ratios,wList)
        
        mu = mean(valueList,numValues)
        v = weightedMean(valueList,ratios)
        
        sampleList.append(mu)
        sampleList.append(v)
        sampleList.append(geometricMean(valueList,numValues))
        sampleList.append(weightedGeometricMean(valueList,ratios))
        sampleList.append(entropy(wList))
        sampleList.append(weightedEntropy(intList))
        sampleList.append(getRange(valueList))
        sampleList.append(getWeightedRange(valueList,ratios))
        sampleList.append(stdDev(valueList,mu,numValues))
        sampleList.append(weightedStdDev(valueList,ratios,v))
        
    # print(sampleList)
        
    return sampleList

#Test it out
#Should work properly
# value = "H20"
# parsed = parseInput(value)
# Listy = makeSample(parsed)