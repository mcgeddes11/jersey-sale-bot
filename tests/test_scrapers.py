from website_enums import scrapers
import re
from scrapers import DicksSportingGoodsProductScraper
import requests
import itertools
from multiprocessing import Process, Queue, Pool


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
    scraper.scrape_products(scraper.url)
    print("Found {} products".format(len(scraper.products)))

def test_scrape_all_implementations():
    scraper = scrapers["SvpSports"]
    scraper.get_all_products()

def test_parallelization():

    # Run the two parallelized
    scraper_1 = scrapers["RiverCitySports"]
    scraper_2 = scrapers["BostonTeamStore"]

    queue = Queue()

    scraper_1._set_queue(queue)
    scraper_2._set_queue(queue)

    processes = [Process(target=scraper_1.get_all_products),
                 Process(target=scraper_2.get_all_products)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    # Get parallelized results list
    parallel_results = [queue.get() for p in processes]
    parallel_results = list(itertools.chain.from_iterable(parallel_results))

    # Now run them in serial and check the results match
    scraper_1._set_queue(None)
    scraper_2._set_queue(None)
    scraper_1.get_all_products()
    scraper_2.get_all_products()

    assert(len(list(parallel_results)) == len(scraper_1.products) + len(scraper_2.products))



