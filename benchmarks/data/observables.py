import pathlib
import sys
from datetime import datetime

import tinydb
import numpy as np

# import yaml

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from apfel_utils import (  # pylint:disable=import-error,wrong-import-position
    str_datetime,
)

db = tinydb.TinyDB(here / "input.json")
obs_table = db.table("observables")
# for the time being the table is freshly generated at each run of this script
obs_table.truncate()

observables = [
    "F2light",
    "F2charm",
    "F2bottom",
    "F2top",
    "FLlight",
    "FLcharm",
    "FLbottom",
    "FLtop",
]

# keep in mind, that in TMC xi < x
# np.linspace(0.1, 1.0, 20),
xgrid = np.unique(
    np.concatenate([np.logspace(-4, np.log10(0.15), 20), np.linspace(0.15, 1.0, 12)])
)
# with open("apfel_xg.yaml") as o:
#    xgrid = yaml.safe_load(o)
# xgrid = xgrid.split()
# xgrid = [float(x[1:]) for x in xgrid]
# xgrid = xgrid[-6:]
# xgrid = np.array(xgrid)

polynomial_degree = 1
is_log_interpolation = True

kinematics = []
# fixed Q2
kinematics.extend([dict(x=x, Q2=90.0) for x in xgrid[6:7].tolist()])
#kinematics.extend([dict(x=x, Q2=90.0) for x in np.logspace(-3, -1, 12).tolist()])
#kinematics.extend([dict(x=x, Q2=90.0) for x in np.linspace(0.15, 0.9, 12).tolist()])
# fixed x
#kinematics.extend([dict(x=0.8, Q2=Q2) for Q2 in np.logspace(1.5, 2.5, 6).tolist()])

# iterate over observables (one dict for each)
for sf in observables:
    content = dict(
        xgrid=xgrid.tolist(),
        polynomial_degree=polynomial_degree,
        is_log_interpolation=is_log_interpolation,
        prDIS="EM",
        comments="",
        _modify_time=str_datetime(datetime.now()),
    )
    content[sf] = kinematics

    obs_table.insert(content)
