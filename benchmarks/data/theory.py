import pathlib
import itertools
import sys
from datetime import datetime

import yaml
import tinydb

# import numpy as np
here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from external_utils import (  # pylint:disable=import-error,wrong-import-position
    str_datetime,
)

is_regression = False

if is_regression:
    ask = input("Do you want to refill the regression theories? [y/n]")
    if ask != "y":
        print("Nothing done.")
        exit()

db_name = "regression.json" if is_regression else "input.json"
print(f"writing to {db_name}")
db = tinydb.TinyDB(here / db_name)
theories_table = db.table("theories")
# for the time being the table is freshly generated at each run of this script
theories_table.truncate()

matrix = {
    "PTO": [0, 1],
    "XIR": [0.5, 1.0, 2.0],
    "XIF": [0.5, 1.0, 2.0],
    "TMC": [0, 1, 2, 3],
    "NfFF": [3, 4, 5],
    "FNS": ["FFNS", "ZM-VFNS", "FONLL-A"],
    "DAMP": [0, 1],
}


def my_product(inp):
    """
    Thank you: https://stackoverflow.com/questions/5228158/
    """
    return [
        dict(zip(inp.keys(), values)) for values in itertools.product(*inp.values())
    ]


with open(here / "theory_template.yaml") as f:
    template = yaml.safe_load(f)


for config in my_product(matrix):
    template.update(config)
    template["_modify_time"] = str_datetime(datetime.now())
    theories_table.insert(template)
