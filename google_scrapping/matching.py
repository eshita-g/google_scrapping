import pandas as pd         #importing modules
import ast
import json
import re
df1 = pd.read_csv("/home/thebrain-eshita/Documents/g2.csv", dtype='object')    #uploading csv file into a dataframe
df2 = pd.read_csv("/home/thebrain-eshita/Documents/target_study.txt", delimiter='\t')

def name_matching():
    df1_name = []                      #list for storing names of df1
    df2_name = []                      #list for storing names of df2
    stopwords = ["of", "coaching", "the", "classes", "center", "best", "academy", "education", "institute", "tutorials","for", "pvt", "ltd","tutorial"]
    for name in df1['name']:
        name = name.lower()
        name1 =re.findall('\w+',name)                     #tokenizing names of df1
        name1=[x for x in name1 if x not in stopwords]      #removing stopwords from names of df1
        df1_name.append(name1)                               #appending to a list

    for name in df2['name']:
        name =name.lower()                                 #converting into lower case
        name2=re.findall('\w+',name)                       #tokenizing names of df2
        name2 =[x for x in name2 if x not in stopwords]     #removing stopwords from names of df2
        df2_name.append(name2)

    nm1, nm2 = string_matching(df1_name, df2_name)           #calling string matching
    final_nm = {'nm1': nm1, 'nm2': nm2}
    return final_nm

def address_matching():
    df1_address = []                                           #list for storing address of df1
    df2_address = []                                           #list for storing address of df2
    stopwords1 =["nagar","behind","indore","madhya pradesh","opposite","road"]  #stopwords for address
    for add in range(len(df1['address'])):
        a = ast.literal_eval(df1['address'][add])['line1']
        b = ast.literal_eval(df1['address'][add])['line2']
        c = a + b                                                 #combining address of line1 and line2
        c = c.lower()
        address1 = re.findall('\w+',c)                            #tokenizing address
        address1 = [x for x in address1 if x not in stopwords1]
        df1_address.append(address1)                                 #appending address of df1

    for add in range(len(df2['address'])):
        a = ast.literal_eval(df2['address'][add])['address line 1']
        b = ast.literal_eval(df2['address'][add])['address line 2']
        c = a + b                                                    #combining address of line1 and line2
        c = c.lower()
        address2 = re.findall('\w+',c)                               #tokenizing address of df2
        address2 = [x for x in address2 if x not in stopwords1]
        df2_address.append(address2)
    add1, add2 = string_matching(df1_address, df2_address)             #calling string matching
    final_add = {'add1': add1, 'add2': add2}                           #adding into dictionary
    return final_add


def phone_matching():
    df1_phone = []                                                   #list for storing phone no  of df1
    df2_phone = []                                                   # list for storing phone no of df2

    for ph in df1['contact_no']:
        if (type(ph)=='str'):
          df1_phone.append(ph)                                      #appending to list1
        else:
            df1_phone.append(0)
    for ph in range(len(df2['phones'])):
        a = ast.literal_eval(df2['phones'][ph])['phone']
        df2_phone.append(a)                                        #appending to list2


    phn1, phn2 = string_matching(df1_phone, df2_phone)
    final_phn = {'phn1': phn1, 'phn2': phn2}
    return final_phn


def string_matching(df1_list,df2_list):
    list1 = []
    list2 = []
    for i in df1_list:                                                    #iterating through list1
        for j in df2_list:                                                # iterating through list2
            count = 0
            try:
               if i is not None and j is not None and len(i)!=0 and len(j)!=0:
                   for x in i:
                       for y in j:
                          if x.strip()==y.strip():
                              count =count + 1
               list1.append((count/len(i))*100)                #appending matching percenatge to list1
               list2.append((count/len(j))*100)                #appending matching percentage to list2
            except:
                list1.append(0.0)
                list2.append(0.0)
    return list1,list2

def prepare_id():
    nm = name_matching()                                       #calling name matching function
    phn = phone_matching()                                     #calling phone matching
    add = address_matching()                                   #calling address matching function
    final = {'nm1': nm['nm1'], 'nm2': nm['nm2'],
             'phn1': phn['phn1'], 'phn2': phn['phn2'],
             'add1': add['add1'], 'add2': add['add2']}
    df_final = pd.DataFrame.from_dict(final,orient='index')
    df_final.to_csv("/home/thebrain-eshita/Documents/eshita_train.csv",index=False) #writing data to csv file


def write_data(data):
    name1 = []
    name2 = []
    phone1 = []
    phone2 = []
    address1 = []
    address2 = []
    for x in data:
        print(x)
        name1.append(x[0])
        name2.append(x[1])
        phone1.append(x[2])
        phone2.append(x[3])
        address1.append(x[4])
        address2.append(x[5])
    data = pd.DataFrame({'n1': name1, 'n2': name2, 'p1': phone1, 'p2': phone2, 'a1': address1, 'a2': address2})
    data.to_csv("/home/thebrain-eshita/Documents/eshita_train.csv", sep=',', index=False)

# calling function
prepare_id()
