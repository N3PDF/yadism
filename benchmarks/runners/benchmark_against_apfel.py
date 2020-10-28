# -*- coding: utf-8 -*-
#
# Compare the results with APFEL's

import pytest

import numpy as np

from yadmark.benchmark.db_interface import DBInterface


class ApfelBenchmark:
    """Wrapper to apply some default settings"""

    db = None

    def _db(self, assert_external=None):
        """init DB connection"""
        # assert_external = False
        self.db = DBInterface("APFEL", assert_external=assert_external)
        return self.db

    def run_external(
        self, PTO, pdfs, theory_update=None, obs_update=None, assert_external=None
    ):
        """Query for PTO also in obs by default"""
        self._db(assert_external)
        # set some defaults
        obs_matrix = {
            "PTO": self.db.obs_query.PTO == PTO,
            "prDIS": self.db.obs_query.prDIS == "EM",
            "projectile": self.db.obs_query.projectile == "electron",
            "PolarizationDIS": self.db.obs_query.PolarizationDIS == 0,
        }
        # allow changes
        if obs_update is not None:
            obs_matrix.update(obs_update)
        # collect Query
        obs_query = self.db.obs_query.noop()
        for q in obs_matrix.values():
            if q is None:
                continue
            obs_query &= q
        return self.db.run_external(PTO, pdfs, theory_update, obs_query)


def plain_assert_external(theory, obs, sf, yad):
    if sf == "FLbottom" and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2:
        # APFEL has a discreization in Q2/m2
        return dict(abs=5e-6)
    if obs["prDIS"] == "CC":
        if sf[2:] == "charm" and yad["x"] > 0.75:
            return dict(abs=2e-6)  # grid border
        if sf[2:] == "top" and yad["Q2"] < 150:
            return dict(abs=1e-4)  # production threshold
        if sf == "F3total" and (yad["Q2"] < 7 or 500 < yad["Q2"] < 1000):
            # we have a change in sign (from + to - at small Q2 and back to + at large)
            # F3light is > 0, but F3charm < 0
            return dict(abs=2e-4)
    return None


@pytest.mark.quick_check
@pytest.mark.commit_check
class BenchmarkPlain(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(0, ["ToyLH"], obs_update={"prDIS": None})

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["ToyLH"],
            obs_update={"prDIS": None},
            assert_external=plain_assert_external,
        )


@pytest.mark.commit_check
class BenchmarkProjectile(ApfelBenchmark):
    """The most basic checks"""

    def benchmark_LO(self):
        return self.run_external(
            0,
            ["ToyLH"],
            obs_update={
                "prDIS": self._db().obs_query.prDIS.one_of(["NC", "CC"]),
                "projectile": None,
                "PolarizationDIS": None,
            },
        )

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["ToyLH"],
            obs_update={
                "prDIS": self._db().obs_query.prDIS.one_of(["NC", "CC"]),
                "projectile": None,
                "PolarizationDIS": None,
            },
            assert_external=plain_assert_external,
        )

def sv_assert_external(theory, obs, sf, yad):
    if np.isclose(theory["XIF"], 1) and np.isclose(theory["XIR"], 1):
        return plain_assert_external(theory, obs, sf, yad)
    if (
        sf == "FLbottom"
        and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2
    ):
        # APFEL has a discreization in Q2/m2
        return dict(abs=1e-5)
    if sf == "FLcharm" and yad["Q2"] < 7:
        return dict(rel=0.015)
    if obs["prDIS"] == "CC":
        if sf[2:] == "top":
            if yad["Q2"] < 160:
                return dict(abs=2e-4)  # production threshold
            if sf[:2] == "F3" and yad["Q2"] > 900:
                return dict(abs=3e-5)  # why does the thing go worse again?
        if (
            sf == "F3charm"
            and 0.5e-3 < yad["x"] < 2e-3
        ):
            # there is a cancelation between sbar and g going on:
            # each of the channels is O(1) with O(1e-3) accuracy
            return dict(abs=5e-3)
        if sf == "F3total":
            # still F3light is > 0, but F3charm < 0
            return dict(rel=0.05)
    if theory["XIF"] < 1 and theory["XIR"] < 1:
        # for small xir pQCD becomes unreliable
        if sf in ["F2light", "F2total"] and yad["Q2"] < 7:
            return dict(abs=5e-2)
    return None

@pytest.mark.commit_check
class BenchmarkScaleVariations(ApfelBenchmark):
    """Vary factorization and renormalization scale"""

    def benchmark_LO(self):
        return self.run_external(
            0, ["CT14llo_NF3"], {"XIR": None, "XIF": None}, {"prDIS": None}
        )

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["CT14llo_NF3"],
            {"XIR": None, "XIF": None,},
            {"prDIS": None},
            assert_external=sv_assert_external,
        )


def tmc_assert_external(theory, _obs, sf, yad):
    # turning point (maybe again a cancelation of channels?)
    if sf in ["F2light", "F2total"] and yad["x"] > 0.9:
        return dict(abs=1e-4)
    # same as in plain
    if sf == "FLbottom" and theory["mb"] ** 2 / 4 < yad["Q2"] < theory["mb"] ** 2:
        # APFEL has a discreization in Q2/m2
        return dict(abs=1e-5)
    # FL TMC is broken in APFEL
    # https://github.com/scarrazza/apfel/issues/23
    if sf[:2] == "FL" and yad["x"] > 0.3:
        return dict(abs=1e-2)
    return None


@pytest.mark.commit_check
class BenchmarkTMC(ApfelBenchmark):
    """Add Target Mass Corrections"""

    def benchmark_LO(self):
        return self.run_external(
            0,
            ["ToyLH"],
            {"TMC": self._db().theory_query.TMC == 1},
            assert_external=tmc_assert_external,
        )

    def benchmark_NLO(self):
        return self.run_external(
            1,
            ["ToyLH"],
            {"TMC": self._db().theory_query.TMC == 1},
            assert_external=tmc_assert_external,
        )


class BenchmarkFNS(ApfelBenchmark):
    """Flavor Number Schemes"""

    def benchmark_LO(self):
        return self.run_external(
            0,
            ["CT14llo_NF6"],
            {"FNS": ~(self._db().theory_query.FNS.search("FONLL-")), "NfFF": None},
        )

    def benchmark_NLO_FFNS(self):
        def ffns_assert(theory, obs, sf, yad):
            if theory["NfFF"] < 5:
                return plain_assert_external(theory, obs, sf, yad)
            # TODO https://github.com/N3PDF/yadism/wiki/2020_05_28-F2charm-FFNS4-low-Q2-non-zero
            if theory["NfFF"] == 5 and sf[2:] in ["bottom", "total"] and yad["Q2"] < theory["mb"] ** 2:
                return False
            return None

        return self.run_external(
            1,
            ["CT14llo_NF6"],
            {
                "FNS": self._db().theory_query.FNS == "FFNS",
                "NfFF": self._db().theory_query.NfFF != 3,
            },
            assert_external=ffns_assert,
        )

    def benchmark_NLO_ZM_VFNS(self):
        return self.run_external(
            1, ["CT14llo_NF6"], {"FNS": self._db().theory_query.FNS == "ZM-VFNS"}
        )

    def benchmark_NLO_FONLL(self):
        return self.run_external(
            1,
            ["CT14llo_NF6"],
            {"FNS": self._db().theory_query.FNS == "FONLL-A", "DAMP": None},
        )


if __name__ == "__main__":
    # plain = BenchmarkPlain()
    # plain.benchmark_LO()
    # plain.benchmark_NLO()

    # proj = BenchmarkProjectile()
    # proj.benchmark_LO()
    # proj.benchmark_NLO()

    sv = BenchmarkScaleVariations()
    sv.benchmark_NLO()

    # fns = BenchmarkFNS()
    # fns.benchmark_NLO_FONLL()
