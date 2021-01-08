# -*- coding: utf-8 -*-
import copy

import numpy as np
import pytest

from yadism.esf.esf_result import ESFResult


class MockPDFgonly:
    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x ** 2 * Q2  # it is xfxQ2! beware of the additional x
        return 0

    def hasFlavor(self, pid):
        if pid == 21:
            return True
        else:
            return False 

@pytest.mark.quick_check
class TestESFResult:
    def test_init(self):
        # test creation
        q2 = 90
        len_pids = 2
        len_xgrid = 2
        for x in [0.1, 0.2]:
            r = ESFResult(x, q2, len_pids, len_xgrid)
            assert r.x == x

    def test_from_dict(self):
        d = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[0.0, 1.0], g=[1, 0]),
            errors=dict(q=[0.0, 0.0], g=[0, 0]),
        )
        x = 0.1 
        q2 = 90
        len_pids = 2
        len_xgrid = 2
        r = ESFResult(x, q2, len_pids, len_xgrid)
        r = r.from_dict(d)
        dt =np.float
        assert len( dict(r.values.item(0))["q"] )== len(d["values"]["q"])
        for v in  dict(r.values.item(0))["q"]:
            assert isinstance( v, dt)

    @pytest.mark.skip
    def test_add_1(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[0, 1], g=[1, 0]),
            errors=dict(q=[0, 0], g=[0, 0]),
        )
        b = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[1, 0], g=[0, 1]),
            errors=dict(q=[1, 1], g=[1, 1]),
        )

        ra = ESFResult.from_dict(a)
        rb = ESFResult.from_dict(b)

        # sum
        rc = ra + rb
        assert pytest.approx(rc.values["q"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, 1])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 1])

        # subtract
        rc1 = ra - rb
        rc2 = copy.deepcopy(ra)
        rc2 -= rb
        for rc in [rc1, rc2]:
            assert pytest.approx(rc.values["q"], 0, 0) == np.array([-1, 1])
            assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 1])
            assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, -1])
            assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 1])
    
    @pytest.mark.skip
    def test_add_2(self):
        rempty = ESFResult(0.5, 10, 3, 3)
        a = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}),
            values=dict(q=[0, 1]),
            errors=dict(q=[0, 1]),
        )
        ra = ESFResult.from_dict(a)
        rea = rempty + ra
        assert rea.weights["q"] == {1: 1}
        b = dict(
            x=0.5,
            Q2=10,
            weights=dict(g={21: 1}),
            values=dict(g=[1, 0]),
            errors=dict(g=[1, 0]),
        )
        rb = ESFResult.from_dict(b)
        reab = rea + rb
        assert reab.weights["q"] == {1: 1}
        assert reab.weights["g"] == {21: 1}

        with pytest.raises(ValueError, match="Weights"):
            a = dict(
                x=0.5,
                Q2=10,
                weights=dict(q={1: 1}),
                values=dict(q=[0, 1]),
                errors=dict(q=[0, 1]),
            )
            ra = ESFResult.from_dict(a)
            b = dict(
                x=0.5,
                Q2=10,
                weights=dict(q={2: 1}),
                values=dict(q=[1, 0]),
                errors=dict(q=[1, 0]),
            )
            rb = ESFResult.from_dict(b)
            _ = ra + rb

    @pytest.mark.skip
    def test_neg(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        rc = - ra

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, -1])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([1, 0])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([1, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([1, 0])

    @pytest.mark.skip
    def test_mul(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        rc = ra * 2

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 2])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([2, 0])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([-2, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([2, 0])

        rc = [2, 1] * ra

        assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 2])
        assert pytest.approx(rc.errors["q"], 0, 0) == np.array([2, 1])
        assert pytest.approx(rc.values["g"], 0, 0) == np.array([-2, 0])
        assert pytest.approx(rc.errors["g"], 0, 0) == np.array([3, 0])

        rc1 = ra / 2.0
        rc2 = copy.deepcopy(ra)
        rc2 /= 2
        for rc in [rc1, rc2]:
            assert pytest.approx(rc.values["q"], 0, 0) == np.array([0, 0.5])
            assert pytest.approx(rc.errors["q"], 0, 0) == np.array([0.5, 0])
            assert pytest.approx(rc.values["g"], 0, 0) == np.array([-0.5, 0])
            assert pytest.approx(rc.errors["g"], 0, 0) == np.array([0.5, 0])

        with pytest.raises(ValueError):
            ra *= [1, 2, 3]

    def test_get_raw(self):
        a = dict(
            x=0.5,
            Q2=10,
            weights=dict(q={1: 1}, g={21: 1}),
            values=dict(q=[0, 1], g=[-1, 0]),
            errors=dict(q=[1, 0], g=[1, 0]),
        )

        ra = ESFResult.from_dict(a)
        dra = ra.get_raw()
        # they should be just the very same!
        for k in dra:
            if k in a:
                assert dra[k] == a[k] 

    def test_apply_pdf(self):
        # test Q2 values
        for Q2 in [1, 10, 100]:
            a = dict(
                x=0.5,
                Q2=Q2,
                weights={"g": {21: 2 / 9}, "q": {}},
                values=dict(q=[0, 1], g=[-1, 0]),
                errors=dict(q=[1, 0], g=[1, 0]),
            )
            # plain
            ra = ESFResult.from_dict(a)
            pra = ra.apply_pdf( MockPDFgonly(),[21], [0.5, 1.0], 1.0)
            expexted_res = a["values"]["g"][0] * a["x"] * a["Q2"] * 2 / 9
            expected_err = np.abs(a["values"]["g"][0]) * a["x"] * a["Q2"] * 2 / 9
            assert pytest.approx(pra["result"], 0, 0) == expexted_res
            assert pytest.approx(pra["error"], 0, 0) == expected_err
            # test factorization scale variation
            for xiF in [0.5, 2.0]:
                pra = ra.apply_pdf([0.5, 1.0], xiF, MockPDFgonly())
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF ** 2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF ** 2

        # errors
        with pytest.raises(ValueError, match=r"Q2"):
            r = ESFResult()
            r.apply_pdf([1, 2, 3], 1, MockPDFgonly())
