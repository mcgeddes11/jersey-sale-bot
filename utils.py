import re

# TODO: universal implementation
def price_formatter(price_string: str) -> float:
    match_result = re.findall(r"\$?[0-9]{1,}\.?[0-9]{2}", price_string)
    if len(match_result) == 0:
        raise Exception("Regex failed to extract price")
    elif len(match_result) > 1:
        raise Exception("Regex matched multiple prices")
    else:
        return float(match_result[0].replace("$",""))
