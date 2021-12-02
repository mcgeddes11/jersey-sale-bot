from website_enums import scrapers

def test_coolhockey():

    scraper = scrapers["CoolHockey"]
    next_page = scraper.scrape_products(product_page_url=scraper.url)
    assert (next_page is None or type(next_page) == str)

def test_hockeyauthentic():
    pass

def test_fanatics():
    pass

def test_shopify_collections():
    scraper = scrapers["VanBase"]
    # next_page = scraper.scrape_products(product_page_url=scraper.url)

    scraper.get_all_products("VanBase")