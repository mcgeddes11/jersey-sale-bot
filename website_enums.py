from scrapers import FanaticsProductScraper, HockeyAuthenticProductScraper, CoolHockeyProductScraper, \
     BigCommerceProductScraper, DicksSportingGoodsProductScraper, RiverCitySportsProductScraper, \
     HockeyJerseyOutletProductScraper, SvpSportsProductScraper, \
     AnaheimTeamStoreProductScraper, BuffaloTeamStoreProductScraper, CalgaryFlamesportProductScraper, \
     CarolinaProShopProductScraper, ChicagoTeamStoreProductScraper, ColoradoTeamStoreProductScraper, \
     DallasTeamStoreProductScraper, LosAngelesTeamStoreProductScraper, NewJerseyTeamStoreProductScraper, \
     NewYorkRangersTeamStore, OttawaTeamStoreProductScraper, SeattleTeamStoreProductScraper, StLouisTeamStoreProductScraper, \
     TorontoTeamStoreProductScraper, VanbaseProductScraper, VegasTeamStoreProductScraper, WinnipegTeamStoreProductScraper

# TODO: define a currency for each?
scrapers = {
    "NHLShopCanada": FanaticsProductScraper("https://www.nhlshop.ca/en/men-jerseys/ga-23+d-50117028+os-90+z-97000-3006405570", currency="CAD"),  # Validated
    "FanaticsUSA": FanaticsProductScraper("https://www.fanatics.com/nhl/men-jerseys/o-1362+ga-56+d-08555612+os-78+z-914-677297166", currency="USD"), # Validated
    "HockeyAuthentic": HockeyAuthenticProductScraper("https://hockeyauthentic.com/products.json?page=1", currency="CAD"), # Validated
    "CoolHockey": CoolHockeyProductScraper("https://www.coolhockey.com/ca/sale.html", currency="CAD"), # Validated
    "DicksSportingGoods": DicksSportingGoodsProductScraper("https://prod-catalog-product-api.dickssportinggoods.com/v2/search", currency="USD"), # Validated
    "RiverCitySports": RiverCitySportsProductScraper("https://www.rivercitysports.com/CDA/viewproducts-06.cfm?league=NHL&team=&product=&perPage=249&lastLeague=NHL&lastTeam=&lastProduct=&mode=sale&startAt=1", currency="CAD"), # Validated
    "HockeyJerseyOutlet": HockeyJerseyOutletProductScraper("https://www.hockeyjerseyoutlet.com/products.json?page=1", currency="USD"), # Validated
    "SvpSports": SvpSportsProductScraper("https://www.svpsports.ca/products.json?page=1", currency="CAD"), # Validated
    "AnaheimTeamStore": AnaheimTeamStoreProductScraper("https://anaheimteamstore.com/products.json?page=1", currency="USD"), # Validated
    "BostonTeamStore": BigCommerceProductScraper("https://bostonproshop.com/shop-bruins/sale/", currency='USD'), # Validated
    "BuffaloTeamStore": BuffaloTeamStoreProductScraper("https://shoponebuffalo.com/products.json?page=1", currency="USD"), # Validated
    "CarolinaProShop": CarolinaProShopProductScraper("https://carolinaproshop.com/products.json?page=1", currency="USD"), # Validated
    "CalgaryFlamesport": CalgaryFlamesportProductScraper("https://www.flamesport.com/products.json?page=1", currency="CAD"), # Validated
    "ColoradoTeamStore": ColoradoTeamStoreProductScraper("https://www.altitudeauthentics.com/products.json?page=1", currency="USD"), # Validated
    "ColumbusTeamStore": BigCommerceProductScraper("https://thebluelineonline.com/clear/", currency="USD"), # Validated
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
    "StLouisTeamStore": StLouisTeamStoreProductScraper("https://www.stlauthentics.com/products.json?page=1", currency="USD"), # Validated
    "TampBayTeamStore": BigCommerceProductScraper("https://tampabaysports.com/sale/", currency='USD'), # Validated
    "TorontoTeamStore": TorontoTeamStoreProductScraper("https://shop.realsports.ca/products.json?page=1", currency='CAD'), # Validated
    "VanBase": VanbaseProductScraper("https://vanbase.ca/products.json?page=1", currency="CAD"), # Validated
    "VegasTeamStore": VegasTeamStoreProductScraper("https://vegasteamstore.com/products.json?page=1", currency="USD"), # Validated
    "WashingtonTeamStore": FanaticsProductScraper("https://shop.monumentalsportsnetwork.com/washington-capitals-jerseys/t-25156419+d-7883396305+os-3+z-8-695244688", currency="USD"), # Validated
    "WinnipegTeamStore": WinnipegTeamStoreProductScraper("https://truenorthshop.com/products.json?page=1", currency="CAD")# Validated
}