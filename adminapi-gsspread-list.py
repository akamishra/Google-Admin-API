import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="bold-mantis-296113-d134720d3b8b.json"
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import ListPropertiesRequest
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
    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "185646141"
    list_properties(account_id)


def list_properties(account_id):
    """Lists Google Analytics 4 properties under the specified parent account
    that are available to the current user."""
    client = AnalyticsAdminServiceClient()
    results = client.list_properties(
        ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=False)
    )
    index = 2
    count =0
    dataList=[]
    print("Result:")
    for property_ in results:
        print(property_)
        print(type(property_))               
        index = index + 1
        
        sheet = sh.worksheet("Property List")
        property_id =  getattr(property_,"name").split('/')[1]
        display_name=getattr(property_,"display_name")
        industry_category=str(getattr(property_,"industry_category")).split(".")[1]
        time_zone=getattr(property_,"time_zone")
        currency_code = getattr(property_,"currency_code")
        
        tempList = [property_id,display_name,industry_category,time_zone,currency_code]
        dataList.append(tempList)
        count = count + 1
    count = count + 1   
    sheet = sh.worksheet("Property List")
    sheet.update(f"A2:E{count}",dataList)
# [END analyticsadmin_properties_list]


if __name__ == "__main__":
    run_sample()