#!/usr/bin/env python

# August 2014
# Author Wong Fei Zhu(blk_ninja)
# Email: ninjakonnect.blogspot.com
# Tested under python2.7

import os
import sys
from pykickutils.PykickassAPI import PyKickassAPI
from pykickutils.PykickassUtils import PyKickassUtils



class PyKickassMenu(object):
    '''
    Handles the simple graphical user interface and design.
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.piapi = PyKickassAPI()
        self.piutils = PyKickassUtils()
        
    
    def clear_screen(self):
        '''
        Clears the screen when program starts to give nice output
        
        '''
        if("windows" in sys.platform.lower()):
            os.system("cls")
        elif ("linux" or "unix" or "darwin" in sys.platform.lower()):
            os.system("clear")
    
    def draw_logo(self):
        
        """
        Draws the ASCII Text Logo for the application.
        
        """
        
        print '''     
            
            \033[1;31m/**************************************************************\\\033[1;m
            \033[1;31m*     ______         _   __ _        _                         *\033[1;m
            \033[1;31m*     | ___ \       | | / /(_)      | |                        *\033[1;m
            \033[1;31m*     | |_/ /_   _  | |/ /  _   ___ | | __ __ _  ___  ___      *\033[1;m
            \033[1;31m*     |  __/| | | | |    \ | | / __|| |/ // _` |/ __|/ __|     *\033[1;m
            \033[1;31m*     | |   | |_| | | |\  \| | | (__|   < | (_||\__ \\\__\      *\033[1;m
            \033[1;31m*     \_|   \__,| | \_| \_/|_| \___||_|\_\\__,_||___/|___/      *\033[1;m
            \033[1;31m*             __/ |                                            *\033[1;m
            \033[1;31m*            |___/                                             *\033[1;m
            \033[1;31m*                                                              *\033[1;m  
            \033[1;31m\\**************************************************************/\033[1;m
            
            '''
    
    def program_info(self):
        """
        Displays information about the program
        """
        self.draw_logo()
        
        print """
        
        *******************************************************************************
        *                           PROGRAM INFORMATION                               *
        *                                                                             *
        *  This is a wrapper to query Kickass Torrents database. It provides          *
        *  a simple way to search for torrents information from the Kickass           *
        *  Database making use of the JSON endpoint currently provided by Kickass     *
        *  Torrents.                                                                  *
                                                                                      *
        *  So far this was developed with very basic functionality and was geared     *
        *  towards a specific audience. But as you may notice, I plan on actually     *
        *  fully making this into a full blown wrapper. You can see from some of the  *
        *  skeleton function/methods provided and from its documentation.             *
        *                                                                             *
        *  Author: Wong Fei Zhu (blk_ninja)                                      *
        *  Version: December 25, 2014                                                 *
        *                                                                             *
        *******************************************************************************
        """
        
        raw_input("\nPress [ENTER] To Return To The Main Menu...\n")
        self.clear_screen()
        return
     
    def display_program_menu(self):
        
        """
        Displays the application user menu to interact with the application.
        
        """
        
        try:
            #clear the screen for a nice output
            self.clear_screen()
        
            while True:
                # Display My Logo
                self.draw_logo()
                print '----------------------------------\n'                    
                print '1.  Perform a basic search'
                print '2.  Perform an advanced search'
                print '3.  View Basic Reports of Results'
                print '4.  Super User - Query DB using SQL'
                print '5.  Program Information'
                print '99. Exit Program\n'
                print '----------------------------------\n'
                
                try:    #lets enclose it in a ty/catch block incase user enters a non-digit
                    
                    user_chosen_option = int(raw_input('Enter an option>> '))
                    self.clear_screen()
                
                    if(user_chosen_option == 1):
                        self.display_simplesearch_dialog()  #display simple search dialog
                    elif(user_chosen_option == 2):
                        self.display_advancesearch_menu()
                    elif(user_chosen_option == 3):
                        self.display_basicreports_dialog()
                    elif(user_chosen_option == 4):
                        self.display_superuser_dialog()
                    elif(user_chosen_option == 5):
                        self.program_info()
                    elif(user_chosen_option == 99):
                        break
                    else:
                        self.draw_logo()
                        print('[--] ERROR: Invalid Option.')
                    raw_input("Press [ENTER] To Return To The Main Menu...\n") 
                    self.clear_screen()                   
                except ValueError, e:
                    print('[--] ERROR: Invalid Option.')
                    self.clear_screen()
                    continue
                
        except KeyboardInterrupt:
            print'[--] CTRL+C Pressed.'
        #except Exception, e:
        #    print'[--] ERROR: %s' % str(e)
        return 0
    
    #end of method
    
    def display_simplesearch_dialog(self):
        
        """
        Serves as the dialog for performing a basic search 
        using this wrapper.
        
        """
        self.draw_logo()
        print '***** Welcome to basic search ****'
        searchphrase= str(raw_input("Enter your search term/phrase >> ")) #get the phrase to search for
        numberofpages = None
        oauth = None
        while True: #
            
            try:
                numberofpages = int(raw_input("Enter the # of pages of results you want(1-100) >> "))   #get # of desired pages of results.
                break
            except ValueError, e:
                print '[-] Invalid page number, try again'
                continue
        
        #end while loop
                
        while True: 
            try:
                   
                oauth = str(raw_input("Authentication (y)es or (n)o. Press Enter Key for default (n) ? >> "))     #is authentication required.
                
                if oauth.lower() == 'y' or oauth.lower() == 'yes':  #if answer is yes
                    oauth = False
                    print '[-] Currently oauth2 authorization is not required, default used'
                    break     #uncomment in the future when oauth is required and remove continue
                
                elif oauth.lower() == 'n' or oauth.lower() == 'no':
                    oauth = False
                    break
                elif not oauth:
                    oauth = False
                    break
                
            except ValueError, e:
                oauth = False
                pass
            
        #end while loop
        
        #assign search results to a variable
        searchresults = self.piapi.simple_search(searchphrase, the_oauth=oauth, the_numberof_pages=numberofpages)
        
        if searchresults:   #if we have results, let's insert them into the database.
            self.piutils.insert_resultsin_db(searchresults) 
                    
    #end of method
       
    def display_advancesearch_menu(self):
        """
        Displays the dialog for advance search
        
        """            
        while True:
            
            self.draw_logo()
            print '***** Welcome to Advanced Search Reports *****' 
            print '\nThe advanced search build on simple search by'
            print 'providing more search paramaters for a user'
            print 'to choose from.'
            print '' 
            print 'The advanced search has to be carefully crafted'
            print 'return the right results as well as avoid errors'
            print 'on the server end.\n'
            print '1.  Search Using Advance Options'
            print '2.  View Advanced Search Parameters'
            print '99. Return to Main Menu\n'

            
            try:    #lets enclose it in a ty/catch block incase user enters a non-digit
                
                user_chosen_option = int(raw_input('Enter an option>> '))
                self.clear_screen()
                
                if(user_chosen_option == 1):
                    pass
                elif(user_chosen_option == 2):
                    self.display_advancesearch_help()
                elif(user_chosen_option == 3):
                    pass
                elif(user_chosen_option == 99):
                    break
                else:
                    self.draw_logo()
                    print('[--] ERROR: Invalid Option.')
                
                raw_input("Press [ENTER] To Return To Previous Menu...\n")
                self.clear_screen()
                    
            except ValueError, e:
                print('[--] ERROR: Invalid Option.')
                self.clear_screen()
                continue
        
        #end while loop
    
    #end of method
    
    def display_advancedsearch_dialog(self):
        """
        Displays the dialog to start an advanced
        search.
        
        """
        pass
    
    def display_basicreports_dialog(self):
        """
        Displays the basic reports dialog for user to 
        run canned reports
        
        """
        while True:
            self.draw_logo()
            print '***** Welcome to Basic Reports'
            print 'Below are the available canned reports\n'
            print '1.  View All Results in the DB'
            print '2.  View Basic Select Columns(id, title, and seeds)'
            print '3.  View Statistics of Torrent Seeds'
            print '4.  View Statistics of Torrent Votes'
            print '5.  View Statistics of Torrent Verifications'
            print '99. Return to Main Menu\n'

            
            try:    #lets enclose it in a ty/catch block incase user enters a non-digit
                
                user_chosen_option = int(raw_input('Enter an option>> '))
                self.clear_screen()
                
                if(user_chosen_option == 1):
                    self.display_alldbresults_dialog()
                elif(user_chosen_option == 2):
                    self.display_selectdbresults_dialog()
                elif(user_chosen_option == 3):
                    self.display_topfiveseed_dialog()
                elif(user_chosen_option == 4):
                    self.display_topfivevotes_dialog()
                elif(user_chosen_option == 5):
                    self.display_topfiveverified_dialog()
                elif(user_chosen_option == 99):
                    break
                else:
                    self.draw_logo()
                    print('[--] ERROR: Invalid Option.')
                
                raw_input("Press [ENTER] To Return To Previous Menu...\n")
                self.clear_screen()
                    
            except ValueError, e:
                print('[--] ERROR: Invalid Option.')
                self.clear_screen()
                continue
        
        #end while loop
    #end of method
    
    
    def display_superuser_dialog(self):
        
        """
        Displays the dialog to provide user the ability
        to write custom SQL queries for results stored
        in the database.
        
        """

        self.draw_logo()    #display logo
        print '***** Welcome to the Super User Mode *****'
        self.piutils.select_data_dictionary()   #generate the data dictionary to help user.
         
        while True: #lets continue giving the user the prompt to enter custom query
            custquery = str(raw_input("Enter your SQL statement (Enter Quit to exit this screen) \n>> ")) #get sql statement
            if custquery.lower() == 'quit': #if quit, lets go back to our main screen.
                break
            else:
                self.piutils.custom_query_db(custquery) #display results on the screen
                continue
        
    #end of method
        
    
    def display_alldbresults_dialog(self):
        """
        Displays all results from the database
        
        """
        self.piutils.select_allsearch_results() #display all search results
    #end method
    
    def display_selectdbresults_dialog(self):
        """
        Displays all results from the database
        
        """
        #display select torrent info
        self.piutils.select_basicinfo_results() 
    
    #end method
    
    
    def display_topfiveseed_dialog(self):
        
        """
        Displays the top 5 seeded torrents
        from the database.
        
        """
        #display top 5 seeded torrents, also plots on a graph
        self.piutils.select_topfive_seeds() 
    
    #end of method
    
    def display_topfivevotes_dialog(self):
        
        """
        Displays the top 5 voted torrents
        from the database.
        
        """
        #display top 5 seeded torrents, also plots on a graph
        self.piutils.select_topfive_voted() 
    
    #end of method
    
    
    def display_topfiveverified_dialog(self):
        
        """
        Displays the top 5 verified torrents
        from the database.
        
        """
        #display top 5 seeded torrents, also plots on a graph
        self.piutils.select_topfive_verified() 
        
    #end of method
    
    def display_advancesearch_help(self):
        """
        Displays the list of parameter options
        when searching using the advance feature
        
        """
        print '***** Available Search Options *****'
        print '\nTorrent Posting Date Within Timeframe'
        print 'Parameter Name = age'
        print 'Values = Any Time, hour, 24hr, weeks, year\n'
       
       

    
    #end of method
    