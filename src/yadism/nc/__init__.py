# -*- coding: utf-8 -*-

import copy

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f3_light import F3lightQuark
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f3_heavy import F3heavyQuarkVA
from .f2_asy import F2asyGluonVV, F2asyGluonAA
from .fl_asy import FLasyGluonVV, FLasyGluonAA
from .f3_asy import F3asyQuarkVA

from .weights import light_factory, heavy_factory

partonic_channels_em = {
    "F2light": [F2lightQuark, F2lightGluon],
    "FLlight": [FLlightQuark, FLlightGluon],
    "F3light": [F3lightQuark],
    "F2heavy": [F2heavyGluonVV],
    "FLheavy": [FLheavyGluonVV],
    "F3heavy": [],
    "F2asy": [F2asyGluonVV],
    "FLasy": [FLasyGluonVV],
    "F3asy": [],
}

# in NC for HQ new channels open: gluon_aa
partonic_channels_nc = copy.deepcopy(partonic_channels_em)
partonic_channels_nc["F2heavy"].extend([F2heavyGluonAA])
partonic_channels_nc["FLheavy"].extend([FLheavyGluonAA])
partonic_channels_nc["F3heavy"].extend([F3heavyQuarkVA])
partonic_channels_nc["F2asy"].extend([F2asyGluonAA])
partonic_channels_nc["FLasy"].extend([FLasyGluonAA])
partonic_channels_nc["F3asy"].extend([F3asyQuarkVA])


def weights_nc(obs_name):
    if obs_name.flavor == "light":
        return light_factory(obs_name.kind, range(1, 3 + 1))
    elif obs_name.flavor_family == "light":
        # so it's heavylight
        return light_factory(obs_name.kind, [obs_name.hqnumber])
    return heavy_factory(obs_name.kind, obs_name.hqnumber)
