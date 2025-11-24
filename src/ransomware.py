import requests
import sys
import json
from alert_sender import AlertSender
import time

class RANSOsint:
    
    def __init__(self):
        self.domains = {} # List of overseen domains
        self.api_urls = {
            "RansomWareLive" : "https://api.ransomware.live/v2/recentvictims", 
            "RansomLook" : "https://www.ransomlook.io/api/recent",
            "Ransomfeed" : "https://api.ransomfeed.it/offset/100"
            } # API urls used to detect ransomware attacks
        self.json_response = {} # Response body from each API
        if len(sys.argv) != 5:
            print(f"\r\nInvalid number of arguments (expected 4) \r\n\r\nUsage : python3 {sys.argv[0]} <domains_file.json> <sender_mail> <sender_mail_password> <receiver_mail> \r\n")
            exit(1)
        else :
            with open(sys.argv[1]) as f:
                self.domains = json.load(f)
        self.alert_sender = AlertSender(token="", chat_id=0, sender_mail=sys.argv[2], password_mail=sys.argv[3])
        self.receiver_mail = sys.argv[4]
        self.has_been_ransomwared = {} # Domains that have been ransomwared
            
    def get_responses(self): # Used to get all json body from APIs
        for key in self.api_urls:
            try:
                response = requests.get(self.api_urls[key], timeout=10)
                
                if response.status_code == 200:
                    self.json_response[key] = response.json()
                else:
                    print('Error:', response.status_code)
            except requests.exceptions.Timeout as e:
                print('Error:', e)    
    
    def get_ransom_from_api(self, apikey: str): # Check if a given domain is present in a response body from a certain api
        domain_name = None
        url = None
        group = None
        
        if apikey == "RansomWareLive":
            domain_name = "domain"
            url = "claim_url"
            group = "group"
        elif apikey == "RansomLook":
            domain_name = "post_title"
            url = "link"
            group = "group_name"
        elif apikey == "Ransomfeed":
            domain_name = "victim"
            group = "gang"
        
        for domain in self.domains["domains"]:    
            for victims in self.json_response[apikey]:
                if domain.lower() in victims[domain_name].lower():
                    if url == None:
                        claim_url = f"No url found for this attack by api {apikey}"
                    else :
                        claim_url = victims[url]
                    if victims[group] == None:
                        attacker_group = "No group found for this attack"
                    attacker_group = "attacker group : " + victims[group]
                    self.has_been_ransomwared[domain] = claim_url + ", by " + attacker_group

    def get_ransom_info(self): # Check if ay of the domain in the entry file <domains.json> has been ransmowared
        for apikey in self.json_response:
            self.get_ransom_from_api(apikey)
    
    def send_ransom_info(self): # Send email info for potential ransomware attack
        self.get_responses()
        self.get_ransom_info()
        length = len(self.has_been_ransomwared)
        if  length > 0:
            all_domains = ""
            informations = ""
            cursor = 0
            for victim_domains in self.has_been_ransomwared:
                all_domains += victim_domains
                informations += victim_domains + " with link to the claim url : " + self.has_been_ransomwared[victim_domains]
                cursor += 1
                if cursor == length:
                    all_domains += ""
                    informations += ""
                elif cursor == length - 1:
                    all_domains += " and "
                    informations += " and "
                else:
                    all_domains += ", "
                    informations += ", "
            self.alert_sender.send_mail(self.receiver_mail, "Ransomware", all_domains, informations)
        elif length == 0:
            print("All given domains not found in ransomware lists, no mail sent.")
        else:
            print("Something went wrong... Exiting.")
            exit(1)

if __name__ == "__main__":
    a = RANSOsint()
    while True:
        a.send_ransom_info()
        time.sleep(86400) #Execute bot every day (1d = 24 * 3600 seconds = 86400 seconds)