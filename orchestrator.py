from website_enums import scrapers
import pandas
import os
from multiprocessing import Pool
from datetime import datetime

previous_version_path = "last_version.pkl"


if __name__ == '__main__':

    # Get a multiprocessing pool with default number of workers
    process_pool = Pool()

    # Scrape asynchronously
    results = [process_pool.apply_async(scraper_obj.get_all_products, args=(site_name, )) for site_name, scraper_obj in scrapers.items()]

    # Collect the results
    output = [p.get() for p in results]
    product_master_list = [item for sublist in output for item in sublist]

    # TODO: filter out kids, youth, infant, pets shit?

    # Convert to dataframe
    dfout = pandas.DataFrame.from_records(product_master_list)

    # Create deterministic hash
    dfout["deterministic_hash"] = pandas.util.hash_pandas_object(dfout, index=False)

    # # Compare to previous version
    # if not os.path.exists(previous_version_path):
    #     dfout.to_pickle(previous_version_path)
    # else:
    #     dfold = pandas.read_pickle(previous_version_path)
    #     # TODO: comparison here
    #     # TODO: do we want to exclude price from deterministic has to detect price changes for existing products?
    #     # We want to detect:
    #     # 1. existing products that have decreased in price
    #     # 2. New products on sale
    #     # Note that we don't care if products have dropped off the sale list
    #     # Left join/merge dfout -> dfold on deterministic_hash should give us the mismatches





