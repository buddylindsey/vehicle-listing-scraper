# Vehicle Listing Scraper

This is the start to a generic scraper for pulling in vehicle listings off of sites. The first one is AutoTrader and is kind of the example. Others could be added.

### Lastest Working Date
This the last time the scraper worked with the HTML on the site the provider was written for.

* `AutoTrader` - 11-24-2017

## Components

### Providers

* `BaseProvider` This is the base class for common things. See AutoTrader for example implementations.
* `AutoTrader` This is the class for AutoTrader that takes a vehicle object and mangles it around to pull in vehicle data. For starters it pulls in the first page of results for each trim type.

### Vehicles

* `Honda` Holds vehicle models with some basic information for hondas.
* `Toyota` Holds vehicle models with some basic information for toyotas.
* `Chrysler` Holds vehicle models with some basic information for chryslers.
* `Dodge` Holds vehicle models with some basic information for dodges.

### Utils

* `VINMixin` Mixin for getting information about the vin number. To start you can get the year from the vin number instead of scraping it.

## Usage

I recommend to fork this repo, clone it locally, and create a `main.py` in the root. Below is an example of using it to get a Honda Odyssey based on my default location information.

### Basic Usage
```python
import csv

from src.providers import AutoTrader
from src.vehicles.honda import Odyssey

data = AutoTrader(Odyssey()).get_data()

with open('odyssey.csv', 'w+') as the_file:
    fieldnames = [
        'vin', 'mileage', 'mpg', 'engine', 
        'transmission', 'price', 'year', 'trim', 'url'
    ]

    writer = csv.DictWriter(the_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### Custom Config
```python
import csv

from src.providers import AutoTrader
from src.vehicles.honda import Odyssey

custom_config = {
    "startyear": 2010,
    "endyear": 2016,
    "perpage": 100,  # see autotrader for different paging options
    "mileradius": 500,
    "zip": 74864,
    "location": "Prague+OK-74864",
    "engine": "6CLDR"  # 6 Cylindar car
}

data = AutoTrader(Odyssey(), base_url_config=custom_config).get_data()

with open('odyssey.csv', 'w+') as the_file:
    fieldnames = [
        'vin', 'mileage', 'mpg', 'engine', 
        'transmission', 'price', 'year', 'trim', 'url'
    ]

    writer = csv.DictWriter(the_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### Custom User Agent
AutoTrader filters requests based on user agent so you need to set a user agent of an actual browser.
```python
import csv

from src.providers import AutoTrader
from src.vehicles.honda import Odyssey

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"

data = AutoTrader(Odyssey(), user_agent=agent).get_data()

with open('odyssey.csv', 'w+') as the_file:
    fieldnames = [
        'vin', 'mileage', 'mpg', 'engine', 
        'transmission', 'price', 'year', 'trim', 'url'
    ]

    writer = csv.DictWriter(the_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## Contribute
This isn't really meant to be a long term project. Just something to mess around with here and there to find listings to get an idea of what a good average price for a specfic vehicle. If you want to contribute to making it better please feel free to submit PRs.