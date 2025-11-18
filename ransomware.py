import requests
import sys
import json
sys.path.insert(0, "../DDOSint/src/")
from alert_sender import AlertSender 

class RANSOsint:
    
    def __init__(self):
        self.domains = {} # List of overseen domains
        self.api_urls = {
            "RansomWareLive" : "https://api.ransomware.live/v2/recentvictims", 
            "RansomLook" : "https://www.ransomlook.io/api/recent"
            } # API urls used to detect ransomware attacks
        self.json_response = {} # Response body from each API
        if len(sys.argv) != 5:
            print(f"Usage : {sys.argv[0]} <domain_file.json> <sender_mail> <sender_password> <receiver_mail>")
            exit(1)
        else :
            with open(sys.argv[1]) as f:
                self.domains = json.load(f)
        self.alert_sender = AlertSender(token="", chat_id=0, sender_mail=sys.argv[2], password_mail=sys.argv[3])
        self.receiver_mail = sys.argv[4]
        self.has_been_ransomwared = {} # Domains that have been ransomwared
            
    def get_responses(self): 
        for key in self.api_urls:
            try:
                # Make a GET request to the API endpoint using requests.get()
                response = requests.get(self.api_urls[key], timeout=5)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    self.json_response[key] = response.json()
                else:
                    print('Error:', response.status_code)
            except requests.exceptions.Timeout as e:
            
                # Handle any network-related errors or exceptions
                print('Error:', e)    
    
    def get_ransom_from_api(self, apikey: str): # Check if a given domain is present in a response for a certain api
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
        
        for domain in self.domains["domains"]:    
            for victims in self.json_response[apikey]:
                if domain in victims[domain_name]:
                    print(f"\r\n Warning : The domain {domain} has been found in the ransomware list from the {apikey} API. \r\n")
                    claim_url = " Link to the claim url : " + victims[url] + "\r\n"
                    print(claim_url)
                    attacker_group = " Attacker Group : " + victims[group] + "\r\n"
                    print(attacker_group)
                    self.has_been_ransomwared[domain] = domain
                    #return True
            print(f"\r\n Domain {domain} not found in ransomware list from {apikey}. \r\n")
            #return False      

    def get_ransom_info(self): # Check if ay of the domain in the entry file <domains.json> has been ransmowared
        if len(self.json_response) == 0:
            print("\r\n Please get all APIs' list responses before analysis (with the method get_responses).\r\n")
            return
        for apikey in self.json_response:
            self.get_ransom_from_api(apikey)
    
    def send_ransom_info(self): # Send email info for potential ransomware attack
        self.get_responses()
        self.get_ransom_info()
        length = len(self.has_been_ransomwared)
        if  length > 0:
            all_domains = ""
            cursor = 0
            for victim_domains in self.has_been_ransomwared:
                all_domains += self.has_been_ransomwared[victim_domains]
                cursor += 1
                if cursor == length:
                    all_domains += ""
                elif cursor == length - 1:
                    all_domains += " and "
                else:
                    all_domains += ", "
            self.alert_sender.send_mail(self.receiver_mail, "Ransomware", all_domains)

if __name__ == "__main__":
    a = RANSOsint()
    a.send_ransom_info()
    #tests
    # maresalogistica for 1st API
    # for 2nd API
    # bew