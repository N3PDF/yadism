import pathlib

import yaml
import numpy as np

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

xgrid = np.unique(np.concatenate([np.logspace(-4, -1, 40), np.linspace(0.1, 0.99, 20)]))
polynomial_degree = 4
is_log_interpolation = True

kinematics = []
# fixed Q
kinematics.extend([dict(x=x, Q2=90.0) for x in np.logspace(-3, -1, 6).tolist()])
kinematics.extend([dict(x=x, Q2=90.0) for x in np.linspace(0.15, 0.9, 6).tolist()])
# fixed x
kinematics.extend([dict(x=0.1, Q2=Q2) for Q2 in np.logspace(1.5, 2.5, 6).tolist()])

for sf in observables:
    content = dict(
        xgrid=xgrid.tolist(),
        polynomial_degree=polynomial_degree,
        is_log_interpolation=is_log_interpolation,
    )
    content[sf] = kinematics

    fn = pathlib.Path(__file__).absolute().parent / f"{sf}.yaml"
    with open(fn, "w") as f:
        yaml.safe_dump(content, f)
