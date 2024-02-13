# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:34:25 2023

@author: Filmon Teweldemedhin Gebremichael
"""
# IMPORT LIBRARIES

import streamlit as st
import numpy as np
import pandas as pd
import glob
import warnings

# Page Configuration
st.set_page_config(
    page_title= "UJ Photonics Lab Dashboard",
    page_icon= "📊",
    layout= "wide"
)

warnings.filterwarnings('ignore')

files = glob.glob('data/*.txt')

# Create an empty list to contain every data in the files
li = []

for f in files:
    temp_df = pd.read_csv(f, delimiter= "\t", skiprows= 1)
    li.append(temp_df)
    print(f'Successfully created dataframe for {f} with shape {temp_df.shape}')

# Concatenate all data from every file into this single data frame
df = pd.concat(li, axis=0, ignore_index=True)
#print(df.shape)
#st.header("Raw data")
#df

# Data from Channel 0 only
ch0_df = df.iloc[:, :12]

# Clean rows with NaN values
cleaned_df = ch0_df.dropna(axis=0, how='any')

# Concatenate UTC Date and UTC Time 
cleaned_df['Sample'] = pd.to_datetime(cleaned_df['UTC Date'] + ' ' + cleaned_df['UTC Time'])


cleaned_df.rename(columns={'Sample':'UTC DateTime'}, inplace=True)

# Drop redundant columns now that UTC DateTime is created
cleaned_df_v2 = cleaned_df.drop('UTC Date', axis=1)
cleaned_df_v2 = cleaned_df_v2.drop('UTC Time', axis=1)
st.header("Cleaned Data")
cleaned_df_v2

# Plotting the wide dataframe
st.header("Strain VS Time")
st.scatter_chart(
    cleaned_df_v2,
    x = 'UTC DateTime',
    y = cleaned_df_v2.columns[2:],
    height = 440
)

#Descriptive Statistics | average strain and temperature
temperature_average = cleaned_df_v2[1].mean
st.metric(label="Average Temperature", value=temperature_average)

#Dataframe info
cleaned_df_v2.info()
