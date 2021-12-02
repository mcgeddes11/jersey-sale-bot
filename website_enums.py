from scrapers import FanaticsProductScraper, HockeyAuthenticProductScraper, CoolHockeyProductScraper, \
     AnaheimTeamStoreProductScraper, BuffaloTeamStoreProductScraper, CalgaryFlamesportProductScraper, \
     CarolinaProShopProductScraper, ChicagoTeamStoreProductScraper, ColoradoTeamStoreProductScraper, \
     DallasTeamStoreProductScraper, NewJerseyTeamStore, NewYorkRangersTeamStore, OttawaTeamStoreProductScraper, \
     SeattleTeamStoreProductScraper, VanbaseProductScraper, VegasTeamStoreProductScraper, \
     WinnipegTeamStoreProductScraper

# TODO: define a currency for each?
scrapers = {
    "NHLShop Canada": FanaticsProductScraper("https://www.nhlshop.ca/en/men-jerseys/ga-23+d-50117028+os-90+z-97000-3006405570"),  # Validated
    "FanaticsUSA": FanaticsProductScraper("https://www.fanatics.com/nhl/men-jerseys/o-1362+ga-56+d-08555612+os-78+z-914-677297166"), # Validated
    "HockeyAuthentic": HockeyAuthenticProductScraper("https://hockeyauthentic.com/products.json?page=1"), # Validated
    "CoolHockey": CoolHockeyProductScraper("https://www.coolhockey.com/ca/sale.html"), # Validated
    "AnaheimTeamStore": AnaheimTeamStoreProductScraper("https://anaheimteamstore.com/products.json?page=1"), # Validated
    "BuffaloTeamStore": BuffaloTeamStoreProductScraper("https://shoponebuffalo.com/products.json?page=1"), # Validated
    "CarolinaProShop": CarolinaProShopProductScraper("https://carolinaproshop.com/products.json?page=1"), # Validated
    "CalgaryFlamesport": CalgaryFlamesportProductScraper("https://www.flamesport.com/products.json?page=1"), # Validated
    "ColoradoTeamStore": ColoradoTeamStoreProductScraper("https://www.altitudeauthentics.com/products.json?page=1"), # Validated
    "ChicagoTeamStore": ChicagoTeamStoreProductScraper("https://cbhshop.com/products.json?page=1"), # Validated
    "DallasTeamStore": DallasTeamStoreProductScraper("https://hangarhockey.com/products.json?page=1"), # Validated
    "NewJerseyTeamStore": NewJerseyTeamStore("https://devilsdenshop.com/products.json?page=1"), # Validated
    "NewYorkRangersTeamStore": NewYorkRangersTeamStore("https://shop.msg.com/products.json?page=1"), # Validated
    "OttawaTeamStore": OttawaTeamStoreProductScraper("https://ottawateamshop.ca/products.json?page=1"), # Validated
    "SeattleTeamStore": SeattleTeamStoreProductScraper("https://seattlehockeyteamstore.com/products.json?page=1"), # Validated
    "VanBase": VanbaseProductScraper("https://vanbase.ca/products.json?page=1"), # Validated
    "VegasTeamStore": VegasTeamStoreProductScraper("https://vegasteamstore.com/products.json?page=1"),
    "WinnipegTeamStore": WinnipegTeamStoreProductScraper("https://truenorthshop.com/products.json?page=1")# Validated

}