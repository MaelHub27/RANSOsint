# Ransomware Detection Bot

The purpose of this bot is to oversee domains and notify a user in case of ransomware attack detected.

It calls APIs and look in the responses if a domain is present or not, the APIs are : 

- Ransomlook.io
- Ransomware.live

## Files

The two files used in the src folder are :

- alert_sender.py : to send an email to a user

- ransomware.py : the bot who will detect the ransomware attack and notify (or not) a user

The file domains.json is used to add or remove domains to verify, you may add your domain in this file if you want to check for potential ransomware attacks. You can either enter the full domain : <"www.mydomain.com">, or partially : <"mydomain.org"> / <"www.mydomain"> or even just the domain name itself : <"domain">.

## Dependencies

First, install the requirements with :

    pip install -r requirements.txt

## Usage

The bot will request all APIs once every day, to launch it, enter the following command line in the src folder :

    python3 ransomware.py <domains_file.json> <sender_mail> <sender_mail_password> <receiver_mail>
