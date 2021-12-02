from scrapers import HockeyAuthenticProductScraper, FanaticsProductScraper

def test_ha():
    price_string = "$127.99 CAD"
    result = HockeyAuthenticProductScraper.price_formatter(price_string)
    expected = float("127.99")

    assert result == expected


def test_nhlshop():
    price_string = "CAD 199.99"
    result = FanaticsProductScraper.price_formatter(price_string)
    expected = float("199.99")
    assert result == expected