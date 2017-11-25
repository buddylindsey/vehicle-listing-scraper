import time
import requests
from bs4 import BeautifulSoup

from .utils import VINMixin


class BaseProvider:
    def __init__(self, vehicle):
        pass
    
    def get_data(self):
        pass

    def get_listing_urls(self):
        pass

    def get_page(self, url):
        headers = {
            "User-Agent": self.user_agent
        }

        response = requests.get(url, headers=headers)
        return BeautifulSoup(response.content, 'html.parser')
    

class AutoTrader(VINMixin, BaseProvider):
    base_url = "https://www.autotrader.com/cars-for-sale/{make}/{model}/{location}?zip={zip}&startYear={startyear}&numRecords={perpage}&sortBy=derivedpriceDESC&engineCodes={engine}&firstRecord=0&endYear={endyear}&modelCodeList={modelcodelist}&makeCodeList={makecodelist}&searchRadius={mileradius}"
    base_url_config = {
        "startyear": 2010,
        "endyear": 2016,
        "perpage": 100,
        "mileradius": 500,
        "zip": 74864,
        "location": "Prague+OK-74864",
        "engine": "6CLDR"
    }
    vehicle = None
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"
    vin = ("td", {"data-qaid": "tbl-value-VIN"})
    mpg = ("td", {"data-qaid": "tbl-value-MPG"})
    engine = ("td", {"data-qaid": "tbl-value-Engine"})
    transmission = ("td", {"data-qaid": "tbl-value-Transmission"})

    def __init__(self, vehicle, user_agent=None, base_url_config=None):
        self.vehicle = vehicle
        if user_agent:
            self.user_agent = user_agent
        if base_url_config:
            self.base_url_config = base_url_config

    def get_data(self):
        ret = []

        for trim, url in self.get_listing_urls():
            page = self.get_page(url)

            paged_list = page.find_all("div", {"data-qaid": "cntnr-lstng-premium"})

            for result in paged_list:
                url = "https://www.autotrader.com/{}".format(result.find('a', href=True)['href'].split('&')[0])
                print(url)
                data = self.get_content_for_listing_page(url)
                data['trim'] = trim
                print(data)
                ret.append(data)
                time.sleep(5)  # being a good citizen and not hammering the server

        return ret

    def get_listing_urls(self):
        urls = []
        for trim in self.vehicle.trims:
            url = "{}&trimCodeList={}".format(self.get_url(), self.get_trim_code(trim))
            urls.append((trim, url))
        return urls

    def get_url(self):
        return self.base_url.format(**self.get_url_config())
        return self.base_url.format(**self.vehicle.url_config)

    def get_url_config(self):
        config = self.base_url_config.copy()
        config.update(self.get_make_model())
        return config

    def get_make_model(self):
        if self.vehicle.make == "Honda":
            if self.vehicle.model == "Odyssey":
                return {
                    "make": "Honda",
                    "model": "Odyssey",
                    "modelcodelist": "ODYSSEY",
                    "makecodelist": "HONDA",
                }
        if self.vehicle.make == "Dodge":
            if self.vehicle.model == "GrandCaravan":
                return {
                    "make": "Dodge",
                    "model": "Grand+Caravan",
                    "modelcodelist": "GRANDCARAV",
                    "makecodelist": "DODGE",
                }
        if self.vehicle.make == "Chrysler":
            if self.vehicle.model == "TownAndCountry":
                return {
                    "make": "Chrysler",
                    "model": "Town+&+Country",
                    "modelcodelist": "TANDC",
                    "makecodelist": "CHRY",
                }
        if self.vehicle.make == "Toyota":
            if self.vehicle.model == "Sienna":
                return {
                    "make": "Toyota",
                    "model": "Sienna",
                    "modelcodelist": "SIENNA",
                    "makecodelist": "TOYOTA",
                }

    def get_content_for_listing_page(self, url):
        soup = self.get_page(url)
        vin = self.get_single_element_content(soup, *self.vin)
        return {
            "vin": vin,
            "mpg": self.get_single_element_content(soup, *self.mpg),
            "engine": self.get_single_element_content(soup, *self.engine),
            "transmission": self.get_single_element_content(soup, *self.transmission),
            "year": self.get_vin_year(vin),
            "mileage": self.get_mileage(soup),
            "price": self.get_price(soup),
            "url": url
        }

    def get_single_element_content(self, soup, element, location):
        try:
            return soup.find(element, location).contents[0]
        except:
            return ''

    def get_price(self, soup):
        try:
            try:
                return soup.find("table", {"data-qaid": "cntnr-priceBreakDown"}).find_all('td')[-1].contents[0]
            except AttributeError:
                return soup.find("div", {"data-qaid": "cntnr-pricing"}).find("span", {"data-qaid": "cntnr-lstng-price1"}).find("strong").contents[0]
        except:
            return ''

    def get_mileage(self, soup):
        try:
            return soup.find('td', {'data-qaid': 'tbl-value-Mileage'}).span.span.contents[1]
        except:
            return ''

    def get_trim_code(self, trim):
        if self.vehicle.make == "Honda":
            if self.vehicle.model == "Odyssey":
                return {
                    "Elite": "ODYSSEY%7CElite",
                    "EX": "ODYSSEY%7CEX",
                    "EX-L": "ODYSSEY%7CEX-L",
                    "LX": "ODYSSEY%7CLX",
                    "SE": "ODYSSEY%7CSE",
                    "Touring": "ODYSSEY%7CTouring",
                    "Touring Elite": "ODYSSEY%7CTouring%20Elite",
                }.get(trim)
        if self.vehicle.make == "Dodge":
            if self.vehicle.model == "GrandCaravan":
                return {
                    "American Value Package": "GRANDCARAV|American Value Package",
                    "Crew": "GRANDCARAV|Crew",
                    "eL": "GRANDCARAV|eL",
                    "ES": "GRANDCARAV|Crew",
                    "eX": "GRANDCARAV|eX",
                    "Express": "GRANDCARAV|Express",
                    "GT": "GRANDCARAV|GT",
                    "Hero": "GRANDCARAV|Hero",
                    "LE": "GRANDCARAV|LE",
                    "Mainstreet": "GRANDCARAV|Mainstreet",
                }.get(trim)
        if self.vehicle.make == "Chrysler":
            if self.vehicle.model == "TownAndCountry":
                return {
                    "EX": "TANDC|EX",
                    "Limited": "TANDC|Limited",
                    "Limited Platinum": "TANDC|Limited%20Platinum",
                    "LX": "TANDC|LX",
                    "LXi": "TANDC|LXi",
                    "S": "TANDC|S",
                    "Touring": "TANDC|Touring",
                    "Touring Plus": "TANDC|Touring%20Plus",
                    "Touring-L": "TANDC|Touring-L"
                }.get(trim)
        if self.vehicle.make == "Toyota":
            if self.vehicle.model == "Sienna":
                return {
                    "CE": "SIENNA%7CCE",
                    "L": "SIENNA%7CL",
                    "LE": "SIENNA%7CLE",
                    "Limited": "SIENNA%7CLimited",
                    "Limited Premium": "SIENNA%7CLimited%20Premium",
                    "SE": "SIENNA%7CSE",
                    "SE Premium": "SIENNA%7CSE%20Premium",
                    "XLE": "SIENNA%7CXLE",
                    "XLE Limited": "SIENNA%7CXLE%20Limited",
                    "XLE Premium": "SIENNA%7CXLE%20Premium"
                }.get(trim)