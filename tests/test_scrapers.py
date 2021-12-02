from website_enums import scrapers
import re


def test_coolhockey():

    scraper = scrapers["CoolHockey"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    assert (next_page is None or type(next_page) == str)

def test_price_regex():
    test_string = "Price now: $195.00"
    a = re.search(r"\$?[0-9]{1,}\.?[0-9]{2}", test_string)
    assert a.group(0) == "$195.00"


def test_hockeyauthentic():
    pass

def test_fanatics():
    pass

def test_shopify_collections():
    scraper = scrapers["PittsburghTeamStore"]
    scraper.get_all_products("PittsburghTeamStore")