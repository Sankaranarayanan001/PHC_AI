from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time

#Asking whether this is a follow up visit
visit = input("Is this a follow up visit\t: ")

#This Number can be Extracted from aadhar
Phone_Number = input("Enter your Mobile Number\t: ")

#List of symptoms
confirmed_symptom = ["Injury"]

#Opening Chrome Browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#Opening the e-sanjeevani sign-in website
driver.get("https://esanjeevani.mohfw.gov.in/#/patient/signin")
driver.maximize_window()

#Writing the phone number in the Text box
search = driver.find_element(By.CLASS_NAME,"mat-input-element")
search.send_keys(Phone_Number)

time.sleep(3)

#Clicking on Get OTP button
otp = driver.find_element(By.LINK_TEXT,"Get OTP")
otp.click()

time.sleep(5)

#Clicking OTP bar
#here AI will say "enter the received OTP from your phone"
search = driver.find_element(By.XPATH,'//*[@id="mat-input-2"]').click()

time.sleep(25)

#Clicking Login Button
button = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
button.click()

time.sleep(5)

#Clicking Consult Now Button
consult = driver.find_element(By.CLASS_NAME,"btn")
consult.click()


time.sleep(5)

#Follow up visit 
if visit == 'y':
    driver.find_element(By.CLASS_NAME,"mat-radio-inner-circle").click()
    time.sleep(5)

#Entering into iframe
iframe = driver.find_element(By.TAG_NAME,"iframe")
driver.switch_to.frame(iframe)
driver.implicitly_wait(30)

#Ticking off the symptoms
for symptom in confirmed_symptom:
    search_bar = driver.find_element(By.CLASS_NAME,"searchText_input")
    search_bar.send_keys(symptom)
    sym = driver.find_element(By.XPATH,"//span[1][text()='%s']"%symptom)
    time.sleep(1)
    sym.click()
    time.sleep(1)
    search_bar.clear()
    time.sleep(1)

time.sleep(5)  


#Clicking Save and Next Button
btn = driver.find_element(By.CLASS_NAME,("saveBtn"))
driver.execute_script("arguments[0].click();", btn)


time.sleep(2)

condition = True
i = 3
while condition==True:
    try:
        #Next Question
        print(driver.find_element(By.XPATH,"//*[@id='chatArea']/div[1]/div[%d]/div/p"%i).text)
        #Options
        try:
            #text input
            options = driver.find_elements(By.XPATH,'//*[@id="chatArea"]/div[2]/div/div/span')
            if options == []:
                #Image Input
                options = driver.find_elements(By.XPATH,"//*[@id='chatArea']/div[2]/div[1]/div/div[2]/p")
        except:
            print("Element Not Found")
        finally:
            pass
        for opt in options:
            #Printing Option Can be later turned into speech
            print(opt.text)
        time.sleep(2)
        reason = True
        while (reason == True):
            #Enter Options Later can Be changed to voice input
            #Options need to be exact and are case sensitive
            ip = input("Enter your option : ")
            try:
                #Clicking Text Options 
                driver.find_element(By.XPATH,"//span[1][text()='%s']"%ip).click()
            except:
                #Clicking Img Options
                driver.find_element(By.XPATH,"//p[text()='%s']"%ip).click()
            finally:
                pass
            #For Multiple Selection options only if Only One options is selectable give n as input
            ip1 = input("Any Other Reason (y/n):")
            if(ip1 == 'y'):
                pass
            else:
                reason = False
        try:
            #Clicking Save and Next Button
            btn = driver.find_element(By.CLASS_NAME,("saveBtn"))
            driver.execute_script("arguments[0].click();", btn)
        except:
            pass
        finally:
            print("\n\nNext Question")
        i += 2
        time.sleep(2)
    except:
        condition = False
        print("Questions Finished pls wait")
    finally:
        pass


print("\n\n\nEOP")