import gspread
from oauth2client.service_account import ServiceAccountCredentials


f=open("email_body.txt","r")
f.seek(0)
s=f.read()
n=s.split()
k= []
sublist = []
for i in n:
    if i == "==================================================":
        if sublist:  # Avoid adding empty lists
            k.append(sublist)
            sublist = []
    else:
        sublist.append(i)

if sublist:  # Add the last sublist if it's not empty
    k.append(sublist)
final=[]
for i in k:
    del i [19:]
    final.append(i)
d={}
a=[]
for i in range(len(final)):
    if final!=[]:
        if final[i]:
            d[final[i][0]]=final[i][1]
            d["Time"]=final[i][2]
            d[final[i][3]]=final[i][4]
            d[final[i][5]]=final[i][6]
            d[final[i][7]]=final[i][8]
            d[final[i][9]]=final[i][10]
            d[final[i][11]]=final[i][12]
            d[final[i][13]]=final[i][14]
            d[final[i][15]]=final[i][16]
            d[final[i][17]]=final[i][18]
            a.append(d)
            d={}
    else:
        print("The list is empty")
print(a)


# Configuration
JSON_CREDENTIALS = 'credentials.json'  # Replace with your JSON credentials file
SHEET_NAME = 'Email Data'       # Replace with your sheet name
WORKSHEET_NAME = 'Sheet1'                   # Replace if different worksheet

# Sample data
data = a

def upload_to_google_sheets():
    # Set up credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_CREDENTIALS, scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

    # Prepare data for upload
    headers = list(data[0].keys())
    rows = [headers]
    
    for item in data:
        rows.append([str(value) for value in item.values()])

    # Clear existing content and update with new data
    sheet.clear()
    sheet.update('A1', rows)

    print(f'Successfully uploaded {len(data)} rows to {SHEET_NAME}')

if __name__ == '__main__':
    upload_to_google_sheets()