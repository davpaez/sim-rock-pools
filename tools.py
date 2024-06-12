# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:38:24 2018

@author: David Paez
"""

from scipy import interpolate
import pandas as pd

def interp(df, known_var, unknown_var):
    '''
    Interpolate between two columns of a dataframe. One known and one target
    
    Arguments
        df: Dataframe
        known_var: key of dictionary associated with known variable
        unknown_var: key of dictionary associated with unknonwn variable
'''
    
    f = interpolate.interp1d(df[known_var], df[unknown_var])
    
    return f


def monthly_mean(df):
    #TODO Correct this function
    
    num_years = df.index.max().year - df.index.min().year
    
    rain_months = list()
    for i in range(1, 13):
        
        rain_months_in_yearj = list()
        for j in range(1997,2017):
            rain_months_in_yearj.append(df[(df.index.month==i) & (df.index.year==j)].value.sum())
        rain_month_allyears = sum(rain_months_in_yearj)/(2017-1997)
        rain_months.append(rain_month_allyears)
    
    return rain_months

def daily_stats(df, field):
    '''
    
    Args:
        df: DataFrame
    '''
    
    list_mean = []
    list_std = []
    list_max = []
    list_min = []
    
    # Days in a normal (non-leap) year
    days = list(pd.date_range('2015-01-01','2015-12-31').date)
    
    for i, day in enumerate(days):
        condition1 = (df.date.dt.day == day.day)&(df.date.dt.month == day.month) # Day of month
        daily_mean = df[condition1][field].mean()
        daily_std = df[condition1][field].std()
        daily_min = df[condition1][field].min()
        daily_max = df[condition1][field].max()
        
        list_mean.append(daily_mean)
        list_std.append(daily_std)
        list_min.append(daily_min)
        list_max.append(daily_max)
    
    df = pd.DataFrame({'average': list_mean, 'stdev': list_std, 'mi':list_min, 'ma': list_max}, index=days)
    
    return df

def length_consecutive_values(df):
    '''
    Returns a list whose elements are the length of consecutive True values
    '''
    pass
    