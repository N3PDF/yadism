# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quarks
"""

# TODO

import numpy as np

from . import partonic_channel as pccc
from .. import splitting_functions as split


class F2heavyQuark(pccc.PartonicChannelHeavy):
    """
        Computes the quark heavy quark channel of F2heavy
    """

    label = "q"

    def LO(self):
        return 0, 0, 1


class F2heavyGluon(pccc.PartonicChannelHeavy):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"

    def NLO(self):
        def reg(z):
            c1 = 12.0 * (1 - self.labda) ** 2 - 18 * (1 - self.labda) + 8 # =12l^2 - 6l +2
            c2 = (1.0 - self.labda) / (1.0 - self.labda * z) - 1.0
            c3 = 6.0 * self.labda
            c4 = -12.0 * self.labda
            return (
                (split.pqg(z, self.constants) * (self.l_labda(z) - np.log(self.labda)))
                + self.h_g(z, [c1, c2, c3, c4])
            ) * 2

        return reg
