# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:10:40 2018

@author: David Paez
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


style = 'presentation.mplstyle'


def update_style():
    #plt.style.use(style)
	pass

    
def setup_month_axes(ax, year=2015):
    
    months_mjr = mpl.dates.MonthLocator()
    months_mnr = mpl.dates.MonthLocator(bymonthday=15)
    monthsFmt = mpl.dates.DateFormatter('%b')
    
    ax.xaxis.set_major_locator(months_mjr)
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    
    ax.xaxis.set_minor_locator(months_mnr)
    ax.xaxis.set_minor_formatter(monthsFmt)
    
    ax.set_xlim(datetime.date(year-1,12,17), datetime.date(year+1,1,13))
    
    return ax

def barplot(df):
    update_style()
    
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col', figsize=(10,4))
    sns.set(rc={"figure.figsize": (15, 2)})
    
    sign = df['runoff'] > 0
    df.plot(ax=axes[0], kind='bar',x='date', y='runoff', color=sign.map({True: 'r', False: 'b'}))
    
    sign = df['evap'] > 0
    df.plot(ax=axes[1], kind='bar',x='date', y='evap', color=sign.map({True: 'r', False: 'b'}))

def dav(df, id_pool):
    '''
    Line plot of depth-area-volume relatinship
    '''
    update_style()
	
    axislabel_size = 40
    axisnumber_size = 30
    
    fig, ax1 = plt.subplots(figsize=(13,9))
    
    
    ax1.plot(df.h, df.A, 'b-', linewidth=4)
    ax1.set_xlabel('Depth (m)', fontsize=axislabel_size)
    ax1.tick_params('x', width=3, length=10, labelsize=axisnumber_size)
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Surface area ($m^2$)', color='b', fontsize=axislabel_size)
    ax1.tick_params('y', width=3, length=10, colors='b', labelsize=axisnumber_size)

    
    ax2 = ax1.twinx()
    ax2.plot(df.h, df.V, 'r', linewidth=4)
    ax2.set_ylabel('Volume ($m^3$)', color='r', fontsize=axislabel_size)
    ax2.tick_params('y', width=3, length=10, colors='r', labelsize=axisnumber_size)
    
    #fig.tight_layout()
    plt.suptitle('Pool '+str(id_pool), weight='bold')
    
    plt.setp(ax1.spines.values(), linewidth=4)

    plt.savefig('Output/dav_p'+str(id_pool)+'.png')
    plt.show()
    
    
    



def scatterfrompool(site, id_pool):
    
    update_style()
    
    years = range(site.start_date.year, site.end_date.year+1)
    wdf = site.list_poolsim[id_pool]
    fig, axes = plt.subplots(nrows=len(years), ncols=1, sharex=False, figsize=(20,15))
    
    
    for i, year in enumerate(years):
        df = wdf[wdf.date.dt.year == year]
        df_true = df[df.haswater == True]
        df_false = df[df.haswater == False]

        a = axes[i]
        a = setup_month_axes(a, year)
        a.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        a.set_ylabel(str(year), rotation='horizontal', ha='right', va='center')
        a.tick_params(axis='y', labelleft=False, pad=25)
        a.tick_params(axis='x', which='both', labelsize=25, pad=25)
        axes[i] = a
        
        axes[i].scatter(df_true.date.values, df_true.haswater.values,s=20, color='b')
        axes[i].scatter(df_false.date.values, df_false.haswater.values, s=20, color='r')
        

    setup_month_axes(a, year)
    plt.subplots_adjust(hspace=1)
    
    plt.savefig(site.path_outputdir+'/scatter_haswater_p'+str(id_pool)+'.png', facecolor='w')
    
#    loc = [365*(i/12) for i in range(12)]
#    plt.xticks(
#            loc,
#            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
 
    

def lineplotCI(x_data, y_data, sorted_x, low_CI, upper_CI, x_label, y_label, title):
    '''
    Define a function for the line plot with intervals
    '''
    
    update_style()
    
    # Create the plot object
    fig, ax = plt.subplots(figsize=(20,10))

    # Plot the data, set the linewidth, color and transparency of the
    # line, provide a label for the legend
    ax.plot(x_data, y_data, alpha = 1, label = 'Fit')
    # Shade the confidence interval
    ax.fill_between(sorted_x, low_CI, upper_CI, alpha = 0.4, label = 'mean +/- 0.5*std')
    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Display legend
    ax.legend(loc = 'lower right')
    
    return ax