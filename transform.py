import pandas as pd
from datetime import datetime
from pytz import timezone

central_tz = timezone('US/Central')
date_frmt = '%Y%m%d_%H%M'
my_date = datetime.now(central_tz).strftime(date_frmt)
print(my_date)

def extract() -> None:
    return None

def transf() -> None:
    return None

def load() -> None:
    return None

if __name__ == "__main__":
    source_file_name = ""
    # file name format = supplier_name_suppinv_YYYYMMDD_HHmm
    desti_file_name = f""
    extract()
    transf()
    load()