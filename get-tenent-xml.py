import requests
import xml.dom.minidom

# We need to import the JSON library just to handle our request to the APIC for login
import json

#We need to login into apic and get token for gathering information about tenants
# We'll need to disable certificate warnings
requests.packages.urllib3.disable_warnings()

#we need to have body of data consisting usrname and password to gather cookies from apic
encoded_body = json.dumps({
    "aaaUser":{
        "attributes": {
            "name": "admin",
            "pwd" : "ciscopsdt"
        }
    }
})
api_url = "https://sandboxapicdc.cisco.com/api"
# api_url = input('Pls provice of APIC name.....')
# url = "https://sandboxapicdc.cisco.com/api/aaaLogin.json"
#now let make the requests and store the data 
resp = requests.post(api_url+"/aaaLogin.json", data=encoded_body, verify=False)

#this store recieved  "APIC-cookie" from the login as a value and used in subsuquest rest api calls
headers = {"Cookie":"APIC-cookie="+ resp.cookies["APIC-cookie"] }
tenants = requests.get(api_url+"/node/class/fvTenant.xml?rsp-subtree-include=health,faults", headers=headers, verify=False)
# print(tenants.text) # ouput is xml big data
#Now use dom to clean up xml from its completely  row data format
dom = xml.dom.minidom.parseString(tenants.text)
xml = dom.toprettyxml()
print(xml)

#Now we want to print resulting xml in that we filter out tenant and health score data
tenant_object = dom.firstChild
if tenant_object.hasChildNodes:
    tenant_element = tenant_object.firstChild
    while tenant_element is not None:
        if tenant_element.tagName == 'fvTenant':
            health_element = tenant_element.firstChild
            output = "Tenant:    " + tenant_element.getAttribute('name') + '\HealthScore:     ' + health_element.getAttribute('cur')
            print(output.expandtabs(40))
            tenant_element = tenant_element.nextSibling
