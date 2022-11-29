import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#Define empty dictionary for later
dict = {}
dict['title245'] = []
dict['oclcnumber'] = []
dict['gponumber'] = []
dict['purl'] = []
dict['gpoid'] = []
dict['956data'] = []
dict['nzmms'] = []

#Set up default things for base URL and bib API key
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'
headers = {"Accept": "application/xml"}

#Bibs read-only API key
bibapi = 'INSERT ALMA BIBS API KEY HERE'

#Pull in Excel file with MMS IDs for lookup
inputname = input('MMSID Input Filename without extension: ')
source = pd.read_excel(inputname + '.xlsx')

#Take the MMS ID Column from the input data and make that a list in Python as Strings (so they don't get cut off for being long numbers)
mmsids=source['MMS ID'].astype(str)

#Optional: Check that MMS IDs imported correctly
print(mmsids)


#Loop through the MMS IDs, for each, extract information from specific fields in the record (if present) and save them to the master Dictionary

for i, mms in enumerate(mmsids, 0):  

    mms = mmsids[i]
    
    #Add MMS ID to Dictionary
    dict['nzmms'].append(mms)

    #Query the API using the parameters up top 
    r = requests.get(alma_base+'/bibs/' + mms +'?apikey=' + bibapi, headers=headers)
    
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(r.content, "xml")

    #Look for the OCLC number in the 035 and adds to Dictionary
    try:
        f035 = soup.findAll("datafield", attrs={"tag": '035'})
        #Looks for match to the OCoLC number in that exact format
        teststring = str(f035)
        oclcsearch = re.compile(r'\(OCoLC\)\d+')
        oclctemp = oclcsearch.search(teststring)
        if oclctemp is not None:
            oclc= oclctemp.group()
        else:
            oclc= "NA"
        dict['oclcnumber'].append(oclc)
    except IndexError:
        oclc = "NA"    
        dict['oclcnumber'].append(oclc)
    print(oclc)
    
    #Looks GPO Identifier in the 035 and adds to Dictionary
    try:
        f035 = soup.findAll("datafield", attrs={"tag": '035'})
        teststring = str(f035)
        gposearch = re.compile(r'\(GPO\)\d+')
        gpotemp = gposearch.search(teststring)
        if gpotemp is not None:
            gpo= gpotemp.group()
        else:
            gpo= "NA"
        dict['gponumber'].append(gpo)
    except IndexError:
        gpo = "NA"    
        dict['gponumber'].append(gpo)
    print(gpo)
    
    #Grabs Title and adds to Dictionary
    try:
        f245 = soup.findAll("datafield", attrs={"tag": '245'})
        title = f245[0].getText()
        dict['title245'].append(title)
    except IndexError:
        title = "NA"    
        dict['title245'].append(title)
    print(title)
        
    #Looks for PURL in 856 in record and adds to Dictionary in full
    try:
        f856 = soup.findAll("datafield", attrs={"tag": '856'})
        recurl = f856[0].getText()
        dict['purl'].append(recurl)

        #Also adds just the numbers from the end of the PURL to the Dictionary in a separate field
        purlsearch = re.compile(r'([^\/]+)\/?$')
        purltemp = purlsearch.search(recurl)
        gpoidtemp = purltemp.group()
        dict['gpoid'].append(gpoidtemp)

    except IndexError:
        recurl = "NA"    
        gpoidtemp = 'NA'
        dict['purl'].append(recurl)
        dict['gpoid'].append(gpoidtemp)
    print(recurl)
    print(gpoidtemp)

    #Adds from 956 to Dictionary
    try:
        f956 = soup.findAll("datafield", attrs={"tag": '956'})
        source = f956[0].getText()
        dict['956data'].append(source)
    except IndexError:
        source = "NA"    
        dict['956data'].append(source)
    print(source)
            

#Converts Dictionary to Dataframe
df = pd.DataFrame(dict)

#Dataframe Cleanup
#Removes (OCoLC) prefix from OCLC number
df['oclcnumber'] = df['oclcnumber'].str.replace("\(OCoLC\)","", regex=True)

#Removes (GPO) prefix from GPO number
df['gponumber'] = df['gponumber'].str.replace("\(GPO\)","", regex=True)


#Save Dataframe to Excel
df.to_excel('recordbatch.xlsx')
