"""Credited exact constants of author10280, without external inputs."""
import series as s
from arithmetic import F
Mstar=s.const(s.fcf(F(8148040331,629856),F(78878749667,1259712),F(-51194418673,629856)))
betastar=s.const(s.fcf(F(27821775167,17915904),F(80418819893,8957952),F(-12650091319,1119744)))
Gstar=s.const(s.fcf(F(183619658945,2519424),F(444829186913,1259712),F(-288729410449,629856)))
L=s.const(s.fcf(F(-101920,243),F(-1218245,486),F(251888,81)))
MUstar=s.ns(L,F(-3,8))
IMPROVEMENT=s.ns(s.np(L,2),F(3,16))
Gmean=s.na(Gstar,s.ns(IMPROVEMENT,-1))
