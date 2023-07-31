import speech_recognition as sr
import easyimap
import pyttsx3 as tts
import smtplib
from email.message import EmailMessage

r= sr.Recognizer()
engine=tts.init()
voices= engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)
engine.setProperty('rate', 150)
dict = {}
def speak(str):
    print(str)
    engine.say(str)
    engine.runAndWait()
def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        str="Speak now"
        speak(str)
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            return text.lower()
        except:
            str="Sorry! Could not recognize what you said. Say again."
            speak(str)
            listen()

def get_emailaddress(receiver_name):
    if dict.keys().contains(receiver_name)==True:
        return dict[receiver_name]
    else:
        return -1
def generate_email_address():
    str = "Please speak the name of the person you want to send email to"
    speak(str)
    receiver_name = listen()
    str= "Is "+ receiver_name +" the intended receiver?"
    speak(str)
    choice=listen()
    if (choice!="no"):
        print(receiver_name)
        list = receiver_name.split(" ")
        n = len(list)
        str1 = ""
        for i in range(0, n):
            str1 += list[i]
        receiver_name=str1
        str = "Please speak your required domian name"
        speak(str)
        email_extension= listen()
        receiver_email = receiver_name + "@" + email_extension + ".com"
        return receiver_email
    else:
        generate_email_address()

def composemail():
    str="Do you want to send the same email to multiple persons?"
    speak(str)
    choice=listen()
    receiver_list = []
    if (choice=="yes"):
        str="Please speak the number of persons to send email to."
        speak(str)
        n=listen()
        num=dict[n]
        for i in range(0,num):
            receiver_email=generate_email_address()
            receiver_list.append(receiver_email)

    else:
        receiver_email = generate_email_address()

    #receiver_email= get_emailaddress(receiver_name)
    #if (receiver_email==-1):
        #str="Sorry! Email id does not exist. Please speak email address of the person"
        #speak(str)
        #receiver_email=listen()

    str = "Please speak the subject of your email"
    speak(str)
    subject = listen()

    str = "Please speak the body of your email"
    speak(str)
    message = listen()

    if (len(receiver_list)!=0):
        for i in receiver_list:
            sendmail(i, subject, message)
    else:
        sendmail(receiver_email, subject, message)

def sendmail(receiver, subject, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("emailbot1607@gmail.com", "vimxrfarapncvtbp")
    #server.sendmail("emailbot1607@gmail.com", "deepanshijalan@gmail.com", "Hello! How are you?")
    email=EmailMessage()
    email['From']="emailbot1607@gmail.com"
    email['To']=receiver
    email['Subject']=subject
    email.set_content(message)
    server.send_message(email)
    str = "You have spoken to send email to " + receiver + " at " + receiver + " with subject " + subject + \
          " and message " + message
    speak(str)

    str = "The message has been sent"
    speak(str)
def unread():
    # 1. count total no of unread mails, then tell system speak the email id of a person and the one email id would be called by user and then that mail will be opened accordingly )
    email_address = "emailbot1607@gmail.com"
    password = "vimxrfarapncvtbp"
    imap_server = "imap.gmail.com"

    server = easyimap.connect(imap_server, email_address, password)

    unread_emails = server.unseen()

    total_unread_emails = len(unread_emails)

    if total_unread_emails == 0:
        str = "You have no unread emails."
        speak(str)
    else:
        str = f"You have {total_unread_emails} unread email(s)."
        speak(str)

    for index, email in enumerate(unread_emails, 1):
        sender_email = email.from_addr
        str = f"Email {index}, sent by {sender_email}."
        speak(str)

    str = "Please say the email number you want to open, or say 'cancel' to exit."
    speak(str)

    while True:
        choice = listen()
        if choice == "cancel":
            str = "Exiting the email system."
            speak(str)
            return
        elif choice.isdigit() and 1 <= int(choice) <= total_unread_emails:
            email_number = int(choice) - 1
            email = list(unread_emails)[email_number]
            str = f"Opening email from {email.from_addr}. Subject: {email.title}"
            speak(str)
            read_email(email)

            str = "What do you want to do with this email? Say 'send', 'forward', 'reply', or 'cancel'."
            speak(str)

            while True:
                action_choice = listen()

                if action_choice == 'forward':
                    forward_email_action(email)
                    break
                elif action_choice == 'reply':
                    reply_email_action(email)
                    break
                elif action_choice == 'cancel':
                    str = "Exiting the email system."
                    speak(str)
                    return
                else:
                    str = "Invalid choice. Please say 'forward', 'reply', or 'cancel'."
                    speak(str)

            print("From:", email.from_addr)
            print("Subject:", email.title)
            print("Body:", email.body)
            return
        else:
            str = "Invalid choice. Please say the correct email number or 'cancel' to exit."
            speak(str)
            server.quit()

def search():

    str = "Do you want to search by keyword or sender name?"
    speak(str)
    choice = listen()

    if choice.lower() == "keyword":
        str = "Please speak the keyword you want to search for in your emails."
        speak(str)
        keyword = listen()
        str = f"Searching for emails containing the keyword '{keyword}'."
        speak(str)

        email_address = "emailbot1607@gmail.com"
        password = "vimxrfarapncvtbp"
        imap_server = "imap.gmail.com"

        server = easyimap.connect(imap_server, email_address, password)

        all_emails = server.listids(limit=100)

        filtered_emails = [email for email_id in all_emails
                           if keyword.lower() in server.mail(email_id).body.lower()]

        total_filtered_emails = len(filtered_emails)

        if total_filtered_emails == 0:
            str = f"No emails found containing the keyword '{keyword}'."
            speak(str)
            return

        str = f"Found {total_filtered_emails} email(s) containing the keyword '{keyword}'."
        speak(str)
        for index, email_id in enumerate(filtered_emails, 1):
            email = server.mail(email_id)
            sender_email = email.from_addr
            subject = email.title
            str = f"Email {index}, sent by {sender_email}. Subject: {subject}"
            speak(str)

        str = "Please say the email number you want to open, or say 'cancel' to exit."
        speak(str)
        while True:
            choice = listen()
            if choice == "cancel":
                str = "Exiting the email search."
                speak(str)
                return
            elif choice.isdigit() and 1 <= int(choice) <= total_filtered_emails:

                email_number = int(choice) - 1
                email_id = filtered_emails[email_number]
                email = server.mail(email_id)
                str = f"Opening email from {email.from_addr}. Subject: {email.title}"
                speak(str)
                print("From:", email.from_addr)
                print("Subject:", email.title)
                print("Body:", email.body)
                return
            else:
                str = "Invalid choice. Please say the correct email number or 'cancel' to exit."
                speak(str)
        server.quit()

    elif choice.lower() == "sender name":

        str = "Please speak the sender name you want to search for in your emails."
        speak(str)
        sender_name = listen()
        str = f"Searching for emails sent by '{sender_name}'."
        speak(str)

        email_address = "emailbot1607@gmail.com"
        password = "vimxrfarapncvtbp"
        imap_server = "imap.gmail.com"

        server = easyimap.connect(imap_server, email_address, password)

        all_emails = server.listids(limit=100)

        filtered_emails = [email for email_id in all_emails
                           if sender_name.lower() in server.mail(email_id).from_addr.lower()]

        total_filtered_emails = len(filtered_emails)

        if total_filtered_emails == 0:
            str = f"No emails found sent by '{sender_name}'."
            speak(str)
            return

        str = f"Found {total_filtered_emails} email(s) sent by '{sender_name}'."
        speak(str)

        for index, email_id in enumerate(filtered_emails, 1):
            email = server.mail(email_id)
            sender_email = email.from_addr
            subject = email.title
            str = f"Email {index}, sent by {sender_email}. Subject: {subject}"
            speak(str)


        str = "Please say the email number you want to open, or say 'cancel' to exit."
        speak(str)

        while True:
            choice = listen()
            if choice == "cancel":
                str = "Exiting the email search."
                speak(str)
                return
            elif choice.isdigit() and 1 <= int(choice) <= total_filtered_emails:

                email_number = int(choice) - 1
                email_id = filtered_emails[email_number]
                email = server.mail(email_id)
                str = f"Opening email from {email.from_addr}. Subject: {email.title}"
                speak(str)

                print("From:", email.from_addr)
                print("Subject:", email.title)
                print("Body:", email.body)
                return
            else:
                str = "Invalid choice. Please say the correct email number or 'cancel' to exit."
                speak(str)

        server.quit()

    else:
        str = "Invalid choice. Please say 'keyword' or 'sender name' to continue."
        speak(str)
        search()
def forward():
    str = "Please speak 'forward' to forward an email ."
    speak(str)
    choice = listen()

    if choice == 'forward':
        str = "Please speak the name of the person you want to forward the email to."
        speak(str)
        receiver_name = listen()

        str = f"Email has been forwarded to {receiver_name}."
        speak(str)

    else:
        str = "Invalid choice. Please speak 'forward' to continue."
        speak(str)
        forward()

def inbox():
    str="UNREAD     SEARCH    FORWARD    GO BACK"
    speak(str)
    ch=listen()
    if (ch=="unread"):
        unread()
    elif (ch=="search"):
        search()
    elif (ch=="forward"):
        forward()
    elif (ch=="go back"):
        main_menu()

def sentmail():
    str = "SEARCH MAIL      FORWARD       GO BACK"
    speak(str)

    ch = listen()

    if ch == "search mail":
        search()
    elif ch == "forward":
        forward()
    elif ch == "go back":
        main_menu()
    else:
        str = "Sorry, I didn't understand your choice. Please try again."
        speak(str)

def createmaillist():
    str="Speak the number of persons in mail list."
    speak(str)
    n=listen()
    for i in range(0,n):
        str="Speak name of person"
        key=listen()
        str="Speak email id of person"
        value=listen()
        dict[key]=value
    str="Your mail list is ready"
    speak(str)
    print(dict)

def main_menu():
    while (1):
        str = "MAIN MENU"
        speak(str)
        str = "COMPOSE MAIL                 INBOX                    SENT MAILS           CREATE MAIL LIST     EXIT"
        speak(str)

        choice = listen()
        if (choice == 'compose mail'):
            str = "You have chosen to compose mail."
            speak(str)
            composemail()

        elif (choice == 'inbox'):
            str = "You have chosen the inbox option."
            speak(str)
            inbox()

        elif (choice == 'sent mails'):
            str = "You have chosen the sent mails option"
            speak(str)
            sentmail()

        elif (choice == 'create mail list'):
            str = "You have chosen to create mail list."
            speak(str)
            createmaillist()

        elif (choice == 'exit'):
            str = "You have chosen to exit"
            speak(str)
            exit(1)

        else:
            str="Please speak a valid choice"
            speak(str)
            main_menu()

        str = "Do you wish to continue?"
        speak(str)

        ch = listen()
        if (ch == 'no'):
            str = "Thank you! Hope the email bot was able to help you"
            speak(str)
            exit(1)

str="Welcome to voice based email system"
speak(str)
dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
#main_menu()
#search()
unread()

