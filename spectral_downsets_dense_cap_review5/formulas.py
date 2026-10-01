"""Scalar formulas independently audited in review8152; reused by reviewer5."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from exact import need, determinant3, psd_rank
from symbols import Rat, coefficients


def formulas(v, lam):
    v, lam = Rat.cast(v), Rat.cast(lam)
    m, b, r, u = v*(v-1)/2, lam*v*(v-1)/6, lam*(v-1)/2, lam*(lam-1)/2
    s, N = v+r, 1+v+m+b
    D = lam*(v*v-10*v+27)-6
    E = 3*lam*v*v-3*lam*v-16*lam+6*v
    a = -lam/3
    c = (v*v-(lam+3)*v+11*lam/3)/((v-2)*(v-3))
    d = (v*v-v-4)/((v-4)*(v-3))
    t = (v-1)*(lam*(v-3)-6)/D
    w = s-(v-3)*c-(r-2*lam)*d
    h = s-(v-4)*d-(r-3*lam)*t
    alpha1 = E/(6*(v-2))
    alpha2 = s+c
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    red = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu = s-t-(r-lam)*red
    A = (r-lam)*d*d*(v-4)**2/(v-2)
    P = (lam**4*(3*v**5-15*v**4+5*v**3+55*v*v-48*v)
         +lam**3*(-19*v**5+127*v**4-203*v**3-235*v*v+618*v)
         +lam**2*(3*v**6-12*v**5-68*v**4+438*v**3-223*v*v-2034*v+2592)
         +lam*(-6*v**5+108*v**4-642*v**3+1452*v*v-816*v-576)
         +36*v**3-180*v*v+216*v)
    return locals()
