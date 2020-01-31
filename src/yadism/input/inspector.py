# -*- coding: utf-8 -*-
"""
The purpose of this module is to provide a runner that implements the semantics
for the input restrictions defined in the following files:
    * ``domains.yaml``: in which all the domains restrictions are defined
    * ``cross_constraints.yaml``: in which further restrictions are defined,
        each one involving more than one input field
"""

import abc
import os

import yaml

# ┌───────────────────┐
# │ Arguments Classes │
# └───────────────────┘


class DomainError(ValueError):
    """Error raised while checking inputs (single argument violation).

    .. todo::
        format domain properly according the type, this should be done by
        error Argument subclasses before raising.

    Parameters
    ----------
    name : str
        Name of the input variable.
    description : str
        Domain description provided.
    domain : list, optional
        The set of rules used to provide .
    """

    def __init__(self, *, name, description, known_as, domain=None, **kwargs):
        """Generates the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.

        .. todo::
            define the actual format
        """
        self.name = known_as
        self.args = (name + known_as + description,)


class Argument(abc.ABC):
    """Base Class for input variables' domains semantics definition.

    Parameters
    ----------
    **kwargs
        Domain specification, with the syntax defined in ``domains.yaml``."""

    def __init__(self, **kwargs):
        """Load ``kwargs`` as object attributes."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def check_value(self, *, value):
        """Perform the actual check .

        Parameters
        ----------
        value : type
            Description of parameter `value`.
        """
        pass

    @abc.abstractmethod
    def _raise_error(self):
        """Raise the error, preprocessing the message."""
        pass


class EnumArgument(Argument):
    """Short summary."""

    def check_value(self, *, value):
        if value not in self.domain:
            self._raise_error()

    def _raise_error(self):
        raise DomainError(**self.__dict__)


class RealArgument(Argument):
    """Short summary."""

    def check_value(self, *, value):
        exec(f"{self.metavar} = {value}")
        for rule in self.domain:
            if not eval(rule):
                self._raise_error()

    def _raise_error(self):
        raise DomainError(**self.__dict__)


type_class_map = {"enum": EnumArgument, "real": RealArgument}

# ┌───────────────────────────┐
# │ Cross Constraints Classes │
# └───────────────────────────┘


class CrossConstraintError(ValueError):
    """Error raised while checking inputs (more arguments involved)."""

    def __init__(self):
        """Generate the error message to be included in the Traceback.

        It formats the provided fields in a single string, and stores it as
        first element of ``args`` attribute.

        ..todo::
            * define the arguments involved
            * define the actual format
        """
        pass


class CrossConstraint(abc.ABC):
    pass


# ╔═══════════╗
# ║ Inspector ║
# ╚═══════════╝


class Inspector:
    """Instantiate the runner that goes through all constraints.

    Use :func:`check_domains` and :func:`check_cross_constraints` to run the
    check defined respectively in ``domains.yaml`` and
    ``cross_constraints.yaml``.
    """

    def __init__(self, user_inputs):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.input_dir = os.path.dirname(os.path.realpath(__file__))
        self.user_inputs = user_inputs

    def check_domains(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """

        domain_file = os.path.join(self.input_dir, "domains.yaml")
        with open(domain_file, "r") as file:
            domains = yaml.safe_load(file)

        for dom_def in domains:
            # load checker with domain definition
            checker = type_class_map[dom_def["type"]](**dom_def)
            # check value provided by user
            try:
                checker.check_value(value=self.user_inputs[dom_def["known_as"]])
            except KeyError:
                # @todo `try` to be replaced by an actual error: all the
                # arguments must by supplied
                pass

    def check_cross_constraints(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        pass
