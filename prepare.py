# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:13:37 2018

@author: David Paez
"""

import pandas as pd


def crop_to_common(list_dfs):
    '''
    Crop the dataframes date-indexed by keeping only a common date range
    '''
    pass

def put_nulls(df_orig):
    '''
    Creates a dataframe with a daily continuous date index so that missing values are
    visible and represented with null values
    TODO Finish and implement this function to handle general datasets
    '''
    
    start_date = df_orig.date.min()
    end_date = df_orig.date.max()
    
    date_range = pd.date_range(start_date, end_date)
    columns = list(df_orig.columns)
    
    df = pd.DataFrame(index=date_range, columns=columns)
    
    df.loc[date_range] = df_orig


def fill_data(df_orig):
    '''
    Fill data with daily average
    '''
    df = df_orig.copy()
    
    delta = (df.date.max() - df.date.min()).days
    
    if delta < 2*365 - 1: # If there are less than a normal year and a leap year
        raise ValueError('Fill is not possible.\n\
                         There is only '+str(delta)+' days in the dataframe date rangedays.\n\
                         729 (2*365-1) days or more is necessary so filling has higher chance of working.')
        
    
    # Get dates of leap year. 2016 is a leap year
    days = list(pd.date_range('2016-01-01','2016-12-31').date)
    for day in days:
        condition1 = (df.date.dt.day == day.day)&(df.date.dt.month == day.month) # Day of month
        condition2 = (df.date.dt.day == day.day)&(df.date.dt.month == day.month)&(df.value.isnull())
        daily_mean = df[condition1].value.mean()
        df.loc[condition2.values,'value'] = daily_mean
        df.loc[condition2.values,'qty'] = 'filled'
        
    return df
