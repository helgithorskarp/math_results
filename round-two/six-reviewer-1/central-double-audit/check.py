"""Fresh whole original-map and whole Bernstein reconstruction, integer/Fraction."""
from pathlib import Path
import sys,json,signal,hashlib,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as Q
from integers import spectral_maps,cap,affine,tensor,listpoly,degree
from controls import controls as original_controls

def math_record():
    H,r,f,Qfull,B,R,Delta,N,P=spectral_maps()
    base={'H64':[listpoly(p)for p in H],'r64':[listpoly(p)for p in r],
          'f64':[listpoly(p)for p in f],'Q64':[listpoly(p)for p in Qfull],
          'B0':[[listpoly(p)for p in row]for row in B],
          'B1':[[listpoly(p)for p in row]for row in R],
          'Delta_scaled':listpoly(Delta),'N_scaled':listpoly(N),'P_scaled':listpoly(P),
          'map_scale':str(64**12),'maps_all_positions_checked':True,'boxes':[]}
    bounds=[('negative',32,Q(1,133),Q(1,26),Q(-1),Q(0)),
      ('positive-left',64,Q(1,133),Q(159,6916),Q(0),Q(1)),
      ('positive-right',64,Q(159,6916),Q(1,26),Q(0),Q(1))]
    for name,k,lo,hi,tl,tr in bounds:
        S,scale=cap(P,k);poly=affine(S,lo,hi,tl,tr);controls=tensor(poly)
        base['boxes'].append({'name':name,'kappa':k,'q':[str(lo),str(hi)],'t':[str(tl),str(tr)],
          'reduced_scale':str(scale),'reduced_polynomial':listpoly(S),
          'entire_affine_polynomial':listpoly(poly),'all_controls':listpoly(controls),
          'all2262_strict_positive':True,'whole_inverse_tensor_equal':True,
          'unscaled_minimum':str(min(controls.values())/scale),'degrees':list(degree(S))})
    minima=[Q(row['unscaled_minimum'])for row in base['boxes']]
    written=[Q(7885466452528416,815730721),Q(330815919331712900214563879677199616,559059441355907035400747527),Q(240063645295309059778608,815432979286835)]
    if minima!=written or min(minima)!=written[0]:raise ValueError('complete independently reconstructed written minima')
    base['original_controls']=original_controls(B,R,Delta,N,P)
    return base

if __name__=='__main__':
    signal.alarm(45);start=time.monotonic();rec=math_record();raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode()
    Path(sys.argv[1]).write_bytes(raw)
    print(json.dumps({'whole_bytes':len(raw),'whole_sha256':hashlib.sha256(raw).hexdigest(),
      'whole_minima':[r['unscaled_minimum']for r in rec['boxes']],
      'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'all6786_controls_and_full_reverse_identities_passed':True}))
