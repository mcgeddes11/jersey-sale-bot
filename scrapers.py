from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import numpy
import pandas

# Base classes
class ProductScraper(ABC):

    def __init__(self, url):
        self.url = url
        self.domain = "https://" + urlparse(url).netloc
        self.needs_pagination = False
        self.products = []
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept': '*/*',
                        'Connection': 'keep-alive'}

    @abstractmethod
    def scrape_products(self, get_url):
        # Abstract method that should implement scraping logic to get the product details and return an absolute link
        # to the next page. If no more pages, return Nones
        # Product data is a list of dicts of the form
        # {
        #   product_name:       some sort of description,
        #   product_url:        absolute URL to the product page,
        #   product_image_url:  absolute URL to product image,
        #   price:              price (string repr)
        # }
        pass

    @staticmethod
    @abstractmethod
    def price_formatter(price_string):
        # Each site uses a different string representation of price, so each site needs to implement their own formatter
        # This should be a simple one-liner to convert for e.g. CAD 159.99 to float(159.99)
        # should return a float value
        pass

    def get_all_products(self, site_name=None):
        # Same operational loop happens on every site
        # Get the base sale page, scrape products returns a link to the next page
        # Iterate until it returns None
        get_url = self.url

        while get_url is not None:
            get_url = self.scrape_products(get_url)

        # add site name to all product items
        for p in self.products:
            p["site_name"] = site_name

class ShopifyProductScraper(ProductScraper):

    def scrape_products(self, product_page_url):

        products = requests.get(product_page_url, timeout=None, headers=self.headers).json()["products"]
        self.products = self.products + products

        # If we've reached the end of the products list, we want to filter and format them appropriately
        if len(products) == 0:
            self.filter_format_products()
            return None
        else:
            # Get the next page URL
            page_numstring = product_page_url.split("=")[-1]
            current_page = int(page_numstring)
            next_page = "?page=" + str(current_page + 1)
            next_page_url = product_page_url.replace("?page=" + page_numstring, next_page)
            return next_page_url

    def filter_format_products(self):

        # Products to dataframe for ease of filtering etc
        product_dataframe = pandas.DataFrame.from_records(self.products,
                                                          columns=["id", "title", "vendor", "product_type"])
        # Find jerseys
        valid_product_ids = self.find_jersey_products(product_dataframe)

        # Get all variants
        jersey_products = []
        for product in self.products:
            if product["id"] in valid_product_ids:
                jersey_products.append(product)

        # Now for every variant we want to get the prices to see what's on sale
        sale_products = []
        for product in jersey_products:
            for variant in product["variants"]:
                if variant["compare_at_price"] is not None and float(variant["compare_at_price"]) != 0.0 and float(variant["compare_at_price"]) > float(variant["price"]):
                    sale_products.append({
                        'product_id': product["id"],
                        'variant_id': variant["id"],
                        'product_name': product["title"],
                        'variant_name': variant["title"],
                        'price': float(variant["price"]),
                        'url': urljoin(self.domain, "products/" + product["handle"]),
                        'product_image_url': product["images"][0]["src"]
                    })
        df = pandas.DataFrame.from_records(sale_products, columns=["product_name", "price", "url", "product_image_url"])
        df = df.drop_duplicates()
        self.products = df.to_dict(orient='records')

    @abstractmethod
    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        # Takes a product dataframe and returns a list of valid product ids that are jersey products
        raise NotImplementedError("Did you forget to implement the jersey finding logic?")


# Trusted sellers
class HockeyAuthenticProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        # TODO: Add product_type == "OFFER" to this?
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics", "Reebok", "CCM", "Nike"]
                          for x, y in zip(product_dataframe["product_type"],
                                          product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("$","").replace("CAD","").strip())

class CoolHockeyProductScraper(ProductScraper):

    def scrape_products(self, product_page_url):
        response = requests.get(product_page_url, timeout=None, headers=self.headers)
        soup = BeautifulSoup(response.text, features="lxml")
        products = soup.find_all("div", {"class": "product-item-info"})
        for p in products:
            stock_unavailable = p.find("div", {"class": "stock unavailable"})
            if stock_unavailable is not None:
                continue
            product_item_link = p.find("a", {"class": "product-item-link"})
            product_image_container = p.find("div", {"class": "product-img"})
            product_data = {
                'product_name': product_item_link.text.strip(),
                'product_url': urljoin(self.domain, product_item_link.attrs["href"]),
                'product_image_url': product_image_container.find("img").attrs["src"],
                'product_price': self.price_formatter(p.find("span", {"class": "price"}).text)
            }
            self.products.append(product_data)

        next_page_link = soup.find("a", {"class": "action next"})
        if next_page_link is None:
            return None
        else:
            return next_page_link.attrs["href"]


    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("CA", "").replace("$", "").strip())

# Fanatics group pages
class FanaticsProductScraper(ProductScraper):

    def scrape_products(self, product_page_url):
        response = requests.get(product_page_url, timeout=None, headers=self.headers)
        soup = BeautifulSoup(response.text, features="lxml")
        products = soup.find_all("div", {"class": "product-card"})
        for p in products:
            product_card = p.find("div", {"class": "product-card-title"})
            product_image_container = p.find("div", {"class": "product-image-container"})
            product_data = {
                'product_name': product_card.text,
                'product_url': urljoin(self.domain, product_card.find("a").attrs["href"]),
                'product_image_url': product_image_container.find("a").attrs["href"].replace("//", "https://"),
                'product_price': self.price_formatter(p.find_all("span", {"class": "sr-only"})[0].text.replace("\xa0"," "))
            }
            self.products.append(product_data)

        next_page_link = soup.find_all("li", {"class": "next-page"})
        if next_page_link is None:
            return None
        else:
            next_page_link = next_page_link[0].find("a")
            is_disabled = next_page_link.attrs["aria-disabled"] == 'true'
            if not is_disabled:
                return urljoin(self.domain, next_page_link.attrs["href"])
            else:
                return None

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("CAD","").replace("$","").strip())

# Team stores
class AnaheimTeamStoreProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics", "Reebok", "CCM"]
                          for x,y in zip(product_dataframe["title"],
                                         product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("$","").replace("CAD","").strip())

class CarolinaProShopProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics"]
                          for x,y in zip(product_dataframe["product_type"], product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("$","").replace("CAD","").strip())

class ColoradoTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        # TODO: validate this logic
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics"]
                          for x,y in zip(product_dataframe["product_type"], product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("$","").replace("CAD","").strip())

class VanbaseProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics", "Reebok", "CCM"]
                          for x,y in zip(product_dataframe["product_type"],
                                         product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

    @staticmethod
    def price_formatter(price_string):
        return float(price_string.replace("$","").replace("CAD","").strip())