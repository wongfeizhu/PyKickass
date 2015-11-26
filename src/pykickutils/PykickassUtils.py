#!/usr/bin/env python

# August 2014
# Author Wong Fei Zhu(blk_ninja)
# Email: ninjakonnect.blogspot.com
# Tested under python2.7
 
import sqlite3 as sql
import pandas as pd
import sys
import time

from prettytable import PrettyTable, from_db_cursor
from matplotlib import pyplot as plt

class PyKickassUtils(object):
    
    """
    A utility class for the simple API wrapper.
    """
    
    #JSON OBJECTS
    TORRENTLIST ='list'
    TITLE = 'title'
    CATEGORY = 'category'
    DOWNLOADLINK = 'link'
    GUID = 'guid'
    PUBDATE ='pubDate'
    TORRENTLINK ='torrentLink'
    FILES = 'files'
    COMMENTS = 'comments'
    HASH = 'hash'
    PEERS = 'peers'
    SEEDS = 'seeds'
    LEECHS = 'leechs'
    SIZE = 'size'
    VOTES = 'votes'
    VERIFIED = 'verified'

    def __init__(self):
        '''
        Constructor
        '''
    
    def connect_to_db(self, the_db_name="/opt/PyKickass/src/db/torrents.db"):
        
        """
        Initiates a connection to a SQLite 3 database
        
        """
        con = None  #intialize to none
        cur = None
        try:
            
            con = sql.connect(the_db_name) #connect to the database
            con.row_factory = sql.Row      #we want our returned results to be in dict cursor for east manipulation
            cur = con.cursor()              #assign the cursor.
            
        except sql.Error, e:# lets catch sql errors here
            print "Oops, something went wrong : {0}".format(str(e))
        
        return (con,cur) #return as a tuple, the connection and  
    
    #end of method         
    
    
    
    def add_toresults_list(self, the_search_results):
        """
        Populates the results into one list for easier manipulation
        such as insertion into the database or simple display to 
        console.
        @param the_search_results: The json dict returned by search
        
        """
        resultslist = []    #initalize empty list to hold populated results
        
        for torrentresult in the_search_results[PyKickassUtils.TORRENTLIST]:  #iterate through the results list.
            
            #add list of tuples to the results list.s
            resultslist.append((torrentresult[PyKickassUtils.TITLE], torrentresult[PyKickassUtils.CATEGORY],torrentresult[PyKickassUtils.DOWNLOADLINK],
                                       torrentresult[PyKickassUtils.GUID],torrentresult[PyKickassUtils.PUBDATE], torrentresult[PyKickassUtils.TORRENTLINK],
                                       torrentresult[PyKickassUtils.FILES],torrentresult[PyKickassUtils.COMMENTS], torrentresult[PyKickassUtils.HASH], 
                                       torrentresult[PyKickassUtils.PEERS],torrentresult[PyKickassUtils.SEEDS],torrentresult[PyKickassUtils.LEECHS], torrentresult[PyKickassUtils.SIZE], 
                                       torrentresult[PyKickassUtils.VOTES], torrentresult[PyKickassUtils.VERIFIED]))
            
        return resultslist  #return populated results 
    
    #end of method    
        
    def display_on_console(self, the_results):
        
        """
        Displays the data on the console formatted nicely using
        pretty table.
        
        @param the_results: A list containing data
        s
        """
        
        print '\n[+] Total # of results retrieved: {0}'.format(len(the_results))
        print '[+] Displaying results'
        
        for result in the_results:
            print result
    
    #end of method
             
    def display_search_results(self, the_populated_results):
        """
        A helper to iterate through the search results.
        This was removed from the simple and advance search methods for ease
        of manipulations. 
        
        Only used when user wishes to only iterate and display simple file name.
        """
        if the_populated_results['total_results']: # continue processing if search returned some results
            print "[+] Total # of Results : " + str(the_populated_results['total_results'])
            
            
            for torrent in the_populated_results['list']:
                print torrent['title']
        else:
            print "[-] No results returned"
    
    #end of method
        
    
    def custom_query_db(self, the_cust_query):
        """
        Provides an ability for the user to custom query
        the results stored in the Torrents DB after a 
        search if the USER is familiar with SQL
        
        """
        
        (con,cur) = self.connect_to_db()
        
        try:
            print '\n[+] Retrieving all results from database...'
            cur.execute(the_cust_query) #retrive the desired data from database.
            
            results = cur.fetchall()
            self.display_pretty_table(cur, results) #assign the results to pretty table
                        
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
        finally:
            if con:
                con.close()
                
    #end of method
    
    def insert_resultsin_db(self, the_data):
        """
        Inserts retrieved results from search into the
        Torrents database.
        
        """
        (con, cur) = self.connect_to_db()
        
        try:
            if con:
                self.display_processing_cursor('\n[+] Inserting results into the database... ')
                with con:
                    cur.execute("DROP TABLE IF EXISTS Torrents")
                    
                    cur.execute("CREATE TABLE Torrents(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT,\
                                    downloadlink TEXT, guid TEXT, pubdate TEXT, torrentlink TEXT, numoffiles INTEGER,\
                                    numofcomments INTEGER, hash TEXT, numofpeers INTEGER, numofseeds INTEGER,\
                                    numofleechs INTEGER, filesize INTEGER, numofvotes INTEGER, numofverified INTEGER)")
                    
                    if the_data:
                        cur.executemany("INSERT INTO Torrents(title,category,downloadlink,guid,pubdate,torrentlink,numoffiles,\
                                    numofcomments,hash,numofpeers,numofseeds,numofleechs,filesize,numofvotes, numofverified) \
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", the_data)
                    
            
            con.commit()
            print '[+] Insertion into database complete.\n'
        except sql.Error, e:
            if con:
                con.rollback()
            print '[-] Oops something went wrong, we had issues inserting in DB {} '.format(str(e))
        
        finally:
            if con:
                con.close()
    
    #end of method
    
    def select_allsearch_results(self):
        """
        Selects from the database all search results
        and displays it to console.
        
        """
        (con,cur) = self.connect_to_db()
        
        try:
            self.display_processing_cursor('[+] Retrieving all results from the database...', the_numof_secs=1)
            cur.execute("SELECT * FROM Torrents") #retrive the desired data from database.
            results = cur.fetchall()
            
            self.display_pretty_table(cur, results) #assign the results to pretty table
            
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass
        finally:
            if con:
                con.close()
                
    #end of method
    
    def select_data_dictionary(self):
        """
        Selects from the database all the table structure
        and displays it to console.
        
        """
        (con,cur) = self.connect_to_db()
        
        try:
            self.display_processing_cursor('[+] Generating data dictionary to help you...', the_numof_secs=1)
            print 'Table Name = Torrents'
            cur.execute("PRAGMA table_info(Torrents)") #retrive the desired data from database.
            results = cur.fetchall()
            
            self.display_pretty_table(cur, results) #assign the results to pretty table
            
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass
        finally:
            if con:
                con.close()
                
    #end of method
    
    def select_basicinfo_results(self):
        """
        Selects from the database three basic info on 
        all search results. Specifically the id, title
        and download link of the torrents
        
        """
        (con,cur) = self.connect_to_db()
        
        try:
            self.display_processing_cursor('[+] Retrieving select columns from the database...', the_numof_secs=1)
            cur.execute("SELECT id, title, numofseeds FROM Torrents") #retrive the desired data from database.
            results = cur.fetchall()
            
            self.display_pretty_table(cur, results) #assign the results to pretty table
            
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass
        finally:
            if con:
                con.close()
                
    #end of method
        
    def select_topfive_seeds(self):
        """
        Retrieves from the database, the top 5 seeded
        torrents and displays it on to console as well
        as creating a bar graph for it
        """    
        (con,cur) = self.connect_to_db()
        
        try:
            self.display_processing_cursor('[+] Retrieving TOP 5 SEEDED torrents from database...', the_numof_secs=1)
            cur.execute("SELECT id, numofseeds FROM Torrents ORDER BY numofseeds DESC LIMIT 5") #retrive the desired data from database.
            
            results = cur.fetchall()
            self.display_pretty_table(cur, results) #assign the results to pretty table
            self.plot_bar_graph(results, "Top 5 Seeded", "Number of Seeds")
                     
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass
        finally:
            if con:
                con.close() 
    
    #end of method
    
    def select_topfive_voted(self):
        """
        Retrieves from the database and displays the
        top 5 voted torrents
        
        """
        (con,cur) = self.connect_to_db()
        
        try:
            print '\n[+] Retrieving TOP 5 VOTED torrents from database...'
            cur.execute("SELECT id, numofvotes FROM Torrents ORDER BY numofvotes DESC LIMIT 5") #retrive the desired data from database.
            
            results = cur.fetchall()
            self.display_pretty_table(cur, results) #assign the results to pretty table
            self.plot_bar_graph(results, "Top 5 Voted", "Number of Votes")
                        
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass 
        finally:
            if con:
                con.close()
    
    #end of method
    
    def select_topfive_verified(self):
        """
        Retrieves from the database and displays the
        top 5 voted torrents
        
        """
        (con,cur) = self.connect_to_db()    #create our database objects
        
        try:
            print '\n[+] Retrieving TOP 5 VERIFIED torrents from database...'
            with con:
                
                cur.execute("SELECT id, numofverified FROM Torrents ORDER BY numofverified DESC LIMIT 5") #retrive the desired data from database.            
                results = cur.fetchall()
                self.display_pretty_table(cur, results) #assign the results to pretty table
                self.plot_bar_graph(results, "Top 5 Verified", "Number of Verifications")
                
        except sql.Error, e:
            print '[-] Oops something went wrong: {0} '.format(str(e))
            pass 
        finally:
            if con:
                con.close()
    
    #end of method
    
    def display_pretty_table(self, the_cursor, the_results):
        
        """
        Displays data on using pretty table to
        console.
        @param the_cursor: A database cursor
        @param the_results: The results of a DB query
        
        """
        print '[+] Printing results...'
        
        try:
            
            colnames = [cn[0] for cn in the_cursor.description] #lets retrieve col name from cursor
        
            pt = PrettyTable(colnames)  #create our pretty table object
            for result in the_results:  #iterate over our results adding to pretty table
                pt.add_row(result)
            
            print pt                    #print our pretty table
        
        except:
            print '[-] Error printing.'
            pass
        
    #end of method
        
    def plot_bar_graph(self, the_results, the_activity_type, the_yaxis_title):
        """
        Plots data on a bar graph
        @param the_results: The results of a DB query
        @param  the_activity_type: The activity type(Seeded,Verified,Voted)
        @param the_yaxis_title: The title to give the bar chart diagram
        """  
        x_values = []   #our x axis values
        y_values = []   #our y axis values
        
        #populate x and y axis values from supplied data
        if the_results: #lets ensure we actually have data to plot
            
            try:
                
                self.display_processing_cursor('[+] Populating graph data...')
                x_vals = [("FID#"+str(i[0])) for i in the_results]
                y_vals = [i[1] for i in the_results]
            
                data = {the_activity_type:pd.Series(y_vals, index=x_vals)} #populate a panda data structure with our values
                df = pd.DataFrame(data) #create a pandas data frame from our data
            
                fig, axes = plt.subplots()
                axes.set_ylabel(the_yaxis_title, fontsize=15)
                axes.set_xlabel('Torrent File ID''s')
                df.plot(kind = 'bar', ax=axes, figsize=(12,10), title=the_activity_type, color='blue')

                """
                #if we had several series, we would iterate through
                for index, columnname in enumerate(df.columns):
                    df[columnname].plot(kind = 'bar', ax=axes[index], figsize=(12,10), title=columnname)
                """
                plt.savefig(('/opt/PyKickass/src/charts/'+the_activity_type +'.png'), bbox_inches='tight') #save the bar chart
                print '[+] A copy of the graph has been saved in the charts folder.'
                plt.show()  #optionall show it to the user.
            
            except Exception, e:
                print '[-] Error generating the bar graph chart', str(e)
                pass
        else:
            print '[-] No data available to plot bar graph'
    
    #end of method

        
    def remove_dict_element(self, the_dict, the_key='page'):
        """
        Removes an element from a dictionary and
        returns the modified dictionary.
        
        A helper when using the advanced query feature
        to search.
        """   
        try:
            newdict = dict(the_dict)
            del newdict['page']
            return newdict
        
        except:
            pass
    
    #end of method
    
    def display_processing_cursor(self,the_message, the_numof_secs=2, the_timeto_sleep=.5):
        '''
        Displays a rotating cursor to indicate processing.
        @param the_message: The desired message to display before displaying cursor
        @param the_numof_secs: The number of seconds to display prompt
        @param the_timeto_sleep: The number of milliseconds to sleep between char displays
        
        '''
        print "\nPlease wait a moment ", the_message
        syms = ['\\', '|', '/', '-']
        bs = '\b'

        for _ in range(the_numof_secs):
            for sym in syms:
                sys.stdout.write(bs + "%s" % sym) #print char
                sys.stdout.flush()
                time.sleep(.5)
                      
        print ''
    
    #end of method
    
