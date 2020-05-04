# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DIS calculations.

.. todo::
    docs
"""
from typing import Any

import numpy as np

from eko.interpolation import InterpolatorDispatcher
from eko.constants import Constants
from eko.thresholds import Threshold
from eko.alpha_s import StrongCoupling

from .output import Output
from .structure_functions import (
    F2_light,
    FL_light,
    F2_charm,
    F2_bottom,
    F2_top,
    FL_charm,
    FL_bottom,
    FL_top,
)


class Runner:
    """Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution.
    observables : dict
        Description of parameter `observables`.

    .. todo::
        docs
    """

    __obs_templates = {
        "F2light": (F2_light,),
        "F2charm": (F2_charm, "mc"),
        "F2bottom": (F2_bottom, "mb"),
        "F2top": (F2_top, "mt"),
        "FLlight": (FL_light,),
        "FLcharm": (FL_charm, "mc"),
        "FLbottom": (FL_bottom, "mb"),
        "FLtop": (FL_top, "mt"),
    }

    def __init__(self, theory: dict, observables: dict):
        self._theory = theory
        self._observables = observables
        self._n_f: int = theory["NfFF"]

        polynomial_degree: int = observables["polynomial_degree"]
        self._interpolator = InterpolatorDispatcher(
            observables["xgrid"],
            polynomial_degree,
            log=observables.get("is_log_interpolation", True),
            mode_N=False,
            numba_it=False,  # TODO: make it available for the user to choose
        )

        # ==========================
        # create physics environment
        # ==========================
        self._constants = Constants()

        FNS = theory["FNS"]
        q2_ref = pow(theory["Q0"], 2)
        if FNS != "FFNS":
            qmc = theory["Qmc"]
            qmb = theory["Qmb"]
            qmt = theory["Qmt"]
            threshold_list = pow(np.array([qmc, qmb, qmt]), 2)
            nf = None
        else:
            nf = theory["NfFF"]
            threshold_list = None
        self._threshold = Threshold(
            q2_ref=q2_ref, scheme=FNS, threshold_list=threshold_list, nf=nf
        )

        # Now generate the operator alpha_s class
        alpha_ref = theory["alphas"]
        q2_alpha = pow(theory["Qref"], 2)
        self._alpha_s = StrongCoupling(
            self._constants, alpha_ref, q2_alpha, self._threshold
        )

        self._xiF = theory["XIF"]

        # ==============================
        # initialize structure functions
        # ==============================
        default_args = dict(
            interpolator=self._interpolator,
            constants=self._constants,
            threshold=self._threshold,
            alpha_s=self._alpha_s,
            pto=theory["PTO"],
            xiR=theory["XIR"],
            xiF=self._xiF,
        )
        self._observable_instances = []
        for sf, obs_t in self.__obs_templates.items():
            # if not in the input skip
            if sf not in self._observables:
                continue

            # first element is the class [required]
            if len(obs_t) == 1:
                obj = obs_t[0](**default_args)
            # if second element specified is the key for the mass
            elif len(obs_t) == 2:
                obj = obs_t[0](**default_args, M2=theory[obs_t[1]] ** 2,)
            else:
                raise RuntimeError("Invalid obs template")

            # read kinematics
            obj.load(self._observables.get(obj.name, []))
            self._observable_instances.append(obj)

        # prepare output
        self._output = Output()
        self._output["xgrid"] = self._interpolator.xgrid_raw
        self._output["xiF"] = self._xiF

    def get_output(self) -> Output:
        """
        .. todo::
            docs
        """
        for obs in self._observable_instances:
            self._output[obs.name] = obs.get_output()

        return self._output

    def __call__(self, pdfs: Any) -> dict:
        """
        Returns
        -------
        dict
            dictionary with all computed processes

        .. todo::
            docs
        """

        return self.get_output().apply_PDF(pdfs)

    def apply(self, pdfs: Any) -> dict:
        """
        .. todo::
            - implement
            - docs
        """
        return self(pdfs)

    def clear(self) -> None:
        """
        Or 'restart' or whatever

        .. todo::
            - implement
            - docs
        """
        pass

    def dump(self) -> None:
        """
        If any output available ('computed') dump the current output on file

        .. todo::
            - implement
            - docs
        """
        return self.get_output().dump()