# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
import abc

import numpy as np

from . import convolution as conv


class EvaluatedStructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        if 1 < kinematics["x"] < 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1)")
        if kinematics["Q2"] < 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")

        self._SF = SF
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        self._cqv = []
        self._e_cqv = []
        self._cgv = []
        self._e_cgv = []
        self._a_s = self._SF._alpha_s.a_s(self._Q2)
        self._n_f = self._SF._threshold.get_areas(self._Q2)[-1].nf

    def _compute(self):
        """
        .. todo::
            docs
        """
        # something to do?
        if not self._cqv:
            # yes
            self._cqv, self._e_cqv = self._compute_component(self.quark_0, self.quark_1)
        if not self._cgv:
            # yes
            self._cgv, self._e_cgv = self._compute_component(self.gluon_0, self.gluon_1)

    def _compute_component(self, f_LO, f_NLO):
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(f_LO())
        if self._SF._pto > 0:
            d_vec += self._a_s * conv.DistributionVec(f_NLO())

        # iterate all polynomials
        for polynomial_f in self._SF._interpolator:
            cv, ecv = d_vec.convolution(self._x, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return ls, els

    def get_output(self):
        """
        .. todo::
            docs
        """
        self._compute()

        output = {}
        output["x"] = self._x
        output["Q2"] = self._Q2
        output["q"] = self._cqv
        output["q_error"] = self._e_cqv
        output["g"] = self._cgv
        output["g_error"] = self._e_cgv
        return output

    @abc.abstractclassmethod
    def quark_0(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractclassmethod
    def gluon_0(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractclassmethod
    def quark_1(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractclassmethod
    def gluon_1(self):
        """
        .. todo::
            docs
        """
        pass
