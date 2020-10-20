# -*- coding: utf-8 -*-
"""
Provides splitting functions definition for coefficient functions calculation.

The coefficient functions are defined in :eqref:`4.87`, :cite:`pink-book`, and
they are organized in:

- qq
- qg
- gq
- gg

according to the partons (entering the hard process - coming from the proton).

Furthermore they are organized according to their distribution structure, for
which see :py:mod:`convolution`.

The reference for LO splitting functions is :cite:`pink-book`.

.. todo:: rewrite pqq in RSL fashion

"""

from eko import constants


def pqq_reg(x):
    """
        The expression of the regular part of :math:`P_{qq}` splitting function.

        |ref| implements :eqref:`4.94`, :cite:`pink-book`.

        Parameters
        ----------
        x : float
            momentum fraction

        Returns
        -------
        float
            the regular bit of pqq splitting function @ :py:`x`

    """
    return -constants.CF * (1 + x)


def pqq_delta(_x):
    r"""
        The coefficient of the Dirac-:math:`\delta(1-x)` part of :math:`P_{qq}`
        splitting function.

        |ref| implements :eqref:`4.94`, :cite:`pink-book`.

        Parameters
        ----------
        x : float
            momentum fraction

        Returns
        -------
        float
            the delta bit of pqq splitting function @ :py:`x`

    """
    return (3 / 2) * constants.CF


def pqq_pd(_x):
    """
        The coefficient of the :math:`1/(1-x)_+` part of :math:`P_{qq}`
        splitting function.

        |ref| implements :eqref:`4.94`, :cite:`pink-book`.

        Parameters
        ----------
        x : float
            momentum fraction

        Returns
        -------
        float
            the *omx* bit of pqq splitting function @ :py:`x`

    """
    return 2 * constants.CF


def pqg(x):
    """
        The expression of :math:`P_{qg}` splitting function.

        |ref| implements :eqref:`4.94`, :cite:`pegasus`.

        Parameters
        ----------
        x : float
            momentum fraction

        Returns
        -------
        float
            the pqg splitting function @ :py:`x`

    """
    return 2.0 * constants.TR * (x ** 2 + (1.0 - x) ** 2)
