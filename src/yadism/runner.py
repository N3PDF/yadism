# -*- coding: utf-8 -*-
"""
This module contains the main loop for the DIS calculations.

There are two ways of using ``yadism``:

* ``Runner``: this class provides a runner that get the *theory* and
  *observables* descriptions as input and manage the whole observables'
  calculation process
* ``run_dis``: a function that wraps the construction of a ``Runner`` object
  and calls the proper method to get the requested output

.. todo::
    decide about ``run_dis`` and document it properly in module header
"""
from typing import Any
import time
import inspect
import logging
import io
import copy

import rich
import rich.align
import rich.panel
import rich.box
import rich.progress
import rich.markdown
import rich.console

from eko.interpolation import InterpolatorDispatcher
from eko import thresholds
from eko import strong_coupling
from eko import basis_rotation as br

from .input import inspector, compatibility
from . import observable_name
from . import log
from .output import Output
from .sf import StructureFunction as SF
from .coupling_constants import CouplingConstants

log.setup()
logger = logging.getLogger(__name__)


class Runner:
    """
    Wrapper to compute a process

    Parameters
    ----------
    theory : dict
        Dictionary with the theory parameters for the evolution (currently
        including PDFSet and DIS process indication).
    observables : dict
        DIS parameters: process description, kinematic specification for the
        requested output.

    Notes
    -----
    For a full description of the content of `theory` and `dis_observables`
    dictionaries read ??.

    .. todo::
        * reference on theory template
        * detailed description of dis_observables entries

    """

    banner = rich.align.Align(
        rich.panel.Panel.fit(
            inspect.cleandoc(
                r"""  __     __       _ _
                     \ \   / /      | (_)
                      \ \_/ /_ _  __| |_ ___ _ __ ___
                       \   / _` |/ _` | / __| '_ ` _ \
                        | | (_| | (_| | \__ \ | | | | |
                        |_|\__,_|\__,_|_|___/_| |_| |_|
                """
            ),
            rich.box.SQUARE,
            padding=1,
            style="magenta",
        ),
        "center",
    )

    def __init__(self, theory: dict, observables: dict):
        # ==============================
        # Validate inputs
        # ==============================
        insp = inspector.Inspector(theory, observables)
        insp.perform_all_checks()

        # ==============================
        # Store inputs
        # ==============================
        self._theory = theory
        self._observables = observables

        # ==============================
        # Setup eko stuffs
        # ==============================
        new_theory = compatibility.update(theory)
        self.interpolator = InterpolatorDispatcher.from_dict(observables, mode_N=False)
        self.threshold = thresholds.ThresholdsAtlas.from_dict(new_theory, "kDIS")
        self.strong_coupling = strong_coupling.StrongCoupling.from_dict(new_theory)

        # Non-eko theory
        self.coupling_constants = CouplingConstants.from_dict(theory, observables)
        self.xiF = theory["XIF"]

        # ==============================
        # Initialize structure functions
        # ==============================
        eko_components = dict(
            interpolator=self.interpolator,
            threshold=self.threshold,
            alpha_s=self.strong_coupling,
            coupling_constants=self.coupling_constants,
        )
        # FONLL damping powers
        FONLL_damping = bool(theory["DAMP"])
        if FONLL_damping:
            damping_power = theory.get("DAMPPOWER", 2)
            damping_power_c = theory.get("DAMPPOWERCHARM", damping_power)
            damping_power_b = theory.get("DAMPPOWERBOTTOM", damping_power)
            damping_power_t = theory.get("DAMPPOWERTOP", damping_power)
            damping_powers = [damping_power_c, damping_power_b, damping_power_t]
        else:
            damping_powers = [2] * 3
        # pass theory params
        intrinsic_range = []
        if theory["IC"] == 1:
            intrinsic_range.append(4)
        theory_params = dict(
            pto=theory["PTO"],
            xiR=theory["XIR"],
            xiF=self.xiF,
            scheme=theory["FNS"],
            nf_ff=theory["NfFF"],
            intrinsic_range=intrinsic_range,
            m2hq=(theory["mc"] ** 2, theory["mb"] ** 2, theory["mt"] ** 2),
            TMC=theory["TMC"],
            M2target=theory["MP"] ** 2,
            FONLL_damping=FONLL_damping,
            damping_powers=damping_powers,
        )
        obs_params = dict(process=observables.get("prDIS", "EM"))

        self.observable_instances = {}
        for obs_name in observable_name.ObservableName.all():
            name = obs_name.name

            # initialize an SF instance for each possible structure function
            obj = SF(
                obs_name,
                runner=self,
                eko_components=eko_components,
                theory_params=theory_params,
                obs_params=obs_params,
            )

            # read kinematics
            obj.load(self._observables["observables"].get(name, []))
            self.observable_instances[name] = obj

        # output console
        if log.silent_mode:
            file = io.StringIO()
        else:
            file = None
        self.console = rich.console.Console(file=file)
        # ==============================
        # Initialize output
        # ==============================
        self._output = Output()
        self._output.update(self.interpolator.to_dict())
        self._output["pids"] = br.flavor_basis_pids
        self._output["xiF"] = self.xiF

    def get_result(self, raw=False):
        """
        Compute coefficient functions grid for requested kinematic points.


        .. admonition:: Implementation Note

            get_output pipeline

        Returns
        -------
        :obj:`Output`
            output object, it will store the coefficient functions grid
            (flavour, interpolation-index) for each requested kinematic
            point (x, Q2)


        .. todo::

            * docs
            * get_output pipeline
        """
        self.console.print(self.banner)

        # precomputing the plan of calculation
        precomputed_plan = {}
        printable_plan = []
        for name, obs in self.observable_instances.items():
            if name in self._observables["observables"].keys():
                precomputed_plan[name] = obs
                printable_plan.append(
                    f"- {name} at {len(self._observables['observables'][name])} pts"
                )

        self.console.print(rich.markdown.Markdown("## Plan"))
        self.console.print(rich.markdown.Markdown("\n".join(printable_plan)))

        # running the calculation
        self.console.print(rich.markdown.Markdown("## Calculation"))
        self.console.print("yadism took off! please stay tuned ...")
        start = time.time()
        for name, obs in rich.progress.track(
            precomputed_plan.items(),
            description="computing...",
            transient=True,
            console=self.console,
        ):
            self._output[name] = obs.get_result()
        end = time.time()
        diff = end - start
        self.console.print(f"[cyan]took {diff:.2f} s")

        out = copy.deepcopy(self._output)
        if raw:
            out = out.get_raw()
        return out

    def get_output(self):
        return self.get_result(True)

    def apply_pdf(self, pdfs: Any) -> dict:
        """
        Alias for the `__call__` method.

        .. todo::
            - implement
            - docs
        """
        return self.get_result().apply_pdf(pdfs)

    def clear(self) -> None:
        """
        Or 'restart' or whatever

        .. todo::
            - implement
            - docs
        """

    def dump(self) -> None:
        """
        If any output available ('computed') dump the current output on file

        .. todo::
            - implement
            - docs
        """
        return self.get_output().dump()
