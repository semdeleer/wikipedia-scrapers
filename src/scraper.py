import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re
import csv

class Scraper:
    """
    Scraper class for retrieving and processing data from the Country Leaders API and Wikipedia.

    Attributes:
    - root_url (str): The root URL for the Country Leaders API.
    - status_url (str): The URL for checking the status of the API.
    - countries_url (str): The URL for retrieving the list of countries from the API.
    - cookie_url (str): The URL for obtaining a session cookie from the API.
    - leaders_url (str): The URL for retrieving information about country leaders from the API.

    Methods:
    - get_session_request(url: str, session: Session) -> Optional[Dict]: Sends a GET request to the specified URL using the provided session.
    - get_session_loop_request(cookie: str, url: str) -> Optional[Dict]: Sends a series of GET requests using a session and returns data based on the provided cookie and URL.
    - get_session_loop_request_param(cookie: str, url: str, country_code: List[str]) -> Dict[str, List[Dict]]: Sends a series of GET requests with parameters using a session and returns data for each country code.
    - get_leaders() -> Dict[str, List[Dict]]: Retrieves information about country leaders using the session loop and specified URLs.
    - get_wiki_leader() -> List[str]: Retrieves Wikipedia URLs for country leaders based on the information obtained from the API.
    - get_first_paraf() -> List[str]: Retrieves the first paragraphs from the Wikipedia pages of country leaders.
    - get_paraf_leader() -> List[Dict[str, Union[str, List[str]]]]: Combines information about country leaders with their corresponding Wikipedia paragraphs.
    - set_write_json(): Writes the information about country leaders and their paragraphs to a JSON file named "classleadesparaf.json".
    """

    def __init__(self) -> None:
        self.root_url = "https://country-leaders.onrender.com/"
        self.status_url = "https://country-leaders.onrender.com/status/"
        self.countries_url = "https://country-leaders.onrender.com/countries/"
        self.cookie_url = "https://country-leaders.onrender.com/cookie/"
        self.leaders_url = "https://country-leaders.onrender.com/leaders/"

    def get_session_request(self, url: str, session: Session):
            response = session.get(url)
            response_json = response.json()
            status_response = session.get(self.status_url)

            if status_response.status_code == 200:
                return response_json
            else:
                print(status_response.status_code)
                return None

    def get_session_loop_request(self, cookie: str, url: str):
            with Session() as session:
                self.get_session_request(cookie, session)
                country_list = self.get_session_request(url, session)
                
                if country_list:
                    return country_list
            
    def get_session_loop_request_param(self, cookie: str, url: str, country_code):
            leadersl={}
            for i in country_code:
                leaders_country_url = f"{url}?country={i}"

                with Session() as session:
                    self.get_session_request(cookie, session)
                    leadersl[i] = self.get_session_request(leaders_country_url, session)
            return leadersl

    def get_leaders(self):
        return self.get_session_loop_request_param(self.cookie_url, self.leaders_url, self.get_session_loop_request(self.cookie_url, self.countries_url))

    def get_wiki_leader(self):
        leaderInfo = self.get_leaders()
        wikiLeaders = []
        for key, value in leaderInfo.items():
            for i in value:
                wikiLeaders.append(i["wikipedia_url"])
        return wikiLeaders
    
    def get_first_paraf(self):
        paragrapf = []
        ids = 1
        for wiki in self.get_wiki_leader():
            url = wiki
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html")
            for id, elem in enumerate(soup.find_all("p")):
                    if id == ids and elem.text == '\n':
                        ids += 1
                    if id == ids and elem.text != '\n':
                        paragrapf.append(elem.text)
                        break
        return paragrapf
    
    def get_paraf_leader(self):
        dict_lead = self.get_leaders()
        dict_leader = {}
        for key, values in dict_lead.items():
            dict_leader = [{'first_name': person['first_name'], 'last_name': person['last_name']} for people in dict_lead.values() for person in people]
        list_paraf = self.get_first_paraf()
        lcount = 0
        for i in dict_leader:
            i["paraf"] = list_paraf[lcount]
            lcount += 1
        return dict_leader
    
    def set_write_json(self):
        dictl = self.get_paraf_leader()
        brackt = re.compile(r'\[.*?\]')
        for i in dictl:
            i["paraf"] = re.sub(brackt, '', i["paraf"])
        with open("classleadesparaf.json", "w", encoding='utf-8') as outfile:
            json.dump(dictl, outfile, indent=4, ensure_ascii=False)
    
    def write_csv(self):
        #You need to add encoding utf8 after it because the json file is written with this param
        with open('classleadesparaf.json', 'r', encoding='utf-8') as json_file:
            jsondata = json.load(json_file)
        
        #the isinstance check if a object is a specefic class
        if isinstance(jsondata, list) and jsondata:
            keys = jsondata[0].keys()  # Assuming all dictionaries in the list have the same keys

            with open('classleadesparaf.csv', 'w', newline='', encoding='utf-8') as outfile:
                csv_writer = csv.writer(outfile)
                #the keys from the json file become the headers
                csv_writer.writerow(keys)

                for item in jsondata:
                    #The values become the rows of the csv file
                    csv_writer.writerow(item.values())


