from scrapers import FanaticsProductScraper, HockeyAuthenticProductScraper, CoolHockeyProductScraper, \
     BigCommerceProductScraper, \
     AnaheimTeamStoreProductScraper, BuffaloTeamStoreProductScraper, CalgaryFlamesportProductScraper, \
     CarolinaProShopProductScraper, ChicagoTeamStoreProductScraper, ColoradoTeamStoreProductScraper, \
     DallasTeamStoreProductScraper, LosAngelesTeamStoreProductScraper, NewJerseyTeamStoreProductScraper, \
     NewYorkRangersTeamStore, OttawaTeamStoreProductScraper, SeattleTeamStoreProductScraper, VanbaseProductScraper, \
     VegasTeamStoreProductScraper, WinnipegTeamStoreProductScraper

# TODO: define a currency for each?
scrapers = {
    "NHLShop Canada": FanaticsProductScraper("https://www.nhlshop.ca/en/men-jerseys/ga-23+d-50117028+os-90+z-97000-3006405570", currency="CAD"),  # Validated
    "FanaticsUSA": FanaticsProductScraper("https://www.fanatics.com/nhl/men-jerseys/o-1362+ga-56+d-08555612+os-78+z-914-677297166", currency="USD"), # Validated
    "HockeyAuthentic": HockeyAuthenticProductScraper("https://hockeyauthentic.com/products.json?page=1", currency="CAD"), # Validated
    "CoolHockey": CoolHockeyProductScraper("https://www.coolhockey.com/ca/sale.html", currency="CAD"), # Validated
    "AnaheimTeamStore": AnaheimTeamStoreProductScraper("https://anaheimteamstore.com/products.json?page=1", currency="USD"), # Validated
    "BuffaloTeamStore": BuffaloTeamStoreProductScraper("https://shoponebuffalo.com/products.json?page=1", currency="USD"), # Validated
    "CarolinaProShop": CarolinaProShopProductScraper("https://carolinaproshop.com/products.json?page=1", currency="USD"), # Validated
    "CalgaryFlamesport": CalgaryFlamesportProductScraper("https://www.flamesport.com/products.json?page=1", currency="USD"), # Validated
    "ColoradoTeamStore": ColoradoTeamStoreProductScraper("https://www.altitudeauthentics.com/products.json?page=1", currency="USD"), # Validated
    "ColumbusTeamStore": BigCommerceProductScraper("https://thebluelineonline.com/clear/", currency="USD"), # Validated, not only jerseys though
    "ChicagoTeamStore": ChicagoTeamStoreProductScraper("https://cbhshop.com/products.json?page=1", currency="USD"), # Validated
    "DallasTeamStore": DallasTeamStoreProductScraper("https://hangarhockey.com/products.json?page=1", currency="USD"), # Validated
    "FloridaTeamStore": BigCommerceProductScraper("https://flateamshop.com/sale/", currency="USD"), # Validated, not only jerseys
    "LosAngelesTeamStore": LosAngelesTeamStoreProductScraper("https://teamlastore.com/products.json?page=1", currency="USD"), # Validated
    "NashvilleTeamStore": BigCommerceProductScraper("https://nashvillelockerroom.com/golden-deals/jerseys/", currency="USD"), # Validated
    "NewJerseyTeamStore": NewJerseyTeamStoreProductScraper("https://devilsdenshop.com/products.json?page=1", currency="USD"), # Validated
    "NewYorkRangersTeamStore": NewYorkRangersTeamStore("https://shop.msg.com/products.json?page=1", currency="USD"), # Validated
    "OttawaTeamStore": OttawaTeamStoreProductScraper("https://ottawateamshop.ca/products.json?page=1", currency="CAD"), # Validated
    "PittsburghTeamStore": BigCommerceProductScraper("https://pensgear.com/jerseys/sale-jerseys/", currency="USD"), # Validated
    "SeattleTeamStore": SeattleTeamStoreProductScraper("https://seattlehockeyteamstore.com/products.json?page=1", currency="USD"), # Validated
    "VanBase": VanbaseProductScraper("https://vanbase.ca/products.json?page=1", currency="CAD"), # Validated
    "VegasTeamStore": VegasTeamStoreProductScraper("https://vegasteamstore.com/products.json?page=1", currency="USD"), # Validated
    "WinnipegTeamStore": WinnipegTeamStoreProductScraper("https://truenorthshop.com/products.json?page=1", currency="CAD")# Validated
}