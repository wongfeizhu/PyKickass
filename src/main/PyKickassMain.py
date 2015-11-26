#!/usr/bin/env python

# August 2014
# Author Wong Fei Zhu(blk_ninja)
# Email: ninjakonnect.blogspot.com
# Tested under python2.7

import os
import sys

#add our program folder to python path
sys.path.append(os.path.abspath(os.path.dirname("/opt/PyKickass/src/")))

#Imports
from pykickutils.PykickassUtils import PyKickassUtils
from pykickutils.PykickassAPI import PyKickassAPI
from main.PykickassMenu import PyKickassMenu 


class PyKickassMain(object): 
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    
    if __name__ == "__main__":
        
        piutils = PyKickassUtils()
        pimenu = PyKickassMenu()
        piapi = PyKickassAPI()
        
        pimenu.display_program_menu()
        
        """
        
        
        #piapi.simple_search("alladin", the_numberof_pages=100)
        #piapi.simple_search("game of thrones", the_numberof_pages=3)
        results = piapi.advanced_search({'q':"game of thrones",'category':"all",'page':1})
        if results:
            piutils.insert_resultsin_db(results)
            #piutils.plot_bar_graph(results)
        
        #piutils.select_allsearch_results()
        #piutils.show_topfive_seeds()
        piutils.show_topfive_verified()
        #piutils.show_topfive_voted()
        
        """
    #end
        
