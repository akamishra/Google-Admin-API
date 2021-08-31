#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Admin API sample application which creates a Google
Analytics 4 property.
See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties/create
for more information.
"""
# [START analyticsadmin_properties_create]
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="bold-mantis-296113-d134720d3b8b.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secret.json"
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import Property
from google.analytics.admin_v1alpha.types import WebDataStream
import gspread
gc = gspread.service_account(filename='bold-mantis-296113-d134720d3b8b.json')
sh = gc.open("Google Analytics 4 - Admin")


# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']


def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'bold-mantis-296113-d134720d3b8b.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
   
    print("explicit",buckets)

def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "185646141"
    create_property(account_id)


property_ = ""
def create_property(account_id):
    global property_
    """Creates a Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    
    
    index =2
    data =''
    
    while True:
        
        cell = f"A{index}"
        cellStatus = f"H{index}"
        
        tempData=sh.sheet1.get(cell)
        tempStatus=sh.sheet1.get(cellStatus)
       
        
        if len(tempData)> 0:
            
            if len(tempStatus) > 0:
                tempStatus=tempStatus[0][0]
            
            if tempStatus != "Completed":
                dataCell=f"A{index}:h{index}"
                
                data =sh.sheet1.get(dataCell)
                
                parentID = data[0][0]
                currencyCode =data[0][1]
                displayName = data[0][2]
                industryCategory = data[0][3]
                timeZone = data[0][4]
                dataStreamType = data[0][5]
                displayStreamName = data[0][6]
                print(parentID,'-',currencyCode,'-',displayName,'-',industryCategory,'-',timeZone,'-',dataStreamType,'-',displayStreamName)
                
                
                property_ = client.create_property(
                    property=Property(
                        parent=f"accounts/{parentID}",
                        currency_code=f"{currencyCode}",
                        display_name=f"{displayName}",
                        industry_category=f"{industryCategory}",
                        time_zone=f"{timeZone}",
                    )
                )
            
                print("Property Created:")
                print(property_)    
                property_id = getattr(property_,"name").split('/')[1]
                if dataStreamType.upper() == 'WEB': 
                    datastreamOutput=create_web_data_stream(property_id,displayStreamName)
                    print('measurement_id : ',datastreamOutput.measurement_id)
                    sh.sheet1.update(cellStatus,'Completed')
                    sh.sheet1.update(f"I{index}",datastreamOutput.measurement_id)
                
                
            index = index + 1
                
        else:
            break
    


def create_web_data_stream(property_id,displayStreamName):
    """Creates a web data stream for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    web_data_stream = client.create_web_data_stream(
        parent=f"properties/{property_id}",
        web_data_stream=WebDataStream(
            default_uri="https://www.google.com", display_name= displayStreamName
        ),
    )

    print("Web Data Stream Created:")
    print(web_data_stream)
    return web_data_stream



    
# [END analyticsadmin_properties_create]

if __name__ == "__main__":
    run_sample()
   
    
    
    
    
def list_accounts():
  """Lists the available Google Analytics accounts."""
  from google.analytics.admin import AnalyticsAdminServiceClient
  # Using a default constructor instructs the client to use the credentials
  # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
  client = AnalyticsAdminServiceClient()

  # Displays the configuration information for all Google Analytics accounts
  # available to the authenticated user.
  for account in client.list_accounts():
    print(account)
