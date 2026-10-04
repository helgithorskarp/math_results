"""Bounded exact reconstruction. Output is generated evidence, never an input."""
from pathlib import Path
import json,sys,signal,time,resource,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as Q
from ring import spectral_maps,listpoly,degree
from certificates import positive_q0,real_q0,affine,bernstein,quartic
from bridges import identities

def record():
    H,r,f,Qfull,B,R,Delta,N,P=spectral_maps()
    base={'H64':[listpoly(p)for p in H],'r64':[listpoly(p)for p in r],
      'f64':[listpoly(p)for p in f],'Q64':[listpoly(p)for p in Qfull],
      'B0':[[listpoly(p)for p in row]for row in B],'B1':[[listpoly(p)for p in row]for row in R],
      'Delta_scaled':listpoly(Delta),'N_scaled':listpoly(N),'P_scaled':listpoly(P),'map_scale':str(64**12),'boxes':[]}
    cases=[('positive-q0-plus',lambda:positive_q0(P,1),[(Q(1,72),Q(17,250)),(Q(0),Q(1)),(Q(0),Q(1))],(31,8,5)),
       ('positive-q0-minus',lambda:positive_q0(P,-1),[(Q(1,72),Q(71,1000)),(Q(0),Q(1)),(Q(0),Q(1))],(31,8,5)),
       ('real-q0-minus',lambda:real_q0(P,1024),[(Q(1,123),Q(1,26)),(Q(-7,4),Q(-1)),(Q(0),Q(1))],(12,28,5)),
       ('real-q0-plus-left',lambda:real_q0(P,576),[(Q(1,123),Q(149,6396)),(Q(1),Q(7,4)),(Q(0),Q(1))],(12,28,5)),
       ('real-q0-plus-right',lambda:real_q0(P,576),[(Q(149,6396),Q(1,26)),(Q(1),Q(7,4)),(Q(0),Q(1))],(12,28,5))]
    for name,build,bounds,deg in cases:
        S,scale=build();p=affine(S,bounds);controls=bernstein(p,deg)
        base['boxes'].append({'name':name,'bounds':[[str(x)for x in pair]for pair in bounds],
          'reduced_scale':str(scale),'reduced':listpoly(S),'affine':listpoly(p),'controls':listpoly(controls),
          'degree':list(degree(S)),'count':len(controls),'unscaled_min':str(min(controls.values())/scale),
          'complete_inverse_equal':True})
        print(name,len(S),len(controls),'positive',flush=True)
    quartic_poly,records=quartic();base['quartic_poly']=listpoly(quartic_poly)
    base['quartic_boxes']=[{'affine':listpoly(p),'controls':listpoly(c),'minimum':str(min(c.values()))}for p,c in records]
    from written_minima import MINIMA,QUARTIC_MINIMA
    if [Q(x['unscaled_min'])for x in base['boxes']]!=MINIMA or [Q(x['minimum'])for x in base['quartic_boxes']]!=QUARTIC_MINIMA:
        raise ValueError('complete independently reconstructed written minima')
    if sum(x['count']for x in base['boxes'])+sum(len(c)for p,c in records)!=10492:
        raise ValueError('entire new certificate count')
    base['original_bridges']=identities()
    b=Q(base['boxes'][1]['unscaled_min'])
    if min(Q(x['unscaled_min'])for x in base['boxes'][:2])!=b or b/(72**10*2**31)<=Q(1,2**146):
        raise ValueError('new positive-q0 middle-band deficit')
    if min(Q(x['unscaled_min'])for x in base['boxes'][2:])<=2**26:
        raise ValueError('new outer real-q0 deficit')
    base['quantitative_refinements']={'positive_q0_middle_band_gap':'2^-146','real_q0_outer_middle_band_gap':'2^-125*(24*(A-1/8)^2/D-1)^2','gap_hypotheses':'actual one-double with reflected a>0,4+4 signs,1/625<D<=5/141; chart regions and original-root licences as in proof'}
    return base

if __name__=='__main__':
    signal.alarm(45);start=time.monotonic();rec=record()
    raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode();Path(sys.argv[1]).write_bytes(raw)
    print(json.dumps({'whole_bytes':len(raw),'whole_sha256':hashlib.sha256(raw).hexdigest(),
      'minima':[r['unscaled_min']for r in rec['boxes']],'quartic_minima':[r['minimum']for r in rec['quartic_boxes']],
      'all10492_coefficients_positive_and_whole_inverse_equal':True,'seconds':round(time.monotonic()-start,6),
      'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
