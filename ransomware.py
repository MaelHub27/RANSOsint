import requests

class RANSOsint:
    
    def __init__(self, domain: str, urls=["https://api.ransomware.live/v2/recentvictims", "https://www.ransomlook.io/api/recent"]):
        self.domain = domain
        self.urls = {"RansomWareLive" : urls[0], "RansomLook" : urls[1]}
        self.json_response = {}
        self.get_json_response()
        
    def get_json_response(self):
        for key in self.urls:
            try:
                # Make a GET request to the API endpoint using requests.get()
                response = requests.get(self.urls[key])
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    self.json_response[key] = response.json()
                else:
                    print('Error:', response.status_code)
            except requests.exceptions.RequestException as e:
            
                # Handle any network-related errors or exceptions
                print('Error:', e)    
    
    def get_ransom_from_api(self, apikey: str):
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
            
        for i in range(len(self.json_response[apikey])):
            if self.domain in self.json_response[apikey][i][domain_name]:
                print(f"\r\n Warning : The domain {self.domain} has been found in the ransomware list from the {apikey} API. \r\n")
                claim_url = " Link to the claim url : " + self.json_response[apikey][i][url] + "\r\n"
                print(claim_url)
                group = " Attacker Group : " + self.json_response[apikey][i][group] + "\r\n"
                print(group)
                return True
        print(f"\r\n Domain {self.domain} not found in ransomware list from {apikey}. \r\n")
        return False      

    def get_ransom_info(self):
        for apikey in self.json_response:
            self.get_ransom_from_api(apikey)
                
                      
#tests
# maresalogistica for 1st API
# for 2nd API
# bew
a = RANSOsint("maresalogistica")
a.get_ransom_info()
