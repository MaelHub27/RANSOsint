# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Libraries for Telegram notif
import asyncio # Necessary because telegram lib is asynchronous
from telegram import Bot

class AlertSender:
    
    ############################ INIT ############################

    def __init__(self, token:str, chat_id:int, sender_mail:str, password_mail:str):

        # Telegram bot config
        self.TOKEN = token
        self.CHAT_ID = chat_id 
        if token != "" :
            self.bot = Bot(token=self.TOKEN)
        # Email config
        self.sender_email = sender_mail
        self.password = password_mail
        #self.message = MIMEMultipart() -> moved in send_mail to not overflow headers

    ############################ BOT ############################

    async def create_alert(self, attack_type: str, server_address:str):
        message = "Suspected " + attack_type + " attack detected on your web server : " + server_address + ". Please go take a look."
        bot = Bot(token=self.TOKEN)
        try:
            await bot.send_message(chat_id=self.CHAT_ID, text=message)
        except Exception as e:
            print(f"An error occured during bot alert creation... ({e})")
            
    def send_notif(self, attack_type: str):
        asyncio.run(self.create_alert(attack_type))
        print("Notif sent.")
        
    ############################ MAIL ############################    
        
    def fill_mail_header(self, receiver:str, alert_type:str, server_address:str):
        
        # Email header info
        subject = "Alert " + alert_type + " attack potentially detected on " + server_address 
        self.message["From"] = self.sender_email
        self.message["To"] = receiver
        self.message["Subject"] = subject

    def send_mail(self, receiver:str, alert_type:str, server_address:str, informations:str):
        
        self.message = MIMEMultipart()
        self.fill_mail_header(receiver=receiver, alert_type=alert_type, server_address=server_address) 

        # Email content
        body = "This email has been sent to inform you that a " + alert_type + " attack might have happened on your web server " + server_address + " with the following informations : " + informations + ". \r\n\r\nYou may want to take a look at it."

        # Email sending
        self.message.attach(MIMEText(body, "plain"))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(self.message, from_addr=self.sender_email, to_addrs=receiver)
                print("Email sent.")
        except Exception as e:
            print(f"Error when sending email... ({e}).")