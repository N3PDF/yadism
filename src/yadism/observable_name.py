# -*- coding: utf-8 -*-

kinds = ["F2", "FL"]
heavys = ["charm", "bottom", "top"]
flavors = heavys + ["light", "total"] + [h+"asy" for h in heavys]

class ObservableName:
    """
        Abstract wrapper to observables to easy split their names in two parts

        Parameters
        ----------
            name : str
                full observable name
    """
    def __init__(self, name):
        self.kind = name[:2]
        if self.kind not in kinds:
            raise ValueError(f"Unknown kind {self.kind}")
        self.flavor = name[2:]
        if self.flavor not in flavors:
            raise ValueError(f"Unknown flavor {self.flavor}")

    @property
    def name(self):
        """joint name"""
        return self.kind + self.flavor

    def __eq__(self, other):
        return self.kind == other.kind and self.flavor == other.flavor

    def apply_kind(self, kind):
        """
            Create new object with given kind and our flavor

            Parameters
            ----------
                kind : str
                    new kind

            Returns
            -------
                apply_kind : type(self)
                    new kind and our flavor
        """
        return type(self)(kind + self.flavor)

    def get_asy(self):
        """
            Computes the asymptotic heavy correspondend.

            Returns
            -------
                get_asy : type(self)
                    asymptotic heavy correspondend
        """
        if not self.is_heavy:
            raise ValueError("observable is not heavy!")
        return self.apply_flavor(self.flavor+ "asy")

    def apply_flavor(self, flavor):
        """
            Create new object with given flavor and our kind

            Parameters
            ----------
                flavor : str
                    new flavor

            Returns
            -------
                apply_flavor : type(self)
                    our kind and new flavor
        """
        return type(self)(self.kind + flavor)

    @property
    def is_heavy(self):
        """
            Is it a heavy flavor?

            Returns
            -------
                is_heavy : bool
                    is a heavy flavor?
        """
        return self.flavor in heavys

    @classmethod
    def has_heavies(cls,names):
        """
            Are there any heavy objects in names?

            Parameters
            ----------
                names : list(str)
                    names to check

            Returns
            -------
                has_heavies : bool
                    are there heavy obs in names?
        """
        for n in names:
            if not cls.is_valid(n):
                continue
            o = cls(n)
            if o.is_heavy:
                return True
        return False

    @property
    def mass_label(self):
        """mass label in the theory runcard"""
        if self.flavor == "light":
            return None
        else:
            return f"m{self.flavor[0]}"

    @staticmethod
    def is_valid(name):
        """
            Tests whether the name is a valid observable name

            Returns
            -------
                is_valid : bool
                    is valid name?
        """
        try:
            ObservableName(name)
            return True
        except ValueError:
            return False
