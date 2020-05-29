# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

Differently from the :py:mod:`FLheavy` here more classes are provided, since
its flavour can be individually selected. Nevertheless a common class is also
defined, :py:class:`ESF_FLheavy`, to factorize all the common structure related
to heavy flavours; the common class is a further intermediate node in the
hierarchy, since it is a direct child of :py:class:`ESFH` (it is actually the
FL flavoured version of :py:class:`ESFH`) at it is the direct ancestor for the
individual flavour ones.

Actually the coefficient functions formulas are encoded already at the level of
:py:class:`ESF_FLheavy`, while the explicit leaf classes are used to handle the
differences between flavours (e.g. electric charge).

The main reference used is: :cite:`felix-thesis`.

"""

import numpy as np

from .esf import EvaluatedStructureFunctionHeavy as ESFH


class EvaluatedStructureFunctionFLheavy(ESFH):
    """
        Compute FL structure functions for heavy quark flavours.

        This class inherits from :py:class:`ESFH`, providing only the formulas
        for coefficient functions, while all the machinery for dealing with
        distributions, making convolution with PDFs, and packaging results is
        completely defined in the parent (and, mainly, in its own parent).

        Even if this is still an intermediate class it has already enough
        information to be able to express coefficient functions, while children
        are used just ot handle differences among flavours (e.g. electric
        charge).

    """

    def _gluon_1(self):
        """
            Computes the gluon part of the next to leading order FL structure
            function.

            |ref| implements :eqref:`D.2`, :cite:`felix-thesis`.

            Returns
            -------
            sequence of callables
                coefficient functions, as two arguments functions: :py:`(x, Q2)`

            Note
            ----
            Immediately check if the available energy is below threshold for
            flavour production (no other calculation is needed nor performed in
            this case).

        """
        CF = self._SF.constants.CF

        def cg(z):
            if self.is_below_threshold(z):
                return 0
            # fmt: off
            return  self._FHprefactor * self._charge_em ** 2 * (
                3 * CF / 4
                * (-np.pi * self._rho_p(z) ** 3) / (self._rho(z) * self._rho_q)
                * (2 * self._beta(z) + self._rho(z) * np.log(self._chi(z)))
            ) / z
            # fmt: on

        return cg


class EvaluatedStructureFunctionFLcharm(EvaluatedStructureFunctionFLheavy):
    """
        Compute FL structure functions for *charm* quark.

        All the definitions and expression are already given at the level of
        :py:class:`ESF_FLheavy`.
        Currently this class sets only:

        - electric charge = 2/3

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLcharm, self).__init__(
            SF, kinematics, charge_em=2 / 3
        )


class EvaluatedStructureFunctionFLbottom(EvaluatedStructureFunctionFLheavy):
    """
        Compute FL structure functions for *bottom* quark.

        All the definitions and expression are already given at the level of
        :py:class:`ESF_FLheavy`.
        Currently this class sets only:

        - electric charge = 1/3

    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLbottom, self).__init__(
            SF, kinematics, charge_em=1 / 3
        )


class EvaluatedStructureFunctionFLtop(EvaluatedStructureFunctionFLheavy):
    """
        Compute FL structure functions for *top* quark.

        All the definitions and expression are already given at the level of
        :py:class:`ESF_FLheavy`.
        Currently this class sets only:

        - electric charge = 2/3
    """

    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionFLtop, self).__init__(
            SF, kinematics, charge_em=2 / 3
        )