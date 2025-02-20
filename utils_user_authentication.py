"""Beewave module for authentication
    Summary
    -------
        
    Documentation
    -------

    Packages
    -------
"""


import requests
from msal import PublicClientApplication
import config



class user_authantification:
    def __init__(
        self,
        tenant_id = config.tenant_id,
        application_id = config.application_id,
        scopes = config.SCOPES,

    ):
        """[Constructor for the user_authantification class]

        Parameters
        ----------
        tenant_id : str
            [path to the file of data]
        application_id : [type]
            [login of the user for access to influxdb database]
        scopes : [type]
            [password of the user for access to influxdb database]
        base_url : [type]
            [name of the spy to look for]

        """
        self.TENANT_ID = tenant_id 
        self.APPLICATION_ID = application_id 
        self.SCOPES = scopes 

  
      
      
    def azure_AD_authantification(self):
        
        app = PublicClientApplication(
            self.APPLICATION_ID,
            authority=f"https://login.microsoftonline.com/{self.TENANT_ID}/")
        flow = app.initiate_device_flow(scopes=self.SCOPES)

        return app,flow

    def send_request(app,flow,base_url = config.base_url):

        result = app.acquire_token_by_device_flow(flow)# resulat 
        acces_token_id = result['access_token']
        headers = {'Authorization':'Bearer ' + acces_token_id}
        endpoint = base_url + 'me'
        # send request to obtain user informations using Microsoft graph API
        response = requests.get(endpoint,headers=headers)
        json_response = response.json()

        return json_response
