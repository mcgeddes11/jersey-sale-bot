from scrapers import FanaticsProductScraper, HockeyAuthenticProductScraper, CoolHockeyProductScraper, \
     AnaheimTeamStoreProductScraper, CarolinaProShopProductScraper, VanbaseProductScraper, ColoradoTeamStoreProductScraper
websites = {
    "NHLShop Canada":       {"url": "https://www.nhlshop.ca/en/men-jerseys/ga-23+d-50117028+os-90+z-97000-3006405570"},
    "Fanatics USA":         {"url": "https://www.fanatics.com/nhl/men-jerseys/o-1362+ga-56+d-08555612+os-78+z-914-677297166?_ref=p-OSLP:m-SIDE_NAV"},
    "Vanbase":              {"url": "https://vanbase.ca/collections/sale"},
    "CoolHockey":           {"url": "https://www.coolhockey.com/ca/sale.html"},
    "HockeyAuthentic":      {"url": "https://hockeyauthentic.com/collections/sale"},
    "Anaheim Pro Shop":     {"url": "https://anaheimteamstore.com/collections/sale/jersey"},
    "Arizona Sports Shop":  {"url": "https://arizonasportsshop.com/collections/sale"},
    "Boston Pro Shop":      {"url": "https://bostonproshop.com/shop-bruins/jerseys/?_bc_fsnf=1&brand%5B%5D=40&brand%5B%5D=51"},
    "Carolina Pro Shop":    {"url": "https://carolinaproshop.com/collections/clearance/jerseys"},

}

# TODO: define a currency for each?
scrapers = {
    "NHLShop Canada": FanaticsProductScraper("https://www.nhlshop.ca/en/men-jerseys/ga-23+d-50117028+os-90+z-97000-3006405570"),
    "FanaticsUSA": FanaticsProductScraper("https://www.fanatics.com/nhl/men-jerseys/o-1362+ga-56+d-08555612+os-78+z-914-677297166"),
    "HockeyAuthentic": HockeyAuthenticProductScraper("https://hockeyauthentic.com/products.json?page=1"),
    "CoolHockey": CoolHockeyProductScraper("https://www.coolhockey.com/ca/sale.html"),
    "AnaheimTeamStore": AnaheimTeamStoreProductScraper("https://anaheimteamstore.com/products.json?page=1"),
    "CarolinaProShop": CarolinaProShopProductScraper("https://carolinaproshop.com/products.json?page=1"),
    "ColoradoTeamStore": ColoradoTeamStoreProductScraper("https://www.altitudeauthentics.com/products.json?page=1"),
    "VanBase": VanbaseProductScraper("https://vanbase.ca/products.json?page=1")

}