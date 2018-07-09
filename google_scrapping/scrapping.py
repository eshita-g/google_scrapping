from selenium import webdriver
import re
from time import sleep
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
# creating database
db = client["coaching"]
# creating collection
collection2 =db["google"]
# creating driver
driver = webdriver.Firefox(executable_path="/home/thebrain-eshita/Documents/geckodriver")
driver.get("https://www.google.com/")
sleep(3)
a=driver.find_element_by_name("q")
a.send_keys("coaching classes in indore")           #submitting keyword
a.submit()
sleep(4)
b=driver.find_element_by_class_name("DLOTif")
b.click()


def scrapping():
    detail = {}
    detail['address'] = {}
    detail['ratings'] = {}
    detail['reviews'] = []
    detail['websites'] = []
    detail['courses'] = []
    detail['tags'] = []
    detail['source'] = {}
    links =len(driver.find_elements_by_class_name("dbg0pd"))  #assigning links of coachings
    sleep(5)
    for i in range(links):                                   #iteration of all coaching link on one page
       c = driver.find_elements_by_class_name("dbg0pd")[i]
       sleep(3)
       detail['name'] = str(c.text)                            #assigning name of the coaching
       driver.find_elements_by_class_name("dbg0pd")[i].click()    #clicking on the link of the coaching
       sleep(7)
       s_url = driver.current_url
       detail['source']['url'] = str(s_url)                           #assigning current url
       detail['source']['name'] = str("www.google.com")
       details=driver.find_element_by_xpath("//div/div/span[2][@class='LrzXr']")
       p = details.text
       sleep(3)
       detail['address']['city'] = 'Indore'
       list1 = re.findall('\d+',p)                                               #finding numerics in address using re
       for pin in list1:
             if len(pin)==6:
                 detail["address"]["pincode"] = str(pin)                          #assigning pincode
                 p1=re.sub(pin,'',p)
             else:
                  p1 = p
                  detail["address"]["pincode"] = " "
       p2 = re.sub("Indore|Madhya Pradesh",'',p1)
       add = p2.split(',')                                                      #splitting address
       t = 0
       line1 = ""
       line2 = ""
       for line in add[:-2]:
          if(t<=1):
            line1 = line1 + " " + line
          else:
            line2 = line2 + " " + line
          t = t + 1
       line1 = line1.strip(",")
       line2 = line2.strip(",")
       detail["address"]["line1"] = str(line1)                   #assigning line 1 address
       detail["address"]["line2"] = str(line2)                   # assigning line 2 address
       detail["address"]["state"] = "Madhya Pradesh"
       detail['address']['country'] = "India"
       detail["address"]["longitude"] = ""
       detail['address']['latitude'] = ""
       detail["contact_person"] = []
       detail['direction'] = []
       direc = {}
       direc['source'] = "google.com"
       sleep(5)
       try:
          phone=driver.find_element_by_xpath("//div/div/span[2][@class='LrzXr zdqRlf kno-fv']")  #finding phoneno element
          sleep(4)
          phone1 = phone.text
          phone1 = ''.join(phone1.split())                                           #splitting
          detail["contact_no"] = str(phone1)                                         #assigning of phone no
       except:
           detail["contact_no"] = ''
       sleep(5)
       try:
         rate =driver.find_element_by_xpath("//div/div/span[1][@class='rtng']")
         detail["ratings"]["rating"] = str(rate.text)                             #assigning rating
       except:
           detail["ratings"]["rating"] = ""
       detail["ratings"]["source"] = str("google.com")
       sleep(5)
       web = len(driver.find_elements_by_xpath("//div/div[2][@class='hZCf6e']/a"))      #clicking on website and direction
       sleep(4)
       if(web==0):                                                                        #there is only direction
             detail['websites'] = ""
             driver.find_element_by_xpath("//div/div[2]/div[@class='hZCf6e']/a").click()    #clicking on direction
             sleep(6)
             drxn = driver.current_url
             sleep(4)
             direc['direction'] = drxn
             driver.back()
             sleep(6)
       else:                                                                 #there is both direction and website
             driver.find_element_by_xpath("//div/div[2]/div[1][@class='hZCf6e']/a").click()    # clicking on website
             sleep(6)
             website = driver.current_url
             sleep(3)
             detail['websites'] = website                                                       #assigning address
             driver.back()
             sleep(5)
             driver.find_element_by_xpath("//div[2]/div[2][@class='hZCf6e']/a").click()       #clicking on direction
             sleep(5)
             drxn=driver.current_url
             sleep(5)
             direc['direction'] = drxn                                                     #assigning direction
             driver.back()
             sleep(5)
       detail['direction'].append(direc)

       print(detail)
       collection2.insert(detail.copy())                                  #inserting dictionary to a mongodb collection





def nextpage():
      for next in range(20):                                               #iterating through next pages
         scrapping()
         next = driver.find_element_by_xpath("//tr/td[12]/a/span[1][@class='csb ch']")
         next.click()                                                                 #clicking the link of next page



if __name__== "__main__":
    nextpage()

