# -*- coding: utf-8 -*-
"""
Define DistributionVec and its API.

.. todo::
    docs
"""
import copy

import numpy as np
import scipy.integrate


class DistributionVec:
    """
    Representing a distribution giving coefficients on a distribution basis:
        - 1
        - delta(1-x)
        - 1/(1-x)_+
        - (log(1-x)/(1-x))_+
    """

    __names = ["regular", "delta", "omx", "logomx"]

    def __init__(self, regular, delta=None, omx=None, logomx=None):
        try:
            comp_list = [x for x in regular]
            for i in range(len(self.__names) - len(regular)):
                comp_list.append(None)
        except TypeError:
            comp_list = [regular, delta, omx, logomx]

        components = zip(self.__names, comp_list)

        for name, component in components:
            if callable(component):
                component_func = component
            elif component is None:
                component_func = lambda x: 0
            else:
                # if component is None:
                # __import__("pdb").set_trace()
                component_func = lambda x, component=component: float(component)

            setattr(self, f"_{name}", component_func)

    def __getitem__(self, key):
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return getattr(self, f"_{name}")
        else:
            raise IndexError("todo")

    def __setitem__(self, key, value):
        if 0 <= key < len(self.__names):
            name = self.__names[key]
            return setattr(self, f"_{name}", value)
        else:
            raise IndexError("todo")

    def __iter__(self):
        for n in self.__names:
            yield getattr(self, f"_{n}")

    def __add__(self, other):
        """
        Do not support ``DistributionVec + iterable``, if needed use:
        .. code-block::
            d_vec + DistributionVec(*iterable)

        Supported:
        * ``+ num``
        * ``+ function``
        * ``+ DistributionVec``

        .. todo::
            docs
        """
        if isinstance(other, DistributionVec):
            result = DistributionVec(0)
            for i, (c1, c2) in enumerate(zip(self, other)):
                result[i] = lambda x, c1=c1, c2=c2: c1(x) + c2(x)
        elif callable(other):
            result = copy.deepcopy(self)
            old = result[0]
            result[0] = lambda x, old=old, other=other: old(x) + other(x)
        else:
            result = copy.deepcopy(self)
            old = result[0]
            result[0] = lambda x, old=old, other=other: old(x) + float(other)

        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        self = self.__add__(other)

    def convnd(self, x, pdf_func):
        """TODO: Docstring for convnd.

        Parameters
        ----------
        self : TODO
        x : TODO
        pdf : TODO

        Returns
        -------
        TODO

        """

        # providing integrands functions and addends
        # ------------------------------------------

        # plus distribution test function
        __pd_tf = lambda z, n: self[n](z) * pdf_func(x / z) / z

        integrands = [
            lambda z: self[0](z) * pdf_func(x / z) / z,
            0.0,
            lambda z: (__pd_tf(z, 2) - __pd_tf(1, 2)) / (1 - z),
            lambda z: (__pd_tf(z, 3) - __pd_tf(1, 3)) * np.log(1 - z) / (1 - z),
        ]

        addends = [
            0.0,
            self[1](1) * pdf_func(x),
            self[2](1) * pdf_func(x) * np.log(1 - x),
            self[3](1) * pdf_func(x) * np.log(1 - x) ** 2 / 2,
        ]

        # actual convolution
        # ------------------

        res = 0.0
        err = 0.0

        for i, a in zip(integrands, addends):
            if callable(i):
                r, e = scipy.integrate.quad(
                    i, x, 1.0, points=[x, 1.0]
                )  # TODO: take care of both limits
                res += r
                err += e ** 2
            res += a

        return res, np.sqrt(err)
