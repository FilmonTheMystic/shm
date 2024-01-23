# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:34:25 2023

@author: Filmon Teweldemedhin Gebremichael
"""

import streamlit as st
import numpy as np
import pandas as pd
import glob
import warnings

warnings.filterwarnings('ignore')

files = glob.glob('data/*.txt')

li = []

for f in files:
    temp_df = pd.read_csv(f, delimiter= "\t", skiprows= 1)
    li.append(temp_df)
    print(f'Successfully created dataframe for {f} with shape {temp_df.shape}')

df = pd.concat(li, axis=0, ignore_index=True)
print(df.shape)
st.header("Raw data")
df

#Data from Channel 0 only
ch0_df = df.iloc[:, :12]

#Clean rows with NaN values
cleaned_df = ch0_df.dropna(axis=0, how='any')

#Concatenate UTC Date and UTC Time 
cleaned_df['Sample'] = pd.to_datetime(cleaned_df['UTC Date'] + ' ' + cleaned_df['UTC Time'])
cleaned_df.rename(columns={'Sample':'UTC DateTime'}, inplace=True)

#Drop redundant columns now that UTC DateTime is created
cleaned_df_v2 = cleaned_df.drop('UTC Date', axis=1)
cleaned_df_v2 = cleaned_df_v2.drop('UTC Time', axis=1)
st.header("Cleaned Data")
cleaned_df_v2

#Plotting the wide dataframe
st.header("Strain VS Time")
st.scatter_chart(
    cleaned_df_v2,
    x = 'UTC DateTime',
    y = cleaned_df_v2.columns[2:],
    height = 440
)
st.header("Temperature VS Time")
st.scatter_chart(
    cleaned_df_v2,
    x = 'UTC DateTime',
    y = cleaned_df_v2.columns[1],
    height = 440
)

#Dataframe info
cleaned_df_v2.info()
