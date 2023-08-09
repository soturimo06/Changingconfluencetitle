import requests
import json
import logging
import base64

#disable warnings
requests.packages.urllib3.disable_warnings()


#rest api server url
confluenceServerURL = "url"

#service account user name
username = "user"

#service account password
password = "pass"


#page information
spaceKey = "[spacekey]"
pageId="[pageId]"



#Authentication Module
def authentication(username,password):
    #SMSESSSION url
    smSessionURL = "smSessionURL"
    #smSessionHeaders
    smSessionHeaders = {'Accept' : 'application/json'}
    try:
        response=requests.get(smSessionURL,verify=False, headers=smSessionHeaders, auth=(username, password))
        print('Getting SMSESSION from URL')
        if response.status_code == 200:
            smSessionJson = response.json()
            cookie = smSessionJson[u'SMSESSION']           
        else:
            print("Error while obtaining SMSESSION %s ", response.status_code)
            print(response.text)
    except Exception as e:
        print("Error while updating page with id %s due to %s",pageId,str(e))
    return(cookie)
#Getting Page Title and version
def getpage(username,password,confluenceServerURL,spaceKey):
    PageTitle = "Test Passwords"
    #getPageURL="/rest/api/content?title="+PageTitle+"&spaceKey="+spaceKey+"&expand=history"
    getPageURL="/rest/api/content/"+pageId+"?expand=body.storage,version"
    cookie = authentication(username,password)
    headers = {'Cookie' : 'SMSESSION=%s' % cookie}
    try:
        #get SMSESSION cookie
        #print(confluenceServerURL)
        #print(getPageURL)
        response = requests.get(confluenceServerURL+getPageURL, verify=False, headers=headers)
        jsonvalue = response.json()
        PageTitle = jsonvalue['title']
        version = jsonvalue['version']['number']
        updateconfluence(cookie,confluenceServerURL,PageTitle,version)
    except Exception as e:
        print("Error while getting page due to %s",str(e))
#Updating page
def updateconfluence(cookie,confluenceServerURL,PageTitle,version):
    updatePageURL = "/rest/api/content/"+pageId
    if PageTitle == "Test Passwords":
        updatedPageTitle = "Passwords"
    else:
        updatedPageTitle = "Test Passwords"
    headers = {'Cookie' : 'SMSESSION=%s' % cookie,'Content-Type': 'application/json'}
    version = version + 1
    jsonPayload = {"id":pageId,"type":"page","title":updatedPageTitle,"space":{"key":spaceKey},"version":{"number":version}}
    try:
        response = requests.put(confluenceServerURL+updatePageURL,verify=False,data=json.dumps(jsonPayload),headers=headers)
        print(response.status_code)
    except Exception as e:
        print("Error while getting page due to %s",str(e))  
  
getpage(username,password,confluenceServerURL,spaceKey)