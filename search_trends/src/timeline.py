from apiclient.discovery import build
import pandas as pd
import os
from typing import Any

API_KEY = os.environ['API_KEY']
SERVER = 'https://trends.googleapis.com'
API_VERSION = 'v1beta'
DISCOVERY_URL_SUFFIX = '/$discovery/rest?version=' + API_VERSION
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX
MAX_QUERIES = 30

class Timeline :
    def __init__(self):
        self.service = self.get_client()
    

    def get_client(self) -> Any:
        return build('trends', API_VERSION, developerKey=API_KEY,
                discoveryServiceUrl=DISCOVERY_URL)


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
                                                    geoRestriction_country=geo_restriction_option)
        elif geo_restriction == 'dma':
            req = self.service.getTimelinesForHealth(terms=terms,
                                                    time_startDate=start_date,
                                                    time_endDate=end_date,
                                                    timelineResolution=frequency,
                                                    geoRestriction_dma=geo_restriction_option)
        elif geo_restriction == 'region':
            # Region format is ISO-3166-2 (4-letters), e.g. 'US-NY' (see more examples # here: en.wikipedia.org/wiki/ISO_3166-2:US)
            req = self.service.getTimelinesForHealth(terms=terms,
                                                    time_startDate=start_date,
                                                    time_endDate=end_date,
                                                    timelineResolution=frequency,
                                                    geoRestriction_region=geo_restriction_option)
        
        return pd.DataFrame(req[1:],columns=req[0])


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



