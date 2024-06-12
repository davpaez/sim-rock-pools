# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:58:18 2018

@author: David Paez
"""

import datetime
import numpy as np
import pandas as pd
import re

def interpret_line(data_string, spans, day, year):
    
    parts = [data_string[start:end] for start, end in spans]
    
    list_datestring = list()
    list_value = list()
    list_quality = list()
    
    for month, item in enumerate(parts, 1):
        datestring = '{}-{}-{}'.format(year, month, day)
        
        try:
            date = datetime.datetime(year, month, day)
        except ValueError as e:
            #print(date, 'does not exist: ', e)
            pass
        else:
            parts_item = item.split()
            
            if len(parts_item) == 0:
                # The column is empty
                value = np.nan
                quality = np.nan
            elif len(parts_item) == 1: 
                if len(parts_item[0]) == 1: # The unique element is a single character
                    # The single character is the quality
                    value = np.nan
                    quality = parts_item[0]
                else: # The unique element is a string of characters
                    # The element is the value
                    value = float(parts_item[0])
                    quality = np.nan
            else:
                if len(parts_item[0]) == 1: # The first elem is a single character
                    # The single character is the quality, the other is the value
                    value = float(parts_item[1])
                    quality = parts_item[0]
                else: # The unique element is a string of characters
                    # The element is the value
                    value = float(parts_item[0])
                    quality = parts_item[1]
            
            list_datestring.append(date)
            list_value.append(value)
            list_quality.append(quality)
            
    return (list_datestring, list_value, list_quality)


def interpret_section(section, list_lines):
    
    list_datestring = list()
    list_value = list()
    list_quality = list()
    
    initial_pos = section + 12
    year_pos = section + 2
    months_pos= section + 9

    year_line = list_lines[year_pos]
    year = int(re.search('ANO\s+(\d{4})', year_line).group(1))
    
    months_line = list_lines[months_pos]
    
    # Find columns pattern
    matches = re.finditer(r'\w+\s+\*',months_line)
    spans = [match.span() for match in matches]    
    
    # Iterate over days (rows)
    for numline in range(31):
        data_string = list_lines[initial_pos+numline]
        day = numline+1
        dt, vl, ql = interpret_line(data_string, spans, day, year)
        list_datestring += dt
        list_value += vl
        list_quality += ql

    return (list_datestring, list_value, list_quality)


# Read data

def read_ideam(path, var_type):
    
    f = open(path)
    
    '''
    Strategy for reading:
        This is the structure of the data:
            1. Variable and Year
            2. Header of months
            3. Data for days
    
    The variables existing in the data are:
        VALORES TOTALES DIARIOS DE BRILLO SOLAR (Horas)
        
    
    '''
    
    list_type = list()
    list_registry = list()
    
    list_lines = f.readlines()
    
    for i, line in enumerate(list_lines):
        if 'NACIONAL AMBIENTAL' in line:
            variable = line.replace('NACIONAL AMBIENTAL','').strip()
            
            # Add to unique list of variable types
            if variable not in list_type:
                list_type.append(variable)
                list_registry.append(list())
            
            # Add to list registry
            idx = list_type.index(variable)
            list_registry[idx].append(i)
            
    # Print list of available variable types
#    print('Available variables from input data file:')
#    for i, var in enumerate(list_type): print(i,'\t', list_type[i])
    
    list_datestring = list()
    list_value = list()
    list_quality = list()
    
    for section in list_registry[var_type]:
        dt, vl, ql = interpret_section(section, list_lines)
        
        list_datestring += dt
        list_value += vl
        list_quality += ql
    
    f.close()
    
    # Create pandas dataframe
    d = {'date': list_datestring,
         'qty': list_quality,
         'value': list_value,}
    df = pd.DataFrame(d, columns=['date','value', 'qty'], index=list_datestring).sort_index()
    
    return df

def read_pools_data(path):
    
    df = pd.read_excel(path, sheet_name=None)
    
    if len(df) == 1:
        return list(df.items())[0][1] # Returns simple dataframe
    else:
        df_copy = df.copy()
        for i, key in enumerate(df):
            df_copy[i] = df_copy.pop(key)
        return df_copy # Returns ordered dict of dataframes


def to_excel(namefile, df):
    writer = pd.ExcelWriter(r'Output/'+namefile+'.xlsx')
    df.to_excel(writer)