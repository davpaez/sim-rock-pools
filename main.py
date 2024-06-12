# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:46:50 2018

@author: David Paez
"""


# coding: utf-8

#%%  Importing modules
import simrockpools as srp

def run_example():
    #%% Setting up paths
    
    path_climate =   r'C:\Users\ANGELA\Google Drive\Drones en la biología\Paper GTO\Calculos\SimRockPools\Input\data_climate.txt'
    path_pool_attr = r'C:\Users\ANGELA\Google Drive\Drones en la biología\Paper GTO\Calculos\SimRockPools\Input\attr_pools.xlsx'
    path_pool_dav  = r'C:\Users\ANGELA\Google Drive\Drones en la biología\Paper GTO\Calculos\SimRockPools\Input\dav_pools.xlsx'
    path_outputdir = r'C:\Users\ANGELA\Google Drive\Drones en la biología\Paper GTO\Calculos\SimRockPools\Output'
    
    
    #%% Create site object
    
    site = srp.Site(path_climate, path_pool_attr, path_pool_dav, path_outputdir)
    
    
    #%%  Reading data and importing it into the sim object
    
    site.read_data()
    
    #%% Setting up simulation parameters
    
    # Simulation date range
    start_date = '2000-01-01'
    end_date = '2017-12-31'
    site.set_simrange(start_date, end_date)
    
    #%% Filling data with daily mean for each day of the month
    
    site.fill_data()
    
    #%% Run simulation for pool
    
    site.run_pools()
    
    #%% Return object
    
    return site