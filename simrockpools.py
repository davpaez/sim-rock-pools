# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 07:58:44 2018

@author: David Paez
"""

from datetime import datetime

import iodata
import tools
import water
import prepare
import plots

class Site():
    
    def __init__(self, path_climate, path_pool_attr, path_pool_dav, path_outputdir):
        '''
        
        '''
        
        # Setting up paths
        self.path_climate = path_climate
        self.path_pool_attr = path_pool_attr
        self.path_pool_dav = path_pool_dav
        self.path_outputdir = path_outputdir
        
        # Dataframes input data
        self.evap_orig = None
        self.prec_orig = None
        self.evap = None
        self.prec = None
        self.attr = None
        self.dav  = None
        
        # Functions
        self.list_dta = [] # Depth to Area
        self.list_vtd = [] # Volume to Depth
        self.list_dtv = [] # Depth to Volume
        
        # Simulation parameters
        self.start_date = None
        self.end_date = None
        
        # Dataframes output data
        self.list_poolsim = [] # List of output of simulation of pools
        
    
    
    def read_data(self):
        
        # Create pandas dataframes
        self.evap_orig = iodata.read_ideam(self.path_climate, 1) # Evaporation
        self.prec_orig = iodata.read_ideam(self.path_climate, 3) # Precipitation
        self.evap = self.evap_orig.copy()
        self.prec = self.prec_orig.copy()
        
        # Importing pools' data
        self.attr = iodata.read_pools_data(self.path_pool_attr) # Pools attributes
        self.dav = iodata.read_pools_data(self.path_pool_dav) # Depth-area-volume tables from pools
        
        # Creating functions lists
        for pool in self.dav.values():
            self.list_dta.append(tools.interp(pool, 'h', 'A'))
            self.list_vtd.append(tools.interp(pool, 'V', 'h'))
            self.list_dtv.append(tools.interp(pool, 'h', 'V'))
        
        # Setting up default date range for simulations
        self.start_date = max(self.evap.date.min(), self.prec.date.min()).to_pydatetime()
        self.end_date = min(self.evap.date.max(), self.prec.date.max()).to_pydatetime()
        
        # Initialize list of dataframes output data
        self.list_poolsim = [None]*len(self.attr)
    
    
    def reset_inputdata(self):
        self.evap = self.evap_orig
        self.prec = self.prec_orig
    
    def set_simrange(self, start_date, end_date):
        '''
        Specify start and end date for the simulation. This must be coherent 
        with the date range of the input climate data
        
        '''
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    
    def test_continuity(self):
        '''
        Test if evap and prec dataset values within the simulation range
        are continuous, i.e., have no missing values
        '''
        
        evap_within = self.evap[self.start_date:self.end_date]
        prec_within = self.prec[self.start_date:self.end_date]
        
        any_null_evap = evap_within.value.isnull().any()
        any_null_prec = prec_within.value.isnull().any()
        
        # Conditions
        both = any_null_evap and any_null_prec
        anyone = any_null_evap or any_null_prec
        
        if both:
            msg = 'Both evaporation and precipitation series are NOT continuous within the date range'
            return False, msg
        else:
            if anyone:
                if any_null_evap:
                    msg = 'Evaporation series is NOT continuous within the date range'
                    return False, msg
                else:
                    msg = 'Precipitation series is NOT continuous within the date range'
                    return False, msg
            else:
                msg = 'Both evaporation and precipitation series ARE continuous within the date range'
                return True, msg
    
    
    def fill_data(self, within=True):
        '''
        Fills missing data with daily average for the same day of the month
        
        Args:
            within: (bool) If True, the missing values within the date range
            will be filled with the
            daily average within the date range given by the start_date and
            end_date attributes. If False, missing values from the whole
            dataframe will be filled with the date 
            range of the whole dataframe. Default is True.
        '''
        
        if within:
            evap = self.evap[self.start_date : self.end_date]
            prec = self.prec[self.start_date : self.end_date]
            
            self.evap.loc[self.start_date : self.end_date] = prepare.fill_data(evap)
            self.prec.loc[self.start_date : self.end_date] = prepare.fill_data(prec)
        
        else:
            self.evap = prepare.fill_data(self.evap)
            self.prec = prepare.fill_data(self.prec)
        
        
        
    
    def run_pool(self, id_pool):
        tc, msg = self.test_continuity()
        if tc is False:
            raise ValueError(msg)
            
        
        dav = self.dav[id_pool]
        max_depth = float(dav[dav.h == dav.h.max()].h)
        
        df = water.simulate_pool(self.evap, 
                               self.prec, 
                               self.attr, 
                               self.list_dta, 
                               self.list_vtd, 
                               self.list_dtv,
                               id_pool,
                               max_depth,
                               self.start_date,
                               self.end_date)
        
        
        # Set date as index
        df['i'] = df.index
        df = df.set_index('date', drop=False)
        
        # Add column 'haswater'
        df['haswater'] = df['depth'] > 0.01
        
        self.list_poolsim[id_pool] = df
    
    
    def run_pools(self):
        
        for i in range(len(self.list_poolsim)):
            self.run_pool(i)
    
    
    def plot_dav(self, id_pool=None):
        
        if id_pool is not None:
            plots.dav(self.dav[id_pool], id_pool)
