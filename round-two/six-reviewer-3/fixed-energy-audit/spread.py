"""Late geometric refinement; ordinary circle-support proof is in REVIEW.md.

The first audit seal is preserved. This separate stage follows native replay.
"""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import symbol,need
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def build():
 eta,V=symbol('eta'),symbol('V');c=F(15,16)
 radial=1-F(3,8)*eta-F(3,40)*V
 mean=F(5,8)*eta-F(3,40)*V
 support=radial+c*mean
 need(support==1+F(27,128)*eta-F(93,640)*V,'complete original support identity')
 need(F(27,128)/(F(1,2)+F(93,640))==F(135,413),'variance floor rearrangement')
 pi_upper=F(22,7);cos_lower=1-(pi_upper/9)**2/2
 need(cos_lower>c,'rigorous ninth-root cosine lower bound')
 floor=F(135,413);extra=floor/2100
 need(extra==F(9,57820),'firstpower improvement constant')
 need(F(1,3)>extra,'larger F branch covers strengthened firstpower')
 return {'stage':'postnative geometric refinement','support_complete_coefficients':support.record(),'cosine_lower_from_pi_22_7':str(cos_lower),'cosine_margin_above15_16':str(cos_lower-c),'mean_direction_grid':'ALL nine roots: nearest argument differs by at most pi/9; includes the marked label; no phase assumption','actual_disk_radius':'each base center has norm at most1+V/2 because its counted original is disk-rooted','variance_floor':'V>135eta/413 on F<=8+3eta and H<=1/512','noncollision_consequence':'V=0 cannot occur on the actual low sublevel','positive_firstpower_increment':str(extra),'stronger_unconditional_fixed_energy_bound':'F>8+(8/3+9/57820)eta-(4/3)eta^2','larger_F_case_margin':str(F(1,3)-extra),'ordinary_trust':'Ninth-root angular covering, real projection norm bound, pi<22/7 and cos(t)>=1-t²/2; these are proved in the review, not finite parameter enumeration.'}
if __name__=='__main__':
 record=build();expected=json.loads(Path(__file__).with_name('SPREAD.json').read_text())
 if canonical(record)!=canonical(expected):raise ValueError('whole spread fixture mismatch')
 print(json.dumps({'passed':True,'canonical_sha256':hashlib.sha256(canonical(record)).hexdigest(),'variance_floor':'135/413','firstpower_extra':'9/57820'},sort_keys=True))
