
# TODO: universal implementation
def price_formatter(price_string: str) -> float:
    return float(price_string.replace("$","").replace("CAD","").strip())
