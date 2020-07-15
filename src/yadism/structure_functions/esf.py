# -*- coding: utf-8 -*-
"""
This module provides the base classes that define the interface for Structure
Function calculation on a given kinematic point (x, Q2) (that is why they are
called *Evaluated*).
They are:

:py:class:`EvaluatedStructureFunction` :
    this is a pure abstract class, that define the interface (defining the way
    in which coefficient functions are actually encoded) and implement some
    shared methods (like initializer and :py:meth:`get_output`, responsible also
    for :ref:`local caching<local-caching>`.

:py:class:`EvaluatedStructureFunctionLight` :
    this class is inheriting from the former, factorizing some common procedure
    needed for light calculation.

:py:class:`EvaluatedStructureFunctionHeavy` :
    this class is inheriting from the former, factorizing some common procedure
    needed for heavy quark calculation, like auxiliary variable definition,
    threshold passing calculation or directly setting to 0 some coefficient
    functions.
"""

import abc
import copy

import numpy as np

from . import distribution_vec as conv
from .esf_result import ESFResult


class EvaluatedStructureFunction(abc.ABC):
    """
        The actual Structure Function implementation.

        This class is the abstract class that implements the structure for all
        the coefficient functions' providers, for a single kinematic point (x,
        Q2), but all the flavours (singlet, nonsinglet, gluon).

        Since the coefficient functions in general are distributions they are
        provided with an internal representation, that respects the interface
        defined by the class :py:class:`conv.DistributionVec`, and the same
        class is used to perform the convolution with the basis functions (see
        :py:class:`eko.InterpolatorDispatcher`), so the final result will
        consist of an array of dimension 2: one dimension corresponding to the
        interpolation grid, the other to the flavour.

        Its subclasses are organized by:

        - kind: `F2`, `FL`
        - flavour: `light`, `charm`, `bottom`, `top`

        and they all implement a :py:meth:`get_output` method that performs the
        calculation (convolution included), if needed.

        .. _local-caching:

        Caching
        ~~~~~~~

        A part of the overall caching system is implemented at this level.

        The one implemented here is only a **local, isolated** caching, i.e.:

        - the first time the instance is asked for computing the result, through
          the :py:meth:`get_output` method, it registers the result;
        - any following call to the :py:meth:`get_output` method will make use
          of the cached result, and will never recompute it.

        If another instance with the same attributes is asked for the result it
        will recompute it from scratch, because any instance is isolated and
        doesn't keep any reference to the others.

        Parameters
        ----------
            SF : StructureFunction
                the parent :py:class:`StructureFunction` instance, provides an
                interface, holds references to global objects (like managers coming
                from :py:mod:`eko`, e.g. :py:class:`InterpolatorDispatcher`) and
                implements the global caching
            kinematics : dict
                the specific kinematic point as a dict with two elements ('x', 'Q2')

    """

    def __init__(self, SF, kinematics: dict):
        r"""
            Internal Attributes
            -------------------

            _SF :
                parent :py:class:`StructureFunction` reference
            _x :
                momentum fraction
            _Q2 :
                process energy
        """

        x = kinematics["x"]
        if 1 < x <= 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1]")
        if kinematics["Q2"] <= 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")
        # check domain
        if x < min(SF.interpolator.xgrid_raw):
            raise ValueError(f"x outside xgrid - cannot convolute starting from x={x}")

        self._SF = SF
        self._x = x
        self._Q2 = kinematics["Q2"]
        self._res = ESFResult(x=self._x, Q2=self._Q2)
        self._computed = False
        # self.components = {
        #    "g": (self.gluon_0, self.gluon_1, self.gluon_1_fact),
        #    "q": (self.quark_0, self.quark_1, self.quark_1_fact)
        # }

    @property
    @abc.abstractmethod
    def components(self):
        pass

    @abc.abstractmethod
    def _compute_weights(self):
        """
            Compute PDF weights for different channels.

            Returns
            -------
                weights : dict
                    dictionary with key refering to the channel and a dictionary with pid -> weight
        """

    def _compute_local(self):
        """
            Here is where the local caching is actually implemented: if the
            coefficient functions are already computed don't do nothing,
            otherwise call :py:meth:`_compute_component` (checks are per flavour).

            In any case no output is provided, but the result is stored in
            instance's attributes (this method is for internal use).
        """
        # something to do?
        if self._computed:
            return
        # run
        for comp, fncs in self.components.items():
            self._res.values[comp], self._res.errors[comp] = self._compute_component(
                *fncs
            )
        # add the factor x from the LHS
        self._res *= self._x
        # setup weights
        self._res.weights = self._compute_weights()

    def _compute_component(self, f_LO, f_NLO, f_NLO_fact):
        """
            Perform coefficient function calculation for a single flavour,
            combining orders, compute the convolution through
            :py:meth:`DistributionVec.convolution` iterating over *basis
            functions* and take care of scale variations.

            Parameters
            ----------
            f_LO : callable, or sequence of callables
                implements LO coefficient function
            f_NLO : callable, or sequence of callables
                implements NLO coefficient function
            f_NLO_fact : callable, or sequence of callables
                implements NLO factorization scheme contribution

            .. todo::
                reference needed for factorization scheme
        """
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(f_LO())
        if self._SF.pto > 0:
            a_s = self._SF.strong_coupling.a_s(self._Q2 * self._SF.xiR ** 2)
            d_vec += a_s * (
                conv.DistributionVec(f_NLO())
                + 2  # TODO: to be understood
                * (-np.log(self._SF.xiF ** 2))
                * conv.DistributionVec(f_NLO_fact())
            )

        # iterate all polynomials
        for polynomial_f in self._SF.interpolator:
            cv, ecv = d_vec.convolution(self._x, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return np.array(ls), np.array(els)

    @abc.abstractmethod
    def get_result(self):
        """
            .. todo::
                docs
        """

    def get_output(self) -> dict:
        """
           Returns the output for this instance.

           In particular it returns the convolution of the coefficient function
           for the selected observable and the array of basis functions, so the
           result will be an array itself, running over the interpolation grid.

           Caching is provided as explained in the class description (see
           :py:class:`EvaluatedStructureFunction`).

            Returns
            -------
            dict
                a collection of the output arrays with the following structure:

                - `x`: the input momentum fraction
                - `Q2`: the input process scale
                - `q`: a :py:meth:`numpy.array` for the quark coefficient
                  functions
                - `q_error`: a :py:meth:`numpy.array` with the integration
                  errors for `q` calculation
                - `g`: a :py:meth:`numpy.array` for the gluon coefficient
                  functions
                - `g_error`: a :py:meth:`numpy.array` with the integration
                  errors for `g` calculation

        """
        return self.get_result().get_raw()


class EvaluatedStructureFunctionLight(
    EvaluatedStructureFunction
):  # pylint:disable=abstract-method
    """
        Parent class for the light ESF implementations -
        really meaning up, down, and strange quark contributions.
    """

    def __init__(self, SF, kinematics: dict, nf=3):  # 3 = u+d+s
        super(EvaluatedStructureFunctionLight, self).__init__(SF, kinematics)
        # expose number of flavours
        self.nf = nf

    def _compute_weights(self):
        """
            Compute PDF weights for different channels.

            Returns
            -------
                weights : dict
                    dictionary with key refering to the channel and a dictionary with pid -> weight
        """
        weights = {"q": {}, "g": {}}
        # quark couplings
        tot_ch_sq = 0
        for q in range(1, 3 + 1):  # u+d+s
            eq2 = self._SF.coupling_constants.get_weight(q, self._Q2)
            weights["q"][q] = eq2
            tot_ch_sq += eq2
        # gluon coupling = charge average (omitting the *2/2)
        weights["g"][21] = tot_ch_sq / 3  # 3 = u+d+s
        return weights

    def get_result(self):
        """
            .. todo::
                docs
        """
        self._compute_local()

        return copy.deepcopy(self._res)


class EvaluatedStructureFunctionHeavy(EvaluatedStructureFunction):
    """
        Specialize EvaluatedStructureFunction for heavy flavours.

        This class factorizes some common tasks needed for heavy flavours
        (namely: charm, bottom and top quarks), in particular:

        - compute some auxiliary derived variables at initialization time
        - check if the available energy for heavy quark production is above the
          mass threshold of the quark itself (returning immediately 0 otherwise)
        - set :py:meth:`quark_0` and :py:meth:`quark_1` (and the factorization
          scheme contributions corresponding to both gluon and quark, since the
          LO is completely null) to 0

        Parameters
        ----------
            SF : StructureFunction
                the parent :py:class:`StructureFunction` instance, provides an
                interface, holds references to global objects (like managers coming
                from :py:mod:`eko`, e.g. :py:class:`InterpolatorDispatcher`) and
                implements the global caching
            kinematics : dict
                the specific kinematic point as a dict with two elements ('x', 'Q2')
            nhq : int
                heavy quark flavor number, i.e. c=4,b=5,t=6
            force_local : bool
                always return the local object? i.e. ignore e.g. scheme

        Methods
        -------
            get_output()
                compute the coefficient functions (see :py:class:`EvaluatedStructureFunction`)
    """

    def __init__(self, SF, kinematics: dict, nhq: int, force_local: bool = False):
        """
            collect electric charge (relevant for heavy flavours coefficient
            functions) and compute common derived variables

            .. todo::
                - document prefactor: FH page 61 (6.1), 65 (7.2) - Vogt page 21 (4.1)
                - a_s expansion factor already included (simplify with alpha_s/4pi)
                  pay attention to Vogt 1/x in (4.1) in FH appendix are written
                  the expressions for c's (6.1), convolution defined in (7.2)
                  also the charge average 9 / 2 is coming from Vogt (4.1)
                  definition in the gluon
                - remember that is only for the gluon and quark singlet, so it
                  should be removed from the non-singlet prefactor
                - why is it not the pdf but xpdf used? check why Laenen is using
                  xpdf in the first place
                - docs
        """
        super(EvaluatedStructureFunctionHeavy, self).__init__(SF, kinematics)

        self._nhq = nhq
        self._force_local = force_local
        # FH - Vogt comparison prefactor
        self._FHprefactor = self._Q2 / (np.pi * self._SF.M2hq)

        # common variables
        self._rho_q = -4 * self._SF.M2hq / self._Q2
        self._rho = lambda z: -self._rho_q * z / (1 - z)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

    def get_result(self):
        """
            .. todo::
                docs
        """
        # get our local active number of flavors
        nf = self._SF.threshold.get_areas(self._Q2 * self._SF.xiF ** 2)[-1].nf
        # use local only? i.e. by force or because we (Q2) are below our threshold (name)
        if self._force_local or nf < self._nhq:
            self._compute_local()
        else:
            # compute zero-mass part
            obs_name = self._SF.obs_name
            res_light = self._SF.get_esf(
                obs_name.apply_flavor("light"), {"x": self._x, "Q2": self._Q2}, 1
            ).get_result()
            # readjust the weights
            ehq = self._SF.coupling_constants.get_weight(self._nhq, self._Q2)
            res_light.weights = {"g": {21: ehq}, "q": {self._nhq: ehq}}
            # now checkout scheme:
            # matching is only needed for FONLL and in there only if we just crossed our threshold
            # otherwise we continue with the ZM expressions (in contrast to APFEL which treats only
            # F2c in this way)
            # FONLL-A corresponds to (strict) APFEL
            # FONLL-A' reduces to the ZM-VFNS scheme if above the next threshold (which would numerically happen anyway)
            scheme = self._SF.threshold.scheme
            if (scheme == "FONLL-A" and nf >= self._nhq) or (
                scheme == "FONLL-A'" and nf == self._nhq
            ):
                # collect all parts
                res_heavy = self._SF.get_esf(
                    obs_name, {"x": self._x, "Q2": self._Q2}, force_local=True
                ).get_result()
                res_asy = self._SF.get_esf(
                    obs_name.get_asy(), {"x": self._x, "Q2": self._Q2}
                ).get_result()
                # add damping
                damp = 1
                if self._SF.FONLL_damping:
                    power = self._SF.damping_powers[self._nhq - 3]
                    damp = np.power(1.0 - self._SF.M2hq / self._Q2, power)
                # join all
                self._res = res_heavy.suffix(f"_{scheme}_heavy") + damp * (
                    res_light.suffix(f"_{scheme}_light")
                    - res_asy.suffix(f"_{scheme}_asymptotic")
                )
            else:
                self._res = res_light

        return copy.deepcopy(self._res)

    def is_below_threshold(self, z):
        """
            check if available energy is below production threshold or not

            .. todo::
                use threshold on shat or using FH's zmax?
        """
        shat = self._Q2 * (1 - z) / z
        return shat <= 4 * self._SF.M2hq

    def quark_0(self) -> float:
        return 0

    def quark_1(self):
        return 0

    def quark_1_fact(self):
        """
            .. todo::
                docs
        """
        return 0

    def _compute_weights(self):
        """
            Compute PDF weights for different channels.

            Returns
            -------
                weights : dict
                    dictionary with key refering to the channel and a dictionary with pid -> weight
        """
        e2hq = self._SF.coupling_constants.get_weight(self._nhq, self._Q2)
        weights = {"q": {1: e2hq, 2: e2hq, 3: e2hq}, "g": {21: e2hq}}
        return weights

    @abc.abstractmethod
    def _gluon_1(self):
        pass

    def gluon_1(self):
        """
            returns gluon coefficient function at order 1 in :math:`alpha_s`
            (delegated to internal :py:meth:`_gluon_1`) checking before for
            production threshold
        """
        s_h = self._Q2 * (1 - self._x) / self._x
        if s_h <= 4 * self._SF.M2hq:
            return 0
        else:
            return self._gluon_1()

    def gluon_1_fact(self):
        """
            .. todo::
                docs
        """
        return 0
