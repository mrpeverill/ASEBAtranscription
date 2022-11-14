import datetime
import warnings
import pprint
import uuid

def asebadictformat(mapping,cbcldat,ysrdat=None):
    # print("cbclisportstimea is %s" % int(cbcldat['cbclisportstimea']))
    # print("sportstimea is %s" % arithcode(-1,'cbclisportstimea',cbcldat))
    ppf = pprint.PrettyPrinter(indent=4)
    
    #ppf.pprint(mapping['3020']['SourceField'])
    #ppf.pprint(arithcode(-1,'cbclfuisportsabilitya',cbcldat))
    
    #ppf.pprint(mapping[[key for key,value in mapping.items() if key.startswith("3")]])
    #ppf.pprint([getmappings(i,ysrdat,mapping) for i in mapping if i[:1]=="5"])

    recordid=getmappings(1001,cbcldat,mapping)['Value']
    age=getmappings(3005,cbcldat,mapping)['Value']
    gender=getmappings(3004,cbcldat,mapping)['Value']
    genderstring=genderrecode(gender,recordid)
    
    try:
        if int(age) < 6 or int(age) > 18:
            warnings.warn("Record %s age out of range" % recordid,UserWarning)
    except TypeError:
        warnings.warn("Record %s age improperly formatted" % recordid,UserWarning)
    except ValueError:
        warnings.warn("Record %s age missing or misformatted" % recordid,UserWarning)
    
    formslist=[cbcldictformat(cbcldat,mapping)]
    if ysrdat!=None:
        #print('appending ysr data')
        formslist.insert(0,ysrdictformat(ysrdat,mapping,gender,age))
    #pp.pprint(ysrdictformat(ysrdat))
    
    
    dob=getmappings(3009,cbcldat,mapping)['Value']
    dict={'DateOfBirth': dob+'T00:00:00',
        'Ethnicity': '',
        'Forms': formslist,
        'Gender': genderstring,
        'PersonInformation': {   'ContactInfo': {   'Address': {   'City': '',
                                                                   'Country': '',
                                                                   'PostalCode': '',
                                                                   'StateProvince': '',
                                                                   'Street1': '',
                                                                   'Street2': ''},
                                                    'Email': '',
                                                    'HomePhone': '',
                                                    'MobilePhone': '',
                                                    'WorkPhone': ''},
                                 'First': '',
                                 'IdentificationCode': recordid,
                                 'Last': '',
                                 'Middle': '',
                                 'NickName': '',
                                 'Title': ''}}
    
    return dict;

def ysrdictformat(dat,mapping,gender,age):
    #Answerslist=[getmappings(i) for i in mapping if ]
    dict = {   'Agency': '',
                         'AsebaDataId': str(uuid.uuid4()),
                         'Clinician': '',
                         'ContactEmail': '',
                         'ContactName': '',
                         'ContactPhone': '',
                         'EvaluationId': '',
                         'FormInstrument': {   'Answers': [{"Comment": "", "QuestionId": 5004, "Value": gender},
                                                           {"Comment": "", "QuestionId": 5005, "Value": age}] +
                                               [getmappings(i,dat,mapping) for i in mapping if i[:1]=="5"],# All the YSR id's start with 5
                         "Id": "69e3fe20-0206-4a5b-a62e-abcaed7aab79"}, 
                         'Relationship': 'Self',
                         'School': '',
                         'Society': {'Id': '622adb6d-dede-48e3-ae34-e80cdeb37ed8'},
                         'Status': 'Key-Entered',
                         'UserDefined1': '',
                         'UserDefined2': '',
                         'UserDefinedText1': '',
                         'UserDefinedText2': ''}
    dict['FormInstrument']['Answers']=removeEmptyValues(dict['FormInstrument']['Answers'])
    return dict;

def cbcldictformat(dat,mapping):
    dict={   'Agency': '',
                         'AsebaDataId': '5835f083-d874-2853-971b-d8b591bd6874',
                         'Clinician': '',
                         'ContactEmail': '',
                         'ContactName': '',
                         'ContactPhone': '',
                         'EvaluationId': '',
                         'FormInstrument': {   'Answers': [getmappings(i,dat,mapping) for i in mapping if i[:1]=="3"], 
                                               'Id': '07855877-88cf-458a-8d4e-93be0af21fa6'},
                         'Relationship': '', #currently not coded
                         'School': '',
                         'Society': {'Id': '622adb6d-dede-48e3-ae34-e80cdeb37ed8'},
                         'Status': 'Key-Entered',
                         'UserDefined1': '',
                         'UserDefined2': '',
                         'UserDefinedText1': '',
                         'UserDefinedText2': ''}
    dict['FormInstrument']['Answers']=removeEmptyValues(dict['FormInstrument']['Answers'])
    return dict;
    
def genderrecode(gender,record):
    if gender=='1':
        return 'M'
    elif gender=='2':
        return 'F'
    else:
        warnings.warn("Record %s gender unset in CBCL, setting to 'U'" % record,UserWarning)
        return 'U'

def arithcode(y,string,dat):
    try:
        x=str(int(dat[string])+y)
    except ValueError:
        x=''
    except TypeError:
        x=''
    except KeyError:
        x=''
    return x

def removeEmptyValues(listarg):
    return [item for item in listarg if item['Value']!='' and item['Value']!='999' and item['Value']!='NA']
    

def getmappings(id,dat,mapping):
    comment=mapping[str(id)]['SourceCommentField']
    value=mapping[str(id)]['SourceField']

    if comment:
        commentv=eval(comment)
    else:
        commentv=comment
        
    if value:
        valuev=eval(value)
    else:
        valuev=value
    #print(value)
    #print(valuev)
    return({'Comment': commentv, 'QuestionId':int(id), 'Value': valuev})
    
def sdlabrelcalc(string,dat):
    if dat[string+'relation___1']=="1":
        return '1'
    elif dat[string+'relation___2']=="1":
        return '2'
    elif dat[string+'relation___3']=="1":
        return '3'
    elif dat[string+'relation___4']=="1":
        return '4'
    elif dat[string+'relation___5']=="1":
        return '5'
    elif dat[string+'relation___6']=="1":
        return '6'
    else:
        return ''
        
def sdlabsibcode(string,dat):
    try:
        x=str(int(dat[string])-1)
    except ValueError:
        x=''
    except TypeError:
        x=''
    except KeyError:
        x=''
    if x=="-1":
        return 3
    elif x=="998":
        return ''
    else:
        return x
