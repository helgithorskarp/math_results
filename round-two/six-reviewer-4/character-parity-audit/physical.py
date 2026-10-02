#!/usr/bin/env python3
"""Original CRT APs, all phase rows, all affine parameters and positive lifts."""
from pathlib import Path
from itertools import product
from collections import Counter
import argparse,json,hashlib,math
SIG=(0,0,0,1,1,1)

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def crt(field,phase):return next(n for n in range(field,618,103)if n%6==phase)
def positive(n):return n if n else 618
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
 squares={x*x%103 for x in range(1,103)};need(len(squares)==51 and 0 not in squares,'actual field squares')
 def L(x):need(0<x<103,'undefined character at zero');return int(x not in squares)
 checks=0
 for x in range(1,103):
  for y in range(1,103):need(L(x*y%103)==(L(x)^L(y)),'every physical multiplicativity input');checks+=1
 supports=[];transcript=[]
 for k in range(1,103):
  h=crt(k,1);need(math.gcd(h,618)==1,'actual orbit unit');ap=[h*n%618 for n in range(80,87)];colors=[L(n%103)^SIG[n%6]for n in ap];need(len(set(colors))==1,'actual canonical bad AP')
  field=sorted({n%103 for n in ap});need(len(field)==7 and 0 not in field,'actual regular support');supports.append(field);transcript.append([k,h,ap,colors,field])
 need(len({tuple(s)for s in supports})==102,'all actual orbit supports distinct');need(Counter(r for s in supports for r in s)==Counter({r:7 for r in range(1,103)}),'every actual field degree')
 phase_rows=list(product(range(2),repeat=6));legal=[];illegal=[];phase_tests=singleton_checks=0;singleton_max=0;singleton_steps=Counter();singleton_hash=hashlib.sha256()
 for g in phase_rows:
  bad=[]
  for t in range(6):
   for d in range(1,6):
    colors=[g[(t+j*d)%6]for j in range(7)];phase_tests+=1
    if len(set(colors))==1:bad.append((t,d))
  if not bad:legal.append(g);continue
  illegal.append(g)
  choices=[(t,3)for t in range(6)if g[t]==g[(t+3)%6]]
  if not choices:choices=[(t,2)for t in range(6)if len({g[(t+j*2)%6]for j in range(3)})==1]
  need(choices,'every illegal row has explicit short singleton cycle');t,d=choices[0];step=103*d;cycle=618//math.gcd(step,618);singleton_steps[step]+=1
  for r in range(103):
   start=crt(r,t);first=min(positive((start+j*step)%618)for j in range(cycle));end=first+6*step;singleton_max=max(singleton_max,end)
   need(first<=step and end<=2163,'whole singleton lift bound')
   words=[first+j*step for j in range(7)];need(len(set(words))==7 and all(n%103==r for n in words),'nonconstant actual integer singleton AP')
   for palette in [0,1]:
    colors=[g[n%6]^palette for n in words];need(len(set(colors))==1,'actual singleton color witness');singleton_checks+=1;singleton_hash.update(enc([g,r,palette,words,colors]))
 need(set(legal)=={tuple(SIG[(t-c)%6]for t in range(6))for c in range(6)},'exact six legal rotations among all64 rows')
 affine=pointchecks=0;maxendpoint=0;minimum_steps=set();maphash=hashlib.sha256()
 for aa in range(1,103):
  inv=pow(aa,-1,103);A=crt(inv,1);need(math.gcd(A,618)==1,'every affine CRT unit')
  for beta in range(103):
   r0=(-beta*inv)%103
   for c in range(6):
    B=crt(r0,c);g=tuple(SIG[(t-c)%6]for t in range(6));ap=[(A*n+B)%618 for n in range(80,87)]
    for old,new in zip(range(80,87),ap):
     need((aa*(new%103)+beta)%103==old%103 and g[new%6]==SIG[old%6],'actual generic affine character/phase identity');pointchecks+=1
    need(r0 not in {n%103 for n in ap},'affine orbit avoids free root')
    colors=[L((aa*(n%103)+beta)%103)^g[n%6]for n in ap];need(len(set(colors))==1,'actual affine bad AP')
    step=A
    if step>309:ap=list(reversed(ap));step=618-step
    minimum_steps.add(step);need(0<step<=307 and math.gcd(step,618)==1,'unit step improves general309 to307')
    first=positive(ap[0]);words=[first+j*step for j in range(7)];need([n%618 for n in words]==ap and len(set(words))==7,'whole integer lift matches original cyclic points')
    endpoint=words[-1];need(endpoint<=2460,'uniform2460 sufficient interval');maxendpoint=max(maxendpoint,endpoint);affine+=1;maphash.update(enc([aa,beta,c,A,B,ap,words]))
    need(affine<=2_000_000,'INCOMPLETE fixed2M affine stage guard')
 rec={'complete':True,'author_code_maps_imported':False,'field_squares':len(squares),'all_multiplicativity_inputs':checks,'canonical_bad_APs':len(transcript),'canonical_actual_point_values':7*len(transcript),'all64_phase_rows':len(phase_rows),'complete_phase_start_step_tests':phase_tests,'legal_six_rows':[list(g)for g in sorted(legal)],'illegal_rows':len(illegal),'repeated_modular_singleton_witnesses':singleton_checks,'all103_field_columns_in_singleton_controls':True,'singleton_step_row_counts':dict(sorted(singleton_steps.items())),'singleton_maximum_integer_endpoint':singleton_max,'whole_singleton_transcript_sha256':singleton_hash.hexdigest(),'all_affine_phase_parameter_sets':affine,'actual_affine_point_identities':pointchecks,'whole_affine_transcript_sha256':maphash.hexdigest(),'maximum_unit_short_step':max(minimum_steps),'maximum_affine_orbit_integer_endpoint':maxendpoint,'new_sufficient_interval_threshold':2460,'new_illegal_phase_sufficient_threshold':2163,'optimal_interval_threshold_claimed':False,'all_affine_full_orbit_rows_claimed':False,'ordinary_generic_transport_required':True,'canonical_transcript_sha256':hashlib.sha256(enc(transcript)).hexdigest()}
 (a.work/'PHYSICAL_POINTS.json').write_bytes(enc(transcript));print(json.dumps(rec,sort_keys=True))
if __name__=='__main__':main()
