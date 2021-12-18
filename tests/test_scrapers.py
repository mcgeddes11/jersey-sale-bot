from website_enums import scrapers
import re
from scrapers import DicksSportingGoodsProductScraper
import requests
import itertools
from multiprocessing import Process, Queue, Pool, Manager


def test_coolhockey():
    scraper = scrapers["CoolHockey"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    print("Found {} products".format(len(scraper.products)))
    assert (next_page is None or type(next_page) == str)

def test_price_regex():
    test_string = "Price now: $195.00"
    a = re.search(r"\$?[0-9]{1,}\.?[0-9]{2}", test_string)
    assert a.group(0) == "$195.00"

def test_fanatics():
    scraper = scrapers["NHLShopCanada"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    print("Found {} products".format(len(scraper.products)))
    assert (next_page is None or type(next_page) == str)

def test_bigcommerce():
    scraper = scrapers["BostonTeamStore"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    print("Found {} products".format(len(scraper.products)))
    assert (next_page is None or type(next_page) == str)

def test_shopify():
    scraper = scrapers["StLouisTeamStore"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    print("Found {} products".format(len(scraper.products)))
    assert (next_page is None or type(next_page) == str)

def test_dicks_scraper():
    scraper = DicksSportingGoodsProductScraper("https://prod-catalog-product-api.dickssportinggoods.com/v2/search", currency="USD")
    scraper.scrape_products(scraper.url)
    print("Found {} products".format(len(scraper.products)))

def test_rcs_scraper():
    scraper = scrapers["RiverCitySports"]
    scraper.get_all_products()
    # scraper.scrape_products(scraper.url)
    # print("Found {} products".format(len(scraper.products)))

def test_scrape_all_implementations():
    scraper = scrapers["SvpSports"]
    scraper.get_all_products()

def test_parallelization():

    scraper_list = [scrapers["RiverCitySports"], scrapers["CarolinaProShop"], scrapers["HockeyAuthentic"]]

    process_pool = Pool(2)

    results = [process_pool.apply_async(x.get_all_products) for x in scraper_list]

    output = [p.get() for p in results]

    flat_output = [item for sublist in output for item in sublist]

    assert(len(flat_output) > 0)

