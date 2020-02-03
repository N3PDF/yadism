# -*- coding: utf-8 -*-
#
# Testing the loading functions
import os
from pprint import pprint

import yaml
import numpy as np
import lhapdf

import yadism.tests.toyLH as toyLH
import yadism.basis_rotation as rot
from yadism.runner import run_dis
from yadism.tests.apfel_import import load_apfel


def test_loader():
    """Test the loading mechanism"""

    test_dir = os.path.dirname(__file__)

    # read files
    theory_file = os.path.join(test_dir, "theory.yaml")
    with open(theory_file, "r") as file:
        theory = yaml.safe_load(file)
    observables_file = os.path.join(test_dir, "dis_observables.yaml")
    with open(observables_file, "r") as file:
        dis_observables = yaml.safe_load(file)

    # execute DIS
    result = run_dis(theory, dis_observables)

    # setup LHAPDF
    pdfset = theory.get("PDFSet", "ToyLH")
    if pdfset == "ToyLH":
        pdfs = toyLH.mkPDF("ToyLH", 0)
    else:
        pdfs = lhapdf.mkPDF(pdfset, 0)

    def get_useful(x, Q2, Nf):
        """Short summary.

        d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9
        =
        (S + 3*T3/4 + T8/4) * sq_charge_av
        """
        ph2pid = lambda k: k - 7
        ph = [0] + [pdfs.xfxQ2(ph2pid(k), x, Q2) for k in range(1, 14)]
        useful = (rot.QCDsinglet(ph) + rot.QCDT3(ph) * 3 / 4 + rot.QCDT8(ph) / 4) / x

        return useful

    # setup APFEL
    apfel = load_apfel(theory)

    # loop kinematics
    res_tab = []

    for kinematics in result.get("F2", []):
        Q2 = kinematics["Q2"]
        x = kinematics["x"]

        # compute F2
        singlet_vec = np.array(
            [get_useful(x, Q2, theory["NfFF"]) for x in result["xgrid"]]
        )
        f2_lo = np.dot(singlet_vec, kinematics["S"])

        # execute APFEL (if needed)
        if False:
            pass
        else:
            apfel.ComputeStructureFunctionsAPFEL(np.sqrt(Q2), np.sqrt(Q2))
            ref = apfel.F2light(x)

        res_tab.append([x, Q2, ref, f2_lo, ref / f2_lo])

    # print results

    print("\n------\n")
    for x in res_tab:
        for y in x:
            print(y, "" if len(str(y)) > 7 else "\t", sep="", end="\t")
        print()
    print("\n------\n")


if __name__ == "__main__":
    test_loader()