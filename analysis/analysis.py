# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 08:36:43 2024

@author: Marcel Bruckmann
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime
import calendar
import shutil
import json
from datetime import timedelta

os.chdir("C:\\Users\\Marcel Bruckmann\\Downloads\\analysis\\")
"""data = pd.read_excel("DEV-Matchplan-Games-2024-02-10.xlsx")
data2 = data[["gameid", "league", "season", "played_at", "hometeam", "awayteam", "hthg", "htag", "fthg", "ftag"]]


datas1 = data2[data2["season"].isin(["2015-2016"])]
datas2 = data2[data2["season"].isin(["2016-2017"])]
datas3 = data2[data2["season"].isin(["2017-2018"])]

col = ["hthg", "htag", "fthg", "ftag"]
for c in col:
    datas3[c] = datas3[c].astype(str)

datas3["first_result"] = datas3.hthg + "-" + datas3.htag
datas3["second_result"] = datas3.fthg + "-" + datas3.ftag

datas3 = datas3[["gameid", "league", "season", "played_at", "hometeam", "awayteam", "first_result", "second_result"]]

datas3 = datas3.to_dict('records')

with open("datas3.json", "w") as outfile: 
    json.dump(datas3, outfile)"""


f = open("datas1.json",)
season1 = json.load(f)
f.close()
f = open("datas2.json",)
season2 = json.load(f)
f.close()
f = open("datas3.json",)
season3 = json.load(f)
f.close()


# Load data from dictionary
season1 = pd.DataFrame.from_dict(season1)
season2 = pd.DataFrame.from_dict(season2)
season3 = pd.DataFrame.from_dict(season3)

# What types? With datetime
season3.dtypes

### SCREENSHOT Screenshot_001

# What columns?
season1.columns

### SCREENSHOT Screenshot_002


# Head and Tail
season1.head()
### SCREENSHOT Screenshot_003

season1.tail()
### SCREENSHOT Screenshot_004


# How to convert object to datetime?
season1.dtypes
### SCREENSHOT Screenshot_005

season1["played_at"] = season1["played_at"].astype("datetime64[ns]") 
season1.dtypes
### SCREENSHOT Screenshot_006

#Optional: season1.played_at = season1.played_at.astype("datetime64[ns]") 
season2.played_at = season2.played_at.astype("datetime64[ns]") 
season3.played_at = season3.played_at.astype("datetime64[ns]") 

# Unique hometeams?
season1.hometeam.unique()
### SCREENSHOT Screenshot_007

# Sorting? You need numpy
arr1 = np.sort(season1.hometeam.unique())
### SCREENSHOT Screenshot_008

arr2 = season1.hometeam.sort_values().unique()

# Compare both arrays
(arr1==arr2).all()
### SCREENSHOT Screenshot_009

# Check with errors if I change one element
arr1[1] = "Dortmund"
arr1
### SCREENSHOT Screenshot_010

(arr1==arr2).all()
### SCREENSHOT Screenshot_011


# Merging dataframes
df_games = pd.DataFrame()

df_games = pd.concat([df_games,season1])
df_games = pd.concat([df_games,season2])
df_games = pd.concat([df_games,season3])

# info
df_games.info()
### SCREENSHOT Screenshot_012

# Rsults should be in seperate columns
df_games.head(9)
### SCREENSHOT Screenshot_013

df_games["hthg"], df_games["htag1"] = zip(*df_games["first_result"].str.split("-").tolist())
df_games["fthg1"], df_games["ftag"] = zip(*df_games["second_result"].str.split("-").tolist())

df_games.head(9)
### SCREENSHOT Screenshot_014


# Check columns
df_games.columns
### SCREENSHOT Screenshot_015

# Check Index
df_games.index
### SCREENSHOT Screenshot_016

# Unique Indexes? WHy 1447? and not 3 times more?
len(df_games.index.unique())
### SCREENSHOT Screenshot_017

# Reset Index
df_games.reset_index(drop=True, inplace=True)
df_games.index
### SCREENSHOT Screenshot_018

# We can also use another range for index
i = list(range(50, len(df_games)+50))
s = pd.Series(i)
df_games = df_games.set_index(s)
df_games.index

### SCREENSHOT Screenshot_019

# Indexes CHECK
len(df_games.index.unique())

### SCREENSHOT Screenshot_020

# Rename columns
df_games.rename(columns={"htag1": "htag", "fthg1": "fthg"}, inplace=True)


# Other columns I can drop
#OPTIONAL: df_games1 = df_games[['gameid', 'league', 'season', 'played_at', 'hometeam', 'awayteam', 'hthg', 'htag', 'fthg', 'ftag']]
#OPTIONAL: del df_games['first_result'], df_games['second_result']
df_games.drop(['first_result', 'second_result'], axis=1, inplace=True)
df_games.columns
### SCREENSHOT Screenshot_022

# Get unique leagues
unique_leagues = df_games.league.unique()
### SCREENSHOT Screenshot_023

# English is wrong how we change it?
df_games['league'] = df_games["league"].apply(lambda x : x.replace("English", "England"))
### SCREENSHOT Screenshot_024


# Check duplicates - There is one duplicated row
df_games.duplicated().sum()

# What are the duplicates?
df_games[df_games.duplicated(keep=False)]
### SCREENSHOT Screenshot_025


df_games = df_games.drop_duplicates()
# optional drop_duplicates(subset=['season'])

# duplicates check
df_games.duplicated().sum()
### SCREENSHOT Screenshot_026


# Get unique leagues CHECK
unique_leagues = df_games.league.unique()


# We want to replace values England = E1, Germany = G1 ...
# Create a dictionary
dict_league = dict(zip(unique_leagues, ["E1", "G1", "S1", "I1"]))
### SCREENSHOT Screenshot_027


# Replace based on dictionary
df_games.replace(dict_league, inplace=True)

# OPTIONAL WITH MAP
# df_games.league = df_games.league.map(dict_league) # No inplace function

# Unique CHECK
df_games.league.unique()
# Optional: list(dict.fromkeys(df_games.league.values))
### SCREENSHOT Screenshot_028


# How many games per League? Why 918 for Germany? Because they have less games per season
df_games.league.value_counts()
### SCREENSHOT Screenshot_029

# get unique results as an array
col = ["hthg", "htag", "fthg", "ftag"]
[[c, df_games[c].unique()] for c in col]
### SCREENSHOT Screenshot_030

# check of '' for both columns 0, 6, 7
df_games_array = df_games.values
[x[0] for x in df_games.values if x[6] == '' or x[7] == '']
### SCREENSHOT Screenshot_031
df_games[df_games["gameid"] == 'ZMSFK']
### SCREENSHOT Screenshot_032


# For this game we know the result hthg: 0, htag = 1
df_games["hthg"].loc[df_games["gameid"] == 'ZMSFK'] = '0'
df_games["htag"].loc[df_games["gameid"] == 'ZMSFK'] = '1'

df_games[df_games["gameid"] == "ZMSFK"]


# Convert to integer
df_games.info()

df_games["hthg"], df_games["htag"] = df_games["hthg"].astype(int), df_games["htag"].astype(int)
df_games["fthg"], df_games["ftag"] = df_games["fthg"].astype(int), df_games["ftag"].astype(int)
df_games.info()

### SCREENSHOT Screenshot_034


# Date types
df_games.played_at = df_games.played_at.astype("datetime64[ns]") 

df_games["year"] = df_games.played_at.dt.year
df_games["month"] = df_games.played_at.dt.month
df_games["day"] = df_games.played_at.dt.day
df_games["hour"] = df_games.played_at.dt.hour
df_games["date"] = df_games.played_at.dt.date
df_games["time"] = df_games.played_at.dt.time

df_games[["played_at", "year", "month", "day", "hour", "date", "time"]].head(10)
### SCREENSHOT Screenshot_035

# Date is a string (object) and we can convert it to datetime (with 0 numbers for time)
df_games.dtypes
### SCREENSHOT Screenshot_036

df_games["date_dt"] = pd.to_datetime(df_games["date"])
df_games.dtypes
### SCREENSHOT Screenshot_037


currentDatetime = datetime.now()
### SCREENSHOT Screenshot_038

df_games["day_since"] = currentDatetime - df_games["played_at"]
### SCREENSHOT Screenshot_039

df_games["day_since_added_days"] = df_games["day_since"] + timedelta(days=10)
df_games[["day_since", "day_since_added_days"]].head(10)
### SCREENSHOT Screenshot_040

df_games["played_at_reduced_days"] = df_games["played_at"] + timedelta(days=-5)
df_games[["played_at", "played_at_reduced_days"]].head(10)
### SCREENSHOT Screenshot_041


# Get games with only 2 and 4 goals
df1 = df_games[df_games.fthg.isin([2, 4])]
df1.iloc[:,6:10]
### SCREENSHOT Screenshot_041


# Get all other games without 2 and 4 goals
df2 = df_games[~df_games.fthg.isin([2, 4])]
df2.iloc[:,6:10]

# Team goals all (total goals)
df_games["ft_total"] = df_games.fthg + df_games.ftag
df_games[["fthg", "ftag", "ft_total"]].head(10)
### SCREENSHOT Screenshot_042


# Assign nan value
# Create a copy
df_games_copy = df_games
df_games_copy["fthg"].loc[df_games_copy["hometeam"] == 'Stoke City'] = np.nan
np.array((df_games_copy[df_games_copy["hometeam"] == 'Stoke City']['fthg']))
### SCREENSHOT Screenshot_043

    
# check nans
df_games_copy.isna().sum()
### SCREENSHOT Screenshot_044

# another nans
df_games_copy["hthg"].loc[df_games_copy["hometeam"] == 'Hertha BSC'] = np.nan
df_games_copy.isna().sum()
### SCREENSHOT Screenshot_045

# Filter nans
notNull = df_games_copy[(df_games_copy["hthg"].notnull()) & (df_games_copy["fthg"].notnull())]
### SCREENSHOT Screenshot_046

isNull = df_games_copy[(df_games_copy["hthg"].isnull()) | (df_games_copy["fthg"].isnull())]
### SCREENSHOT Screenshot_047

# Drop nan only one column
len(df_games_copy.dropna(subset = ["hthg"])) # optional inplace=True
### SCREENSHOT Screenshot_048

# Drop nan whole dataset
len(df_games_copy.dropna()) # optional inplace=True
### SCREENSHOT Screenshot_049

df_games_copy["fthg"].loc[df_games_copy["hometeam"] == 'Stoke City'] = \
    df_games_copy.ft_total - df_games_copy.hthg - df_games_copy.htag - df_games_copy.htag
df_games_copy.isna().sum()
### SCREENSHOT Screenshot_050


# leagues unique
# There is one league wrong


# reset index
df_games = df_games.reset_index(drop=True)

# Shift values 
df3 = df_games[(df_games['hometeam'] == "Manchester United") & (df_games['season'] == "2017-2018")].sort_values(["played_at"], ascending=True)
### SCREENSHOT Screenshot_051


# Sorting in lists
df3_list =  sorted(df3.values.tolist(), key=lambda x: x[3], reverse=False)
### SCREENSHOT Screenshot_052
df3_list[0]
### SCREENSHOT Screenshot_053

# Check season
### SCREENSHOT Screenshot_054

df_games.season.unique()

# Replace value
df_array = [x.replace("20155-2016", "2015-2016") for x in df_games.season.tolist()]
df_games["season"] = df_array

### SCREENSHOT Screenshot_054
df_games.season.unique()


# String Upper and lower
df_games.columns = [x.upper() for x in df_games.columns]
df_games.columns
### SCREENSHOT Screenshot_056

df_games.columns = [x.lower() for x in df_games.columns]
df_games.columns
### SCREENSHOT Screenshot_057


##################### END OF PART 1




# Rollig mean for one team
df3['avg_roll'] = df3['hthg'].expanding(5).mean()

# Shifted mean
df3["roll_shift_before"] = df3.avg_roll.shift(-1, axis = 0)
df3["roll_shift_next"] = df3.avg_roll.shift(1, axis = 0)  

# Games per season and league
df_5 = pd.pivot_table(df_games, values=["gameid"], index=["season", "league"], aggfunc={"gameid": "count"}).reset_index(drop=False).sort_values(["league", "season"])
df_6 = df_5.set_index(['season','league'])['gameid'].unstack().add_suffix('_games').reset_index()
df_6 = df_6.fillna(0)



# OPTIONAL FILLNA 
# df_5.set_index(['season','league'])['gameid'].unstack().add_suffix('_games').reset_index().fillna(0)

# Fillna seperately
df_6 = df_5.set_index(['season','league'])['gameid'].unstack().add_suffix('_games').reset_index()
df_6.fillna({'G1_games': 1, 'I1_games': 2, 'S1_games': 3}) #Optional ,inplace=True



# Games per season and league CHECK
df_5 = pd.pivot_table(df_games, values=["gameid"], index=["season", "league"], aggfunc={"gameid": "count"}).reset_index(drop=False).sort_values(["league", "season"])

# Row categories to columns
df_5.set_index(['season','league'])['gameid'].unstack().add_suffix('_games').reset_index()

# DROP NA SUBET
df_5 = pd.pivot_table(df_games, values=["gameid"], index=["season", "league"], aggfunc={"gameid": "count"}).reset_index(drop=False).sort_values(["league", "season"])




# ROLLING AVERAGE ON GROUPS
df1 = (df_games.groupby(['season'])
         .agg({'fthg':'mean'})
         .groupby(level=0, group_keys=False)
         .rolling(2)
         .mean())


# SHIFT VALUES


# Rollng mean for group of teams / leagues
leagues = ["E1", "G1"]
seasons = ["2015-2016", "2016-2017"]
teams = ["Newcastle United", "Manchester United", "Borussia Dortmund", "Bayern München"]


df4 = df_games[df_games["league"].isin(leagues) & df_games["season"].isin(seasons) & df_games["hometeam"].isin(teams)].sort_values("played_at")
df4 = df4.set_index(['league', 'season','hometeam'])



df4["roll_avg"] = df4.groupby(index)['fthg'].rolling(3).mean().droplevel(0).reset_index(drop=True)

df4_bvb = df4[(df4["hometeam"] == "Borussia Dortmund") & (df4["season"] == "2015-2016")]

df1 = (df_games.groupby(['season','hometeam'])
         .agg({'fthg':'mean'})
         .groupby(level=0, group_keys=False)
         .rolling(2)
         .mean())

# grouping
df3 = df3.groupby(['hometeam'])['hthg'].agg('mean')





df2 = df_games.groupby(['hometeam', 'awayteam'])['ft_total'].agg('mean')
df2 = df_games.groupby(['hometeam', 'awayteam'])['ft_total'].agg('sum')
df2 = df_games.groupby(['hometeam', 'awayteam'])['ft_total'].agg('max')

df2 = df_games.groupby(['hometeam', 'awayteam'])['ft_total'].agg('max')

# USing pivot_table
df3 = pd.pivot_table(df_games, values=["ft_total"], index=["hometeam", "awayteam"], aggfunc={"ft_total": np.mean, "ft_total": [min, max, "count"]})

df3.columns = [x + y for x,y in df3.columns]

    