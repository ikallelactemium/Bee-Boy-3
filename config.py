"""Config file where all constant variable are defined
"""
import os


#variable azue authentication
tenant_id = "c23df2ff-564e-4346-b7fb-3b3449a2b771"
application_id = "65693b89-cc81-4e9f-9928-c8046bf7906f"


SCOPES = ['User.Read']
base_url = 'https://graph.microsoft.com/v1.0/'



endpoint = os.getenv("ENDPOINT_URL", "https://actemiumopenaiservice.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://actemiumsearchopenai.search.windows.net")  
search_key = os.getenv("SEARCH_KEY", "Zyx32Olcw069Cq2jZapnHm2mRjlrhIMHI7VQnLPu4MAzSeCa6igX")  
search_index = os.getenv("SEARCH_INDEX_NAME", "indexopenaibeeboy") 
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "1mmyAKRmYuBIdTMFlxOxMV5IFPbfllyykQUCx82sXkXLihOVTD2yJQQJ99AKAC5T7U2XJ3w3AAAAACOGVoMj")




