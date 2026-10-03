"""Whole geometric negative controls; six-tammes-1, researcher."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
import json
import check as C
import audit as A

ROOT=Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def rejects(call,why):
    try:call()
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):return
    raise ValueError('negative control unexpectedly accepted: '+why)
def monotone_negative(p):
    A.require(A.upper_terms(A.derivative(p))<=0 and A.at(p,A.LO)<0,'closed monotone negative control')
def main():
    r=json.loads((ROOT/'CERTIFICATE.json').read_text())
    C.verify(r);A.verify(r) # Fresh full geometry, not cached outputs.
    endpoint=[C.LO,F(-1)]
    rejects(lambda:C.negative(endpoint),'closed left endpoint root')
    rejects(lambda:monotone_negative(A.P(C.LO,-1)),'closed left endpoint root, separate method')
    rejects(lambda:C.negative([]),'zero polynomial')
    rejects(lambda:monotone_negative({}),'zero polynomial, separate method')
    C.negative([F(-1)]);monotone_negative(A.P(-1))
    C.negative(C.K);monotone_negative(A.K)
    need(A.upper_terms(A.derivative(A.K))==F(-77587,6400),'strict derivative margin')
    need(A.at(A.K,A.LO)==F(-64373,100000),'strict endpoint margin')
    # A common-neighbor example exactly at the feasibility boundary must
    # not be rejected by confusing S=0 with S<0. For physical c=3/5,
    # w=(1,0,0), u=(3/5,4/5,0), v=(3/5,-4/5,0).
    w=(F(1),F(0),F(0));u=(F(3,5),F(4,5),F(0));v=(F(3,5),F(-4,5),F(0))
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    need(all(dot(x,x)==1 for x in (w,u,v)),'three actual unit vectors')
    need(dot(w,u)==dot(w,v)==F(3,5),'two actual contacts')
    need(1+dot(u,v)-2*F(3,5)**2==0,'valid exact tangency boundary retained')
    # Nine changes exercise the theorem-bearing contents rather than the
    # count alone. Every damaged record goes through both full rebuilds.
    changes=[
      ('B-coordinate',lambda x:x['cases'][0]['B_points']['22'][0].__setitem__(0,'17')),
      ('B-triangle',lambda x:x['cases'][0]['B_triangles'][3].__setitem__(2,21)),
      ('pair',lambda x:x['cases'][0]['pair'].__setitem__(1,21)),
      ('pair-Gram',lambda x:x['cases'][0]['pair_N'].__setitem__(2,'-7')),
      ('Cauchy-gap',lambda x:x['cases'][0]['S'].__setitem__(0,'0')),
      ('K-coefficient',lambda x:x['K'].__setitem__(0,'5')),
      ('Bernstein-endpoint',lambda x:x['K_Bernstein'].__setitem__(0,'0')),
      ('false-closed-band',lambda x:x['r_closed_band'].__setitem__(0,'3/5')),
      ('mask-row',lambda x:x['rows'][0]['cross'].__setitem__(0,[7,10])),
      ('missing-case',lambda x:x['cases'].pop()),
      ('duplicate-map',lambda x:x['excluded_maps'].__setitem__(1,42)),
      ('dropped-remaining-map',lambda x:x['remaining_strict_maps'].pop()),
      ('wrong-case-routing',lambda x:x['rows'][0].__setitem__('case',1)),
      ('wrong-frozen-cover-binding',lambda x:x.__setitem__('previous_sha256','0'*64)),
      ('false-upper-bound',lambda x:x.__setitem__('K_closed_upper','0')),
    ]
    for name,change in changes:
        damaged=deepcopy(r);change(damaged)
        rejects(lambda:C.verify(damaged),name+', full forward rebuild')
        rejects(lambda:A.verify(damaged),name+', full reverse/monotone rebuild')
    for text in (json.dumps(r,indent=3),json.dumps(r,sort_keys=True)):
        C.verify(json.loads(text));A.verify(json.loads(text))
    result={'status':'complete','actual_author':'six-tammes-1','role':'researcher',
            'arithmetic_and_boundary_controls':9,'full_geometric_negative_records':len(changes),
            'each_negative_rebuilt_by_both':True,'valid_JSON_presentations':2,
            'valid_zero_discriminant_example_retained':True,
            'certificate_sha256':sha256(C.canonical(r).encode()).hexdigest()}
    expected=json.loads((ROOT/'CONTROLS.json').read_text())
    need(result==expected,'whole expected controls output')
    print(C.canonical(result).strip())
if __name__=='__main__':main()
