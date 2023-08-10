import json
import requests
import bs4

from bs4 import BeautifulSoup

class Scraper(object):
    """docstring for Scraper."""

    def __init__(self):
        super(Scraper, self).__init__()
        with open("towers.json", "r") as f:
            self.towers = json.load(f)

    def scrapeLauncher(self):

            self.siteScraper(site = link)

    def siteScraper(self, site):
        html = self.getHTML("https://bloons.fandom.com/wiki/Bloons_TD_6")
        soup = BeautifulSoup(html, "html.parser")
        #Sorting out sites
        parsed_links = []
        links = [link['href'].split("#")[0] for link in soup.find_all('a', href=True)]
        for link in links:
            if ("?" in link):
                link = link.split("?")[0]
            check_con = False

            check_for = ["Bloons_Wiki", "Category:", "File:", "Special:", "wikipedia.org", "community.fandom","Blog:", "TD_5", "TD_4", "TD_3", "TD_2", "TD_1"]
            for codeword in check_for:
                if codeword in link:
                    check_con = True
            if check_con:
                pass
            elif ("https://bloons.fandom.com/wiki/" in link):
                parsed_links.append(link)
            elif ("/wiki/" in link):
                parsed_links.append("https://bloons.fandom.com" + link)

        parsed_links.sort()
        parsed_links = list(dict.fromkeys(parsed_links))

        for link in parsed_links:
            html = self.getHTML(link)
            self.towerParser(html)

    def towerParser(self, html):
        soup = BeautifulSoup(html, "html.parser")

    def get_number_sites(self):
        return len(self.sites)

    def getHTML(self, url : str):
        print(f"fetching HTML for : {url}")
        response = requests.get(url)
        html_str = response.text
        return html_str
