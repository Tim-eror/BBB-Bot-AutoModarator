import configparser
import winsound  # TODO use sound lib that is linux compatible
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def send_chat_message(text):
    # identify the bar to enter chat messages
    message_bar = driver.find_element_by_id("message-input")
    # Write  message
    message_bar.send_keys(text)
    message_bar.send_keys(Keys.ENTER)
    return len(text)


def execute_command(pcommand):
    message_len = 0
    if pcommand == "/help":
        message_len = send_chat_message("""
        This is the help:
        - Type /help to get help (english)
        - Tippe /help um hilfe zu erhalten (Deutsch)
        - Type /frage to send a question-ping to the tutor
        - Type /mic to send a your-mic-is-off-ping to the tutor
        """)

    if pcommand == "/hilfe":
        message_len = send_chat_message("""
        Das ist die Hilfe:
        - Tippe /help um hilfe zu erhalten (Deutshc)
        - Type /hilfe to get help (german) *in work*
        - Tippe /frage um dem Tutor einen Frage-Ping zu senden, fals er dich nicht bemerkt
        - Tippe /mic wenn der Tutor vergessen hat sein Micro einzuschlaten, um ihn darauf hinzuweisen 
        """)

    if pcommand == "/frage":
        winsound.MessageBeep()
        print("a student got a question")

    if pcommand == "/frage":
        winsound.MessageBeep()
        print("you forgott your mic")
        # TODO add Popup Window

    return message_len


if __name__ == '__main__':

    # loading config
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot_name = config["DEFAULT"]["Bot_Name"]
    welcome_message = config["DEFAULT"]["Welcome_Message"]
    tick_time = int(config["DEFAULT"]["Tick_Time"])
    room_name = config["LOGIN-CREDENTIALS"]["Room_Name"]

    # testing audios
    if config["SETTINGS"]["Play_Audio_Test"] == "True":
        print("testing audio - please turn up the volume to preferred point")
        winsound.Beep(440, 3000)

    # start driver
    print("starting driver")
    driver = webdriver.Firefox(executable_path=r'D:\Programme\geckodriver-v0.29.1-win64\geckodriver.exe')

    # navigate to the url
    driver.get("https://bbb.informatik.uni-bonn.de/b/"+room_name)

    # identify the bar to enter name
    ele = driver.find_element_by_name("/b/"+room_name+"[join_name]")
    # Write login name
    ele.send_keys(bot_name)
    ele.send_keys(Keys.ENTER)  # Enter (send)

    time.sleep(5)  # Need expliced waiting

    # send welcome message
    if welcome_message != "":
        send_chat_message(welcome_message)

    # Escape Popup *not working*
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # identify chat and start listing
    # ele = driver.find_elements_by_id("chat-messages")
    old_len = len(driver.find_elements_by_class_name("message--Z2n2nXu"))
    while True:
        messages = driver.find_elements_by_class_name("message--Z2n2nXu")

        if len(messages) == 0:
            old_len = 0
            continue

        if len(messages) > old_len:

            for i in range(0, (len(messages)-old_len)):
                command = str(messages[-(i+1)].text)
                print("Message: " + command)
                if command.startswith("/"):
                    execute_command(command.lower())
                    print("Command: " + command)
            old_len = len(messages)
        time.sleep(tick_time)




