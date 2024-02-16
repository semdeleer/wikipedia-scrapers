from src.scraper import Scraper
import requests
from requests import Session
from bs4 import BeautifulSoup
import json

wikscraper = Scraper()
wikscraper.get_leaders()
wikscraper.get_wiki_leader()
wikscraper.get_first_paraf()
wikscraper.get_paraf_leader()
wikscraper.set_write_json()