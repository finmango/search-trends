from apiclient.discovery import build
import pandas as pd
import os
from typing import Any
import datetime

# Keep these as module constants
SERVER = 'https://trends.googleapis.com'
API_VERSION = 'v1beta'
DISCOVERY_URL_SUFFIX = '/$discovery/rest?version=' + API_VERSION
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX
MAX_QUERIES = 30

class Timeline:
    def __init__(self, api_key=None):
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.environ.get('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY must be provided either through constructor or environment variable")
        self.service = self.get_client()
    
    def get_client(self) -> Any:
        return build('trends', API_VERSION, 
                    developerKey=self.api_key,
                    discoveryServiceUrl=DISCOVERY_URL)
    

    def date_to_string(self,datestring):
        """Convert date from (eg) 'Jul 04 2004' to '2004-07-11'. Args:
        
        datestring: A date in the format 'Jul 11 2004', 'Jul 2004', or '2004'
        Returns:
        The same date in the format '2004-11-04'
        Raises:
        ValueError: when date doesn't match one of the three expected formats.
        """
        try:
            new_date = datetime.datetime.strptime(datestring, '%b %d %Y')
        except ValueError:
            try:
                new_date = datetime.datetime.strptime(datestring, '%b %Y') 
            except ValueError:
                try:
                    new_date = datetime.datetime.strptime(datestring, '%Y')
                except:
                    raise ValueError("Date doesn't match any of '%b %d %Y', '%b %Y', '%Y'.")
        
        return new_date.strftime('%Y-%m-%d')



    def get_search_volumes(
        self,
        terms: list, 
        start_date: str, 
        end_date: str, 
        frequency: str,
        geo_restriction: str,
        geo_restriction_option: str
    ) -> pd.DataFrame:
        '''
        main function for querying the trends api.
        
        '''
        if geo_restriction == 'country':
        # Country format is ISO-3166-2 (2-letters), e.g. 'US'
            req = self.service.getTimelinesForHealth(terms=terms, time_startDate=start_date,
                                                    time_endDate=end_date,
                                                    timelineResolution=frequency,
                                                    geoRestriction_country=geo_restriction_option).execute()
        elif geo_restriction == 'dma':
            req = self.service.getTimelinesForHealth(terms=terms,
                                                    time_startDate=start_date,
                                                    time_endDate=end_date,
                                                    timelineResolution=frequency,
                                                    geoRestriction_dma=geo_restriction_option).execute()
        elif geo_restriction == 'region':
            # Region format is ISO-3166-2 (4-letters), e.g. 'US-NY' (see more examples # here: en.wikipedia.org/wiki/ISO_3166-2:US)
            req = self.service.getTimelinesForHealth(terms=terms,
                                                    time_startDate=start_date,
                                                    time_endDate=end_date,
                                                    timelineResolution=frequency,
                                                    geoRestriction_region=geo_restriction_option).execute()
        

        res_dict = {(line[u'term'], self.date_to_string(point[u'date'])):
                  point[u'value']
                  for line in req[u'lines']
                  for point in line[u'points']}
        
        return [[k[0],k[1],v] for k,v in res_dict.items()]


    def get_related(
            self,
            term: str,
            geography: str,
            start_date: str,
            end_date: str,
            type: str
    ):
        '''
        Queries related topics or queries based off of restrictions
        
        '''
        if type == 'topic':
            return self.service.getTopTopics(
                term= term, 
                restriction_geo = geography,
                restrictions_startDate=start_date,
                restrictions_endDate=end_date,
            ).execute()

        else:
            return self.service.getTopQueries(
                term= term, 
                restriction_geo = geography,
                restrictions_startDate=start_date,
                restrictions_endDate=end_date,

            ).execute()



