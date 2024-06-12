# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 22:40:24 2018

@author: David
"""

import os

def run():
    """
    Function that implements command line application to run whole program and
    output all data into a specific folder in /Output
    
    #TODO Implement this
    """
    name_test = input('Write name of test:  ')
    
    os.mkdir('Output/'+name_test)
    
if __name__ == '__main__':
    run()