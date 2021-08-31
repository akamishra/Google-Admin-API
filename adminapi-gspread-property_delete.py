import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.analytics.admin import AnalyticsAdminServiceClient

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('bold-mantis-296113-d134720d3b8b.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open('Google Analytics 4 - Admin')
sheet_instance = sheet.worksheet('Properties Delete')
def run_sample():
   index =2
   data =''
    
   while True:
        
        cell = f"A{index}"
        cellStatus = f"B{index}"
        
        tempData=sheet_instance.get(cell)
        tempStatus=sheet_instance.get(cellStatus)
       
        
        if len(tempData)> 0:
            
            if len(tempStatus) > 0:
                tempStatus=tempStatus[0][0]
            
            if tempStatus != "Deleted":
                dataCell=f"A{index}:h{index}"
                
                data =sheet_instance.get(dataCell)
                
                propertyId = data[0][0]               
                print(propertyId)
                
                sheet_instance.update(cellStatus,'Deleted')                
                property_id = propertyId
                delete_property(property_id)


def delete_property(property_id):
    """Deletes the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    client.delete_property(name=f"properties/{property_id}")
    print("Property deleted")


# [END analyticsadmin_properties_delete]


if __name__ == "__main__":
    run_sample()