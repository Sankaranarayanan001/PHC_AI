from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from gtts import gTTS
import speech_recognition as sr
import playsound
import os

# Initialize counter for voice files
x = 0

def speak(mytext):
    global x
    myobj = gTTS(text=mytext, lang='en', slow=False)
    fname = f"voice{x}.mp3"
    myobj.save(fname)
    time.sleep(0.5)
    playsound.playsound(fname)
    time.sleep(0.5)
    try:
        os.remove(fname)
    except Exception as e:
        print(f"Could not delete {fname}: {e}")
    x += 1

# Greetings
speak("Greetings")
speak("Is this a follow-up visit?")

visit = input("Is this a follow-up visit (y/n): ")
Phone_Number = input("Enter your Mobile Number: ")
confirmed_symptom = ["Cough"]

# Launch browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://esanjeevani.mohfw.gov.in/#/patient/signin")
driver.maximize_window()

# Enter mobile number
search = driver.find_element(By.CLASS_NAME, "mat-input-element")
search.send_keys(Phone_Number)
time.sleep(3)

# Click Get OTP
otp = driver.find_element(By.LINK_TEXT, "Get OTP")
otp.click()
time.sleep(5)

# Prompt for OTP manually (wait 23s)
speak("Please enter the OTP received on your phone.")
driver.find_element(By.XPATH, '//*[@id="mat-input-2"]').click()
time.sleep(23)

# Click Login
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)

# Click Consult Now
driver.find_element(By.CLASS_NAME, "btn").click()
time.sleep(5)

# Handle follow-up visit
if visit.lower() == 'y':
    driver.find_element(By.CLASS_NAME, "mat-radio-inner-circle").click()
    time.sleep(5)

# Enter iframe for symptom selection
iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)
driver.implicitly_wait(30)

# Select symptoms
for symptom in confirmed_symptom:
    search_bar = driver.find_element(By.CLASS_NAME, "searchText_input")
    search_bar.send_keys(symptom)
    sym = driver.find_element(By.XPATH, f"//span[1][text()='{symptom}']")
    time.sleep(1)
    sym.click()
    search_bar.clear()
    time.sleep(1)

# Save and Next
time.sleep(5)
btn = driver.find_element(By.CLASS_NAME, "saveBtn")
driver.execute_script("arguments[0].click();", btn)

for _ in range(5):
    driver.find_element(By.TAG_NAME, "html").send_keys(Keys.ARROW_DOWN)
time.sleep(2)

# Loop through chat-based diagnosis
condition = True
i = 3
while condition:
    try:
        question = driver.find_element(By.XPATH, f"//*[@id='chatArea']/div[1]/div[{i}]/div/p").text
        print(question)
        speak(question)

        try:
            options = driver.find_elements(By.XPATH, '//*[@id="chatArea"]/div[2]/div/div/span')
            if not options:
                options = driver.find_elements(By.XPATH, "//*[@id='chatArea']/div[2]/div[1]/div/div[2]/p")
            if not options:
                options = driver.find_elements(By.XPATH, '//*[@id="chatArea"]/div[2]/div[2]/div/div/span')
        except:
            options = []

        for opt in options:
            print(opt.text)
            speak(opt.text)

        # Handle user input
        reason = True
        while reason:
            ip = input("Enter your option: ")
            try:
                the_ele = driver.find_element(By.XPATH, '//*[@id="chatArea"]/div[2]/div[1]')
                class_names = the_ele.get_attribute('class').split()
                try:
                    driver.find_element(By.XPATH, f"//span[text()='{ip}']").click()
                except:
                    try:
                        driver.find_element(By.XPATH, f"//p[text()='{ip}']").click()
                    except:
                        driver.find_element(By.XPATH, '//*[@id="chatArea"]/div[2]/div[2]/div/div')

                if "multiSelectOpt" in class_names:
                    speak("Any other reason from the above options?")
                    ip1 = input("Any other reason (y/n): ")
                    if ip1.lower() != 'y':
                        reason = False
                else:
                    reason = False
            except:
                print("Option not recognized. Try again.")

        try:
            btn = driver.find_element(By.CLASS_NAME, "saveBtn")
            driver.execute_script("arguments[0].click();", btn)
        except:
            pass
        finally:
            print("Next question...")
            speak("Next question. Please wait.")
        i += 2
        time.sleep(2)
    except:
        condition = False
        print("All questions completed.")
        speak("AI consultation completed. Generating token.")
        break

print("\n\n\nEnd of Process")
time.sleep(30)
