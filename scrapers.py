from abc import ABC, abstractmethod
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import numpy
import pandas
from utils import price_formatter
import json
from multiprocessing import Queue


# Base classes
class ProductScraper(ABC):

    def __init__(self, url, currency=None):
        self.url = url
        self.currency = currency
        self.domain = "https://" + urlparse(url).netloc
        self.needs_pagination = False
        self.products = []
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept': '*/*',
                        'Connection': 'keep-alive'}
        self.session = None
        self.queue = None

    @abstractmethod
    def scrape_products(self, get_url):
        # Abstract method that should implement scraping logic to get the product details and return an absolute link
        # to the next page. If no more pages, return Nones
        # Product data is a list of dicts of the form
        # {
        #   product_name:       some sort of description,
        #   product_url:        absolute URL to the product page,
        #   product_image_url:  absolute URL to product image,
        #   price:              price (float repr)
        # }
        pass

    def get_all_products(self, site_name=None):
        # Same operational loop happens on every site
        # Get the base sale page, scrape products returns a link to the next page
        # Iterate until it returns None
        get_url = self.url

        while get_url is not None:
            get_url = self.scrape_products(get_url)

        # add site name and currency to all product items
        # TODO: add filter to remove kids stuff?
        for p in self.products:
            p["site_name"] = site_name
            p["currency"] = self.currency

        # This bit supports multiprocessing
        if self.queue is not None:
            self.queue.put(self.products)

    # Internal function for setting the results queue to support multiprocessing. Used by the orchestrator only
    def _set_queue(self, queue: Queue):
        self.queue = queue


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
                # TODO: filter out out of stock variants here somehow?
                if variant["compare_at_price"] is not None and float(variant["compare_at_price"]) != 0.0 and float(variant["compare_at_price"]) > float(variant["price"]):
                    sale_products.append({
                        'product_id': product["id"],
                        'variant_id': variant["id"],
                        'product_name': product["title"],
                        'variant_name': variant["title"],
                        'product_price': float(variant["price"]),
                        'url': urljoin(self.domain, "products/" + product["handle"]),
                        'product_image_url': "" if product["images"] == [] else product["images"][0]["src"]
                    })
        df = pandas.DataFrame.from_records(sale_products, columns=["product_name", "product_price", "url", "product_image_url"])
        df = df.drop_duplicates()
        self.products = df.to_dict(orient='records')

    @abstractmethod
    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        # Takes a product dataframe and returns a list of valid product ids that are jersey products
        raise NotImplementedError("Did you forget to implement the jersey finding logic?")


class BigCommerceProductScraper(ProductScraper):

    def scrape_products(self, product_page_url):
        response = requests.get(product_page_url, timeout=None, headers=self.headers)
        soup = BeautifulSoup(response.text, features="lxml")
        products = soup.find_all("li", {"class": "product"})
        for p in products:
            title_card = p.find("h4", {"class": "card-title"})

            # Filter for jerseys here, as we point at base sale page
            title_string = title_card.text.strip()
            if "jersey" not in title_string.lower():
                continue

            product_card = p.find("div", {"class": "card-body"})
            product_data = {
                'product_name': title_string,
                'product_url': urljoin(self.domain, title_card.find("a").attrs["href"]),
                'product_image_url': "",  # images lazy-loaded on BigCommerce, so all we get is the loading image
                'product_price': price_formatter(product_card.find_all("span", {"class": "price"})[-1].text) # sale price should be the last field here
            }
            self.products.append(product_data)

        next_page_link = soup.find("li", {"class": "pagination-item pagination-item--next"})
        if next_page_link is None:
            return None
        else:
            return next_page_link.find("a").attrs["href"]


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
                'product_price': price_formatter(p.find("span", {"class": "price"}).text)
            }
            self.products.append(product_data)

        next_page_link = soup.find("a", {"class": "action next"})
        if next_page_link is None:
            return None
        else:
            return next_page_link.attrs["href"]


class DicksSportingGoodsProductScraper(ProductScraper):

    def __init__(self, url, currency=None):
        super().__init__(url=url, currency=currency)
        self.domain = "https://dickssportinggoods.com"
        self.api_parameters = {
            "selectedCategory": "12301_287054",
             "selectedStore": "0",
             "selectedSort": 5,
             "selectedFilters": {"4539": ["Jerseys"], "5495": ["Men\'s"]},
             "storeId": 15108,
             "pageNumber": 0,
             "pageSize": 48,
             "totalCount": 0,
             "searchTypes": ["CLEARANCE"],
             "isFamilyPage": True,
             "appliedSeoFilters": False,
             "snbAudience": "",
             "zipcode": ""
        }

    def scrape_products(self, product_page_url):
        # Direct calls are forbidden, gotta spoof the URL
        spoofed_url = product_page_url + "?searchVO=" + json.dumps(self.api_parameters)

        # Get the data
        response = requests.get(spoofed_url, headers=self.headers)
        data = response.json()

        # Update the product list
        for ix, product in enumerate(data["productVOs"]):
            self.products.append({
                "product_name": product["name"],
                "product_url": urljoin(self.domain, product["dsgSeoUrl"]),
                "product_image_url": "",  # couldn't find a consistent image url in the json payload
                "price": data["productDetails"][product["parentCatentryId"]]["prices"]["minofferprice"]
            })

        # Check result length to determine whether we need to iterate again (if it's less than pageSize we've gotten
        # all the products already and don't need another call
        result_length = len(data["productVOs"])
        if result_length >= self.api_parameters["pageSize"]:
            # Update the page number to get next set of results
            self.api_parameters["pageNumber"] = self.api_parameters["pageNumber"] + 1
            # we return same url, but we've already updated the pageNumber in the API parameters, so we will get the
            # next page on next iteration
            return product_page_url
        else:
            # Terminus condition: we've already gotten all results so superclass iteration handler needs to know
            return None


class RiverCitySportsProductScraper(ProductScraper):

    def scrape_products(self, product_page_url):

        response = requests.get(product_page_url, timeout=None, headers=self.headers)
        soup = BeautifulSoup(response.text, features="lxml")
        potential_products = soup.find("form", {"action": "viewproducts-06.cfm"}).find_all("td")
        for p in potential_products:
            # these are separators, skip
            if "colspan" in p.attrs.keys():
                continue
            product_details = p.find_all("a")
            text_details = product_details[1]
            image_details = product_details[0]
            product_name = text_details.text
            # filter for jerseys only
            lowername = product_name.lower()
            if "jersey" in lowername and "hoody" not in lowername:
                # Weird products that are on sale but not discounted?
                sale_price = p.find("span", {"class": "normalred"})
                if sale_price is not None:
                    product_price = price_formatter(sale_price.text)
                else:
                    product_price = price_formatter(p.find_all("div")[-1].text)
                product_data = {
                    'product_name': product_name,
                    'product_url': urljoin(self.domain, "CDA/" + text_details.attrs["href"]),
                    'product_image_url': urljoin(self.domain, image_details.find("img")["src"].replace("..","")),
                    'product_price': product_price
                }
                self.products.append(product_data)

        next_page_link = soup.find("input", {"name": "next"})
        if next_page_link is None:
            return None
        else:
            # Find what we are starting at
            startat_numstring = product_page_url.split("=")[-1]
            old_startat_value = "&startAt=" + startat_numstring
            # Get new value and replace in URL
            new_startat_value = "&startAt=" + str(int(startat_numstring) + 249)
            next_product_url = product_page_url.replace(old_startat_value, new_startat_value)
            return next_product_url


class SvpSportsProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        # This excludes womens/kids products
        product_dataframe = product_dataframe[product_dataframe["product_type"] == "Mens Apparel"]
        # Gets jerseys only
        ix = numpy.array([x.lower() in ["adidas", "fanatics", "reebok"] and "jersey" in y.lower() for x, y in
                          zip(product_dataframe["vendor"], product_dataframe["title"])])

        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class HockeyJerseyOutletProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["hockey" in x.lower() for x in product_dataframe["product_type"]])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


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
                'product_price': price_formatter(p.find_all("span", {"class": "sr-only"})[0].text.replace("\xa0"," "))
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


# Team stores
class AnaheimTeamStoreProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics", "Reebok", "CCM"]
                          for x,y in zip(product_dataframe["title"],
                                         product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids

class BuffaloTeamStoreProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        # TODO: Validate this logic
        ix = numpy.array(["jersey" in x.lower() for x in product_dataframe["title"]])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class CalgaryFlamesportProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        product_dataframe = product_dataframe[product_dataframe["product_type"] == "Jerseys"]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class CarolinaProShopProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics"]
                          for x,y in zip(product_dataframe["product_type"], product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class ChicagoTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        product_dataframe = product_dataframe[product_dataframe["product_type"] == "Jersey"]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class ColoradoTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        product_dataframe = product_dataframe[product_dataframe["product_type"] == "Avalanche Jersey"]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class DallasTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() for x in product_dataframe["title"]])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class LosAngelesTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and "la kings" in y.lower() for x,y in zip(product_dataframe["product_type"], product_dataframe["title"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class NewJerseyTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() for x in product_dataframe["product_type"]])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class NewYorkRangersTeamStore(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and y.lower() in ["fanatics", "adidas"] for x,y in zip(product_dataframe["product_type"], product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class OttawaTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and y.lower() in ["fanatics", "adidas"] for x,y in zip(product_dataframe["product_type"], product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class SeattleTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() for x in product_dataframe["title"]])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class StLouisTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array(["jersey" in x.lower() and y.lower() in ["jersey","sale","game-used"] for x,y in zip(product_dataframe["title"], product_dataframe["product_type"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class TorontoTeamStoreProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["jersey" in x.lower() and y.lower() in ["jersey","game worn"] for x,y in zip(product_dataframe["title"], product_dataframe["product_type"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class VanbaseProductScraper(ShopifyProductScraper):

    def find_jersey_products(self, product_dataframe: pandas.DataFrame):
        ix = numpy.array(["jersey" in x.lower() and y in ["Adidas", "Fanatics", "Reebok", "CCM"]
                          for x,y in zip(product_dataframe["product_type"],
                                         product_dataframe["vendor"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class VegasTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array([x.lower() in ["jersey", "game-used"] and "jersey" in y.lower() for x,y in zip(product_dataframe["product_type"], product_dataframe["title"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


class WinnipegTeamStoreProductScraper(ShopifyProductScraper):
    def find_jersey_products(self, product_dataframe):
        ix = numpy.array([x.lower() in ["jerseys", "game worn"] and "jersey" in y.lower() for x,y in zip(product_dataframe["product_type"], product_dataframe["title"])])
        product_dataframe = product_dataframe[ix]
        valid_product_ids = product_dataframe["id"].values.tolist()
        return valid_product_ids


