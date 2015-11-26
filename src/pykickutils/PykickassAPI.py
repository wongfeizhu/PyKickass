#!/usr/bin/env python

# August 2014
# Author Wong Fei Zhu(blk_ninja)
# Email: ninjakonnect.blogspot.com
# Tested under python2.7


import json
import sys
import urllib
import urllib2
import oauth2 as oauth
from pykickutils.PykickassUtils import PyKickassUtils


class PyKickassAPI(object):
    """
    This is a python wrapper to access the Kickass Torrent Search.
    Kickass torrents offers a JSON endpoint that can return search data.
    
    #the highest possible # of pages of results. Currently only up to 100
    
    """
    
    def __init__(self,
                 the_auth_req=False):
        """
        Constructor
        """
        self.piutils = PyKickassUtils() # lets initialize our pykickutils obect/reference
    
    def oauth_request(self, the_api_endpoint="https://kickass.so/json.php?",
                      the_consumer_key=None,
                      the_consumer_secret=None,
                      the_access_token=None,
                      the_access_secret=None):
        """
        Authenticates a user and querys the API using oauth2 authentication.
        
        NOTE: NOT FULLY IMPLEMENTED, SKELETON FOR FUTURE
        
        @param the_api_endpoint: The search API url
        @param the_consumer_key: Consumer Key
        @param the_consumer_secret: Consumer secret
        @param the_access_token: The Access Token
        @param the_access_secret: The Token Secret
        """
        data = None
        
        try:
            
            consumerinfo = oauth.Consumer(key=the_consumer_key, secret=the_consumer_secret) #assign the consumer key and secret info
            tokeninfo = oauth.Token(key=the_access_token, secret=the_access_secret) #assing the token key and secret info
            client = oauth.Client(consumerinfo, tokeninfo)
            
            response, data = client.request(the_api_endpoint, method='GET')
                
        except ValueError:
            pass
        except urllib2.HTTPError, e:
            pass
        except Exception, ex:
            print "Oops. something went wrong" + str(ex)
            pass
        
        return data #this is what we are interested in any way, why not get it.
    
    
    def noauth_request(self, the_api_endpoint="https://kickass.so/json.php?", the_params={}):
        """
        Query's the API in non oaut mode.
        
        @param the_api_endpoint: The search API url
        @param the_params: A dictionary of parameters to be passed to the query string
        """
        data = None
        encodedurl = the_api_endpoint + urllib.urlencode(the_params)

        print '[+] Retrieving results from {0} '.format(encodedurl) 
        try:    
            response = urllib2.Request(encodedurl)
            data = json.load(urllib2.urlopen(response))
        
        except ValueError:
            pass
        except urllib2.HTTPError, e:
            pass
        except Exception, ex:
            print "Oops. something went wrong" + str(ex)
            pass
        
        return data #this is what we are interested in any way, why not get it.
    
    
    def simple_search(self, the_search_term, the_oauth=False, the_numberof_pages=5):
        """
        Performs a simple search using a supplied search term or phrase
        and takes optionally whether oauth autorizations is required,
        or a number of pages of results to retrieve.
        
        @param the_search_term: The phrase or term to query for.
        @param the_oauth: Is oauth2 authorization required.
        @param the_numberof_pages: The number of pages of results to retrieve.
        """
        
        print '[+] Searching for {0} from Kickass Torrents...'.format(the_search_term)
        searchresults = {}  #set our returned results to an empty dictionary
        populatedresults = [] #set our populated list of results to an empty list
        
        if(the_numberof_pages in range(1,101)): #we can only retrieve up to 99 pages of data. UpLim set to 101 due to 0-indexing
            
            if the_oauth: #if ouath2 authentication is required.
                searchresults = self.oauth_request()
            else:
                print '[+] Retrieving results, this depends on how many pages\n    requested, so please be patient...\n'
                for page in range(0, the_numberof_pages): #we strrting the range from 0 because the first results set is usually page 0
                    #else if a user put in # of pages as 1, range cannot find it 
                    #due to 1 being the upper limit

                    searchresults = self.noauth_request(the_params={'q':str(the_search_term),'page':page}) #casted to string for basic sanitization
                    
                    if searchresults == None:
                        break
                    else:
                        if int(searchresults['total_results']) == 0:
                            
                            print '[-] No results found for {0} \n'.format(the_search_term)
                            print '[-] No results found, DB still has the old data from previous search'           
                            break
                        else:
                            populatedresults.extend(self.piutils.add_toresults_list(searchresults)) #lets add the results to our populated list.
        else:
            print '[-] Sorry Kickass Torrents only allow me retrieve between 1 and 99 pages\n'
            
        return populatedresults #return our populated list of tuples

    def advanced_search(self, the_params={}, the_oauth=False):
        """
        Performs an advanced search with user supplied query string,
        capable of adding several query string in the search parameters
        
        @param the_params: The user supplied parameters.
        @param the_oauth: Is outh2 authorization required.
        """
        
        print '\n[+] Searching for {0} from Kickass Torrents...'.format(the_params['q'])
        searchresults = {}  #set our returned results to an empty dictionary
        populatedresults = [] #set our populated list of results to an empty list
        
        
        numberofpages = the_params['page'] #lets get the #of pages first from the supplied param dict.
        
        #lets remove the page# param out, this throws off our search as it
        #explicitly searches for a static page(page#) rather than iterating
        #through pages of results. The page# param is supposed to indicate how                                                               #many pages of data we want, not a static page.
        modifiedparams = self.piutils.remove_dict_element(the_params) 
        
        if(numberofpages in range(1,101)): #we can only retrieve up to 99 pages of data. UpLim set to 101 due to 0-indexing
            
            if the_oauth: #if ouath2 authentication is required.
                searchresults = self.oauth_request()    #NOT A FUNTIONING METHOD, SKELETON FOR FUTURE
            else:
                print '[+] Retrieving results, this depends on how many pages\n    requested, so please be patient...\n'
                for page in range(0, numberofpages): #we strrting the range from 0 because the first results set is usually page 0
                    #else if a user put in # of pages as 1, range cannot find it 
                    #due to 1 being the upper limit
                    
                    modifiedparams['page'] = page   #lets add that key/value pair back, but this time, we are giving it the page we want
                                                    #we are basically forcing the iteration of pages rather 
                                                    #than trying to retrieve that static page#
                                                    
                    searchresults = self.noauth_request(the_params=modifiedparams) #perform our search just like simple search
                    
                    if searchresults == None:
                        break
                    else:
                        if int(searchresults['total_results']) == 0: #if our total results is 0, we obviously have no results returned
                            
                            print '[-] No results found for {0} \n'.format(the_params['q'])
                            break
                        else:
                            
                            populatedresults.extend(self.piutils.add_toresults_list(searchresults)) #lets add the results to our populated list.
        else:
            print '[-] Sorry Kickass Torrents only allow me retrieve between 1 and 99 pages'
            
        return populatedresults #return our populated list of tuples
    

        
        