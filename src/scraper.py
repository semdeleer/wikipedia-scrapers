import requests
from requests import Session
from bs4 import BeautifulSoup
import json

class Scraper:

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
                self.get_session_request(cookie, session)  # Ignoring the return value for the cookie request
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
        with open("classleadesparaf.json", "w") as outfile:
            json.dump(dictl, outfile, indent=4)


