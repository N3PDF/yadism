# -*- coding: utf-8 -*-
# auto-generated module by ic package
# fmt: off
# pylint: skip-file

import numpy as np
from scipy.special import spence

def li2(x):
    return spence(1-x)

def f2_splus_reg(pc):
    return (8*(-2*(pc.m1sq + pc.m2sq)*pc.s1hat**2 - 2*(pc.delta**2 - 6*pc.m1sq*pc.Q2)*(pc.m2sq + pc.s1hat) - (2*pc.delta**4*(2*pc.m2sq + pc.s1hat))/pc.s1hat**2 - 9*pc.m2sq*pc.sigma_pm**2 + 2*pc.s1hat*(2*pc.delta**2 + (pc.m1sq - 5*pc.m2sq)*pc.sigma_pm) - (2*pc.delta**2*(pc.delta**2 + 2*(2*pc.m2sq + pc.s1hat)*pc.sigma_pm))/pc.s1hat - pc.delta**2*(pc.m2sq - 2*pc.sigma_pp) + ((pc.deltap**2 - 6*pc.Q2*(pc.m2sq + pc.s1hat))*pc.sigma_pp*(pc.s1hat + pc.sigma_pp))/(2.*(pc.m2sq + pc.s1hat)))*pc.x)/(pc.deltap**2*pc.Q2) - (8*pc.L_xi*(pc.m2sq + pc.s1hat)*(2*pc.delta**4*(pc.s1hat + pc.sigma_pp) + 2*pc.delta**2*pc.s1hat*(pc.s1hat + 2*pc.sigma_pm)*(pc.s1hat + pc.sigma_pp) + pc.s1hat**2*(pc.deltap**2*pc.sigma_pp - 6*pc.m1sq*pc.Q2*(2*pc.s1hat + 3*pc.sigma_pp)))*pc.x)/(pc.deltap**3*pc.Q2*pc.s1hat**2)

def f2_splus_soft(pc):
    return (-2*(2*pc.delta + pc.L_xisoft*pc.sigma_pp)*pc.x)/pc.Q2

def f2_splus_virt(pc):
    return (pc.delta*(2*pc.CRm + pc.C1p*pc.m1sq + pc.C1m*pc.m2sq)*pc.x)/(2.*pc.Q2)

def f2_sminus_reg(pc):
    return (16*pc.L_xi*np.sqrt(pc.m1sq * pc.m2sq)*(pc.deltap**2 - 6*pc.m1sq*pc.Q2)*(pc.m2sq + pc.s1hat)*pc.x)/(pc.deltap**3*pc.Q2) + (16*np.sqrt(pc.m1sq * pc.m2sq)*(2*pc.deltap**2 - 3*pc.Q2*(pc.s1hat + pc.sigma_pp) - (pc.deltap**2*(pc.s1hat + pc.sigma_pp))/(2.*(pc.m2sq + pc.s1hat)))*pc.x)/(pc.deltap**2*pc.Q2)

def f2_sminus_soft(pc):
    return 0

def f2_sminus_virt(pc):
    return (pc.delta*(pc.Cplus + ((pc.C1m + pc.C1p)*np.sqrt(pc.m1sq * pc.m2sq))/2.)*pc.x)/pc.Q2

def fL_splus_reg(pc):
    return (-4*(8*pc.delta**4*(pc.m2sq + pc.s1hat)**2 + 2*pc.delta**2*(pc.s1hat*(pc.s1hat*(3*pc.m2sq**2 + pc.m2sq*pc.s1hat - pc.s1hat*(9*pc.Q2 + 2*pc.s1hat)) + 4*(pc.m2sq + pc.s1hat)*(2*pc.m2sq + pc.s1hat)*pc.sigma_pm) - 2*(2*pc.m2sq**2*pc.Q2 + pc.s1hat**2*(pc.Q2 + pc.s1hat) + pc.m2sq*pc.s1hat*(4*pc.Q2 + pc.s1hat))*pc.sigma_pp) + pc.s1hat*(pc.s1hat*(28*pc.m1sq**2*pc.Q2*pc.s1hat + pc.s1hat**2*(4*pc.m2sq**2 + 4*pc.m2sq*pc.s1hat + pc.Q2*pc.s1hat) + 2*pc.m1sq*(-12*pc.m2sq**2*pc.Q2 + pc.s1hat*(14*pc.Q2**2 - 9*pc.Q2*pc.s1hat + 2*pc.s1hat*(pc.s1hat - pc.sigma_pm)) + 2*pc.m2sq*pc.s1hat*(-16*pc.Q2 + pc.s1hat - pc.sigma_pm)) + (pc.s1hat*(20*pc.m2sq**2 + 20*pc.m2sq*pc.s1hat - 3*pc.Q2*pc.s1hat) + 4*pc.m2sq*pc.Q2*pc.sigma_mp)*pc.sigma_pm + 18*pc.m2sq*(pc.m2sq + pc.s1hat)*pc.sigma_pm**2) + (4*pc.m1sq*pc.m2sq*pc.Q2*pc.s1hat + pc.s1hat**2*(-pc.deltap**2 + 6*pc.Q2*(pc.m2sq + pc.s1hat) + 7*pc.Q2*pc.sigma_mp) - 8*pc.m2sq*pc.Q2*(2*pc.m2sq + 5*pc.s1hat)*pc.sigma_pm)*pc.sigma_pp + pc.s1hat*(-pc.deltap**2 + 6*pc.Q2*(pc.m2sq + pc.s1hat) - 3*pc.Q2*pc.sigma_mp)*pc.sigma_pp**2))*pc.x)/(pc.deltap**2*pc.Q2*pc.s1hat**2*(pc.m2sq + pc.s1hat)) - (8*pc.L_xi*(pc.m2sq + pc.s1hat)*(2*pc.delta**4*(pc.s1hat + pc.sigma_pp) + 2*pc.delta**2*(pc.s1hat + pc.sigma_pp)*(pc.s1hat**2 + 2*pc.s1hat*pc.sigma_pm - pc.Q2*pc.sigma_pp) + pc.s1hat*(pc.deltap**2*pc.s1hat*pc.sigma_pp - 2*pc.m1sq*pc.Q2*pc.s1hat*(-2*pc.m2sq + 6*pc.s1hat + 9*pc.sigma_pp) - pc.Q2*(pc.s1hat**3 + 4*pc.s1hat**2*pc.sigma_pm + 7*pc.s1hat*pc.sigma_pm*pc.sigma_pp + 4*pc.sigma_pm*pc.sigma_pp**2)))*pc.x)/(pc.deltap**3*pc.Q2*pc.s1hat**2)

def fL_splus_soft(pc):
    return (-2*(2*pc.delta + pc.L_xisoft*pc.sigma_pp)*(pc.delta**2 - pc.Q2*pc.sigma_pp)*pc.x)/(pc.delta**2*pc.Q2)

def fL_splus_virt(pc):
    return (((pc.delta**2*(pc.C1p*pc.m1sq + pc.C1m*pc.m2sq))/pc.Q2 + (2*pc.CRm*(pc.delta**2 - pc.Q2*pc.sigma_pp))/pc.Q2 + (2*pc.Cplus*Sminus*(4*m1**2*m2**2 + pc.sigma_pp**2))/(2*np.sqrt(pc.m1sq * pc.m2sq)*Sminus - Splus*pc.sigma_pp))*pc.x)/(2.*pc.delta)

def fL_sminus_reg(pc):
    return (-16*pc.L_xi*np.sqrt(pc.m1sq * pc.m2sq)*(pc.m2sq + pc.s1hat)*(pc.deltap**2*(2*pc.Q2 - pc.s1hat)*pc.s1hat + 2*pc.Q2*((3*pc.m1sq + pc.m2sq + pc.Q2)*pc.s1hat**2 + (pc.delta**2 + 2*pc.s1hat*pc.sigma_pm)*pc.sigma_pp))*pc.x)/(pc.deltap**3*pc.Q2*pc.s1hat**2) - (8*np.sqrt(pc.m1sq * pc.m2sq)*(4*pc.delta**2*pc.Q2*(pc.m2sq + pc.s1hat)*(2*pc.m2sq + pc.s1hat) + pc.s1hat*(pc.deltap**2*(4*pc.m2sq*(pc.Q2 - pc.s1hat) + pc.s1hat*(4*pc.Q2 - 3*pc.s1hat + pc.sigma_pp)) + 4*pc.Q2*(pc.m2sq + pc.s1hat)*(4*pc.m2sq*pc.sigma_pm + pc.s1hat*(2*pc.s1hat - pc.sigma_mp + 2*(pc.sigma_pm + pc.sigma_pp)))))*pc.x)/(pc.deltap**2*pc.Q2*pc.s1hat**2*(pc.m2sq + pc.s1hat))

def fL_sminus_soft(pc):
    return (-4*np.sqrt(pc.m1sq * pc.m2sq)*(2*pc.delta + pc.L_xisoft*pc.sigma_pp)*pc.x)/pc.delta**2

def fL_sminus_virt(pc):
    return ((2*pc.CRm*np.sqrt(pc.m1sq * pc.m2sq) + (pc.delta**2*(pc.Cplus + ((pc.C1m + pc.C1p)*np.sqrt(pc.m1sq * pc.m2sq))/2.))/pc.Q2 + (4*pc.Cplus*m1**2*m2**2*Splus)/(2*np.sqrt(pc.m1sq * pc.m2sq)*Sminus - Splus*pc.sigma_pp) + (pc.Cplus*Splus*pc.sigma_pp**2)/(2*np.sqrt(pc.m1sq * pc.m2sq)*Sminus - Splus*pc.sigma_pp))*pc.x)/pc.delta

def f3_rplus_reg(pc):
    return (16*((-2*pc.delta**2*(2*pc.m2sq + pc.s1hat))/pc.s1hat**2 + pc.sigma_mp - 3*pc.sigma_pm - (2*(pc.delta**2 + 2*pc.m2sq*pc.sigma_pm))/pc.s1hat - ((pc.s1hat - pc.sigma_mp)*(pc.s1hat + pc.sigma_pp))/(2.*(pc.m2sq + pc.s1hat))))/pc.deltap - (16*pc.L_xi*(pc.m2sq + pc.s1hat)*(pc.s1hat*(pc.s1hat**2 - 4*pc.m1sq*pc.sigma_mp + 3*pc.s1hat*pc.sigma_pm) + 2*pc.delta**2*(2*pc.s1hat + pc.sigma_pp)))/(pc.deltap**2*pc.s1hat**2)

def f3_rplus_soft(pc):
    return -8 - (4*pc.L_xisoft*pc.sigma_pp)/pc.delta

def f3_rplus_virt(pc):
    return 2*pc.CRm

def f3_rminus_reg(pc):
    return (32*np.sqrt(pc.m1sq * pc.m2sq)*(pc.s1hat - pc.sigma_mp))/(pc.deltap*pc.s1hat) + (32*pc.L_xi*np.sqrt(pc.m1sq * pc.m2sq)*(pc.m2sq + pc.s1hat)*(pc.s1hat + pc.sigma_pm))/(pc.deltap**2*pc.s1hat)

def f3_rminus_soft(pc):
    return 0

def f3_rminus_virt(pc):
    return 2*pc.Cplus

def I1(pc):
    return np.log( ( pc.sigma_pp + pc.delta ) / ( pc.sigma_pp - pc.delta ) ) / pc.delta

def CRm(pc):
    return ( pc.delta**2 / 2 / pc.Q2 + pc.sigma_pp * ( 1 + np.log( pc.Q2 / pc.delta ) ) ) * pc.I1 + ( pc.m2sq - pc.m1sq ) / 2 / pc.Q2 * np.log( pc.m1sq / pc.m2sq ) - np.log( pc.Q2 / pc.m1sq ) - np.log( pc.Q2 / pc.m2sq ) - 4 + pc.sigma_pp / pc.delta * ( + np.log( np.abs( ( pc.delta - pc.sigma_pm ) / 2 / pc.Q2 ) )**2 / 2 + np.log( np.abs( ( pc.delta - pc.sigma_mp ) / 2 / pc.Q2 ) )**2 / 2 - np.log( np.abs( ( pc.delta + pc.sigma_pm ) / 2 / pc.Q2 ) )**2 / 2 - np.log( np.abs( ( pc.delta + pc.sigma_mp ) / 2 / pc.Q2 ) )**2 / 2 - li2( ( pc.delta - pc.sigma_pm ) / 2 / pc.delta ) - li2( ( pc.delta - pc.sigma_mp ) / 2 / pc.delta ) + li2( ( pc.delta + pc.sigma_pm ) / 2 / pc.delta ) + li2( ( pc.delta + pc.sigma_mp ) / 2 / pc.delta ) )

def Cplus(pc):
    return 2 * np.sqrt(pc.m1sq * pc.m2sq) * pc.I1

def C1m(pc):
    return - ( pc.sigma_pm * pc.I1 + np.log( pc.m1sq / pc.m2sq ) ) / pc.Q2

def C1p(pc):
    return - ( pc.sigma_mp * pc.I1 - np.log( pc.m1sq / pc.m2sq ) ) / pc.Q2

def S(pc):
    return 2 + pc.sigma_pp / pc.delta * ( pc.delta * pc.I1 + li2( 2 * pc.delta / ( pc.delta - pc.sigma_pp ) ) - li2( 2 * pc.delta / ( pc.delta + pc.sigma_pp ) ) ) + np.log( pc.delta**2 / pc.m2sq / pc.Q2 ) * ( - 2 + pc.sigma_pp * pc.I1 )
