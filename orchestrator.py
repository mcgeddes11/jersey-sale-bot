from website_enums import scrapers
import pandas
import os
from multiprocessing import Queue, Process

previous_version_path = "last_version.pkl"


if __name__ == '__main__':

    # Get the new product master list
    # TODO: implement multiprocessing
    product_master_list = []
    n_sites = len(scrapers.items())
    count = 1

    for site_name, scraper in scrapers.items():
        print("Getting deals from {}, site {} of {}...".format(site_name, count, n_sites))
        scraper.get_all_products(site_name)
        product_master_list = product_master_list + scraper.products
        count += 1

    # TODO: filter out kids, youth, infant, pets shit?

    # Convert to dataframe
    dfout = pandas.DataFrame.from_records(product_master_list)

    # Create deterministic hash
    dfout["deterministic_hash"] = pandas.util.hash_pandas_object(dfout, index=False)

    # Compare to previous version
    if not os.path.exists(previous_version_path):
        dfout.to_pickle(previous_version_path)
    else:
        dfold = pandas.read_pickle(previous_version_path)
        # TODO: comparison here
        # TODO: do we want to exclude price from deterministic has to detect price changes for existing products?
        # We want to detect:
        # 1. existing products that have decreased in price
        # 2. New products on sale
        # Note that we don't care if products have dropped off the sale list
        # Left join/merge dfout -> dfold on deterministic_hash should give us the mismatches





