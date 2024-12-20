# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:14:52 2024

@author: m.hawi
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'understanding the data'
df = pd.read_csv("911.csv")
df.head()
df.info()
df.describe()
df.columns
type(df['timeStamp'].iloc[0])

"cleaning the data"
df.duplicated().sum()
df.shape[0]
print(df.shape[0])
 

"""dropping the column e since it does not provide any useful info"""
df.drop('e', axis=1, inplace=True)
 
"""change the timestamp column datatype from str to date and time"""
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df.head
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Hour'].head()

df['DayOfWeek'] = df['timeStamp'].apply(lambda time: time.dayofweek)
df['DayOfWeek'].head()

df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Month'].head()

df['Year'] = df['timeStamp'].apply(lambda time: time.year)
df['Year'].head()

df['Date'] = df['timeStamp'].apply(lambda time:time.date())
df['Date'].head()

"""Day of Week is an integer 0-6 so i will use the map() method
 to map the actual string names to the day of the week:"""
 
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

df['DayOfWeek'] = df['DayOfWeek'].map(dmap)
df['DayOfWeek'].head()
df.head(5)



"""" desc field contains three information
 Address, Township and Station code seperated by semi-column."""
 
df['station_code'] = df['desc'].str.split('Station', expand=True)[1].str.split(';', expand=True)[0]

df['station_code'] = df['station_code'].str.replace(':', '')
df['station_code'].head()

# Extract Emergency Categories from 'title'

df['reason_category'] = df['title'].apply(lambda title: title.split(':')[0])
df['reason_category'].head()

df['reason'] = df['title'].apply(lambda title: title.split(':')[1])
df['reason'].head()

df.head(5)


#Handling Missing Values
df.isna().sum()

# Fill missing addresses with a 'Unknown Address'

df['addr'].fillna('Unknown Address', inplace=True)
print(df['addr'].isna().sum()) 


# Drop rows with missing 'zip' or 'twp' values

df_cleaned = df.dropna(subset=['zip', 'twp'])

# Drop rows with missing 'station_code'

df_cleaned = df_cleaned.dropna(subset=['station_code'])

print(df_cleaned.isna().sum())  


print(df_cleaned.info())
 

#EDA

#Top 5 townships (twp) for 911 calls

df['twp'].value_counts().head(10)

"""what kind of emergency calls was comming from LOWER MERION since it has the 
highest demand"""


df[df['twp']=='LOWER MERION']['reason'].value_counts().head(10)


"""what was the most called station for emergency"""

dfsc = df['station_code'].value_counts().head(10)
dfsc

df[df['station_code'] == "308A"]['reason_category'].value_counts()

df[df['station_code'] == "308A"]['reason'].value_counts().head(10)

# most called station bar plot
plt.figure(figsize=(12,6))
plt.bar(dfsc.index,dfsc.values,width=0.6)
plt.title("Most Called Stations")
plt.xlabel("Station")
plt.ylabel("Number of calls")
plt.tight_layout()

"""The most called stations are 308A, 329, 313"""

#Top 10 reasons for emergency calls


dfRes = df['reason'].value_counts().head(10)
dfRes
#unique values in reason column
df['reason'].nunique()

plt.figure(figsize=(12, 6))
x = list(dfRes.index)
y = list(dfRes.values)
x.reverse()
y.reverse()

plt.title("Most emergency reasons of calls")
plt.ylabel("Reason")
plt.xlabel("Number of calls")

plt.barh(x,y)
plt.tight_layout()
plt.show()
"""The results shows that the most emergency reasons of calls
 was due vehicle accidents"""
 
#Most common Reason for a 911 call

df['reason_category'].value_counts().head(5)


plt.figure(figsize=(12,6))
sns.countplot(x=df['reason_category'],data=df, palette='bright')
plt.title("Emergency call category")

"""the most common calls for 911 reason is EMS and Trafic """
