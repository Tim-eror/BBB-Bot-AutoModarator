import configparser
from playsound import playsound
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def send_chat_message(text):
    # identify the bar to enter chat messages
    message_bar = driver.find_element(By.ID,"message-input")
    # Write  message
    message_bar.send_keys(text)
    message_bar.send_keys(Keys.ENTER)
    return len(text)


def execute_command(pcommand: str):
    message_len = 0
    if pcommand.startswith("/help"):
        message_len = send_chat_message("""
        This is the help:
        - Type /help to get help (english)
        - Tippe /hilfe um hilfe zu erhalten (Deutsch)
        - Type /frage to send a question-ping to the tutor. You can also start your question with /frage to mark your message as a question
        - Type /mic to send a your-mic-is-off-ping to the tutor
        """)

    if pcommand.startswith("/hilfe"):
        message_len = send_chat_message("""
        Das ist die Hilfe:
        - Type /help to get help (english)
        - Tippe /hilfe um hilfe zu erhalten (Deutsch)
        - Tippe /frage um dem Tutor einen Frage-Ping zu senden, fals er dich nicht bemerkt. Du kanst deine Frage auch mit /frage beginnen um diese als Frage zu markieren
        - Tippe /mic wenn der Tutor vergessen hat sein Micro einzuschlaten, um ihn darauf hinzuweisen 
        """)

    if pcommand.startswith("/frage"):
        playsound("bell-1.wav")
        print("[!] a student got a question: {pcommand}")

    if pcommand.startswith("/mic"):
        playsound("bell-2.wav")
        print("[!] you forgott your mic !")
        # TODO add Popup Window

    if pcommand == "/hydro":
        message_len = send_chat_message("stay hydryded")

    if pcommand == "/answered":
        msg = "--- all questions before this message are marked as answered ---"
        message_len = send_chat_message(msg)
        print(msg)
    
    if "Folien" in pcommand and "haben" in pcommand or pcommand == "/folien":
        message_len = send_chat_message("Auszüge der Folien werden im Anschluss an des Tutoriums auf sciebo hochgeladen. Link siehe Geteilte Notizen")

    return message_len

def findMessages(driver: webdriver.Firefox):
    msg = driver.find_elements(By.XPATH,'//*[@data-test="chatUserMessageText"]')
    return msg

if __name__ == '__main__':

    # loading config
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot_name = config["DEFAULT"]["Bot_Name"]
    welcome_message = config["DEFAULT"]["Welcome_Message"]
    tick_time = int(config["DEFAULT"]["Tick_Time"])
    room_name = config["LOGIN-CREDENTIALS"]["Room_Name"]
    sever_name = config["LOGIN-CREDENTIALS"]["Sever_Name"]

    # testing audios
    if config["SETTINGS"]["Play_Audio_Test"] == "True":
        print("[!] testing audio - please turn up the volume to preferred point")
        playsound("bell-3.wav")

    # start driver
    print("[-] starting driver")
    driver = webdriver.Firefox()

    # navigate to the url
    driver.get("https://bbb.informatik.uni-bonn.de/b/"+room_name)
    print("[-] loggin in")
    # identify the bar to enter name
    ele = driver.find_element(By.ID,"_b_"+room_name+"_join_name")
    # Write login name
    ele.send_keys(bot_name)
    ele.send_keys(Keys.ENTER)  # Enter (send)

    time.sleep(5)  # Need expliced waiting

    # send welcome message
    
    if welcome_message != "":
        print("[-] sending welcome")
        send_chat_message(welcome_message)

    print("[-] Escaping Popup")
    # Escape Popup *not working*
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("[*] Up and running...")
    # identify chat and start listing
    last_msg = findMessages(driver)[-1]
    while True:
        messages = findMessages(driver)
        
        #print(f"[-] m: {len(messages)}  -1: {messages[-1].text}")
        
        i = 1
        msg = messages[-i]
        while msg != last_msg:
            if i<len(messages):
                i += 1
            else:
                break

            command = str(msg.text)
            #print(f"[-] Message {i}: " + command)
            if command.startswith("/"):
                execute_command(command.lower())
                #print("[-] Command: " + command)
            msg = messages[-i]
        last_msg = findMessages(driver)[-1]
        time.sleep(tick_time)




