#!/usr/bin/env python
# coding: utf-8

# # An analysis of watch imports/exports of 2024

# In[1]:


import warnings
warnings.simplefilter('ignore', FutureWarning)

from pandas import *


# In[2]:


FILE = 'myProject_4Data.csv'


# In[3]:


data = read_csv(FILE, dtype={'cmdCode':str})


# In[4]:


def watchType(c):
    if c == '9101':
        return 'Fancy Metal'
    else:
        return 'Standard'

COMMODITY = 'Type of Watch'
data[COMMODITY] = data['cmdCode'].apply(watchType)
MONTH = 'refPeriodId'
PARTNER = 'partnerDesc'
FLOW = 'flowDesc'
VALUE = 'primaryValue'

HEADINGS = [MONTH, PARTNER, COMMODITY, FLOW, VALUE]
cleanData = data[HEADINGS]
cleanData


# In[9]:


countries = cleanData[cleanData['partnerDesc'] != 'World']
imports = countries.groupby('flowDesc').get_group('Import')
exports = countries.groupby('flowDesc').get_group('Export')


# # Total Trade Flows of Both Types of Watches

# In[12]:


totalTrade =  DataFrame([(imports[VALUE].sum(), exports[VALUE].sum(), exports[VALUE].sum()-imports[VALUE].sum() )],columns=['Total Imports','Total Exports','Balance'])
totalTrade


# # Main trade partners over the year

# In[15]:


mainImports = imports.groupby(PARTNER)[VALUE].aggregate(sum).sort_values(ascending = False).head(8)
mainImports


# In[25]:


mainImports.plot(kind='barh', grid=True, title='Main Exporters to the UK')


# In[19]:


mainExports = exports.groupby(PARTNER)[VALUE].aggregate(sum).sort_values(ascending = False).head(8)
mainExports


# In[27]:


mainExports.plot(kind='barh', grid=True, title='Main Importers from the UK')


# # Regular Fancy Watch Import Partners

# In[72]:


def regular(g):
    return (len(g) >= 8)

fancyImports = imports.groupby(COMMODITY).get_group('Fancy Metal')
regFancy = fancyImports.groupby(PARTNER).filter(regular)
regFancyFreq = regFancy.groupby(PARTNER)[PARTNER].aggregate(len)
regFancyFreq.sort_values(ascending=False, inplace=True)
regFancyFreq


# In[135]:


January = 20240101

JanuaryRegularFancyImports = DataFrame(regFancy.groupby(MONTH).get_group(January))
TopJanuaryRegularFancyImports = JanuaryRegularFancyImports.sort_values(VALUE, ascending=False).head()
TopJanuaryRegularFancyImports


# In[133]:


print('The above regular partners accounted for',(fancyImports[fancyImports[PARTNER].isin(TopJanuaryRegularFancyImports[PARTNER])][VALUE].sum()/fancyImports[VALUE].sum()).round(4)*100,'% of fancy watch imports over the year')


# # Bi-directional Partners

# In[137]:


pivot = pivot_table(countries, 
                    index=PARTNER,
                    columns=[FLOW,COMMODITY],
                    values=VALUE,
                    aggfunc=sum,
                   margins=True)
pivot.dropna()


# In[141]:


DataFrame(pivot.dropna().loc['Switzerland'])


# In[ ]:




