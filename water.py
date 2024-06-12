# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 19:36:05 2018

@author: David Paez
"""

import pandas as pd
from datetime import datetime

# Columns simulation data
sim_data_columns = ['date',
                    'runoff', 
                    'evap', 
                    'vol', 
                    'delta_vol', 
                    'outflow', 
                    'area', 
                    'depth', 
                    'depth_percent']

def simulate_pool(evap_df, prec_df, attr, list_dta, list_vtd, list_dtv,  id_pool, max_depth, start_date, end_date):
    
    dta = list_dta[id_pool]
    vtd = list_vtd[id_pool]
    dtv = list_dtv[id_pool]
    
    evap_df = evap_df[start_date:end_date]
    prec_df = prec_df[start_date:end_date]
    
    ws_area = attr.iloc[id_pool]['ws_area'] # Area watershed pool
    initial_depth_percent = attr.iloc[id_pool]['initial_depth']
    max_vol = float(dtv(max_depth))
    initial_depth = initial_depth_percent * max_depth
    
    
    # Lists
    list_runoff = list()
    list_evap = list()
    list_vol = list()
    list_delta_vol = list()
    list_outflow = list()
    list_area = list()
    list_depth = list()
    list_depth_percent = list()
    
    dates = pd.date_range(start_date, end_date)
    
    list_runoff.append(None)
    list_evap.append(None)
    list_vol.append(float(dtv(initial_depth)))
    list_delta_vol.append(None)
    list_outflow.append(None)
    list_area.append(dta(initial_depth))
    list_depth.append(initial_depth)
    list_depth_percent.append(initial_depth_percent)
    
    for i, date in enumerate(dates, 1):
        
        # Calculate delta value
        prec_day = prec_df.loc[date]['value']/1000 # Precipitation height in m
        evap_day = evap_df.loc[date]['value']/1000 # Evaporation height in m
        
        runoff = ws_area * prec_day
        area_previous_step = list_area[i-1]
        evap = area_previous_step*evap_day
        
        delta_vol_prelim = runoff - evap
        
        vol_previous_step = list_vol[i-1]
        vol_prelim = vol_previous_step + delta_vol_prelim
        if vol_prelim < 0:
            vol_prelim = 0
        
        if vol_prelim > max_vol:
            vol_real = max_vol
        else:
            vol_real = vol_prelim
        
        delta_vol_real = vol_real - list_vol[i-1]
        
        outflow = vol_prelim - vol_real
        
        depth = float(vtd(vol_real))
        
        area = float(dta(depth))
        
        depth_percent = depth/max_depth
        
        
        list_runoff.append(runoff)
        list_evap.append(evap)
        list_vol.append(vol_real)
        list_delta_vol.append(delta_vol_real)
        list_outflow.append(outflow)
        list_area.append(area)
        list_depth.append(depth)
        list_depth_percent.append(depth_percent)
    
    d = {'date': list(dates),
             'runoff': list_runoff[1:],
             'evap': list_evap[1:],
             'vol': list_vol[1:],
             'delta_vol': list_delta_vol[1:],
             'outflow': list_outflow[1:],
             'area': list_area[1:],
             'depth': list_depth[1:],
             'depth_percent': list_depth_percent[1:]}
    sim_data = pd.DataFrame(d)
    
    
    return sim_data
        