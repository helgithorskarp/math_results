"""Fresh full four-coefficient original-pair baselines, unchanged owned generator."""
from fractions import Fraction as F
from affine import table,repair
from physical import singleton,typ,key,entry
from orbits import forms
from linear import need,canonical,digest

def one(q,k):
 S,Z,stars=singleton(q,k);non=S[1:];N=len(S);s=3*q+4;g=forms(q,k);where={wanted:i for i,wanted in enumerate(g['keys'])};classes=[where[key(A,Z)]for A in non];out=[[[F(0)]*23 for unused in range(23)]for f in range(4)];Q0=table(q,0);Q1=table(q,1);slopes={code:v-Q0[code]for code,v in Q1.items()};zero_rows=[];kernel=[F(1-int(bool(A&2))-int(bool(A&4))+int((A&7).bit_count()>=2))for A in non]
 for i,A in enumerate(non):
  zr=F(0)
  for j,B in enumerate(non):
   c0=entry(A,B,s,Q0,F(0));de=F(0)if A==B or A&B else slopes[tuple(sorted((typ(A),typ(B))))];r=repair(A,B);u=F(N*(A==B)-1)-c0
   for f,v in enumerate([c0,de,r,u]):out[f][classes[i]][classes[j]]+=v
   zr+=c0*kernel[j]
  need(zr==0,'EVERY literal original lower kernel row');zero_rows.append(zr)
 for name,A in zip(['C0','Delta','R','U0'],out):need(A==g[name],'EVERY full original coefficient Gram '+name)
 return {'q':q,'k':k,'N':N,'all_original_nonempty_positions':len(non)**2,'orbit_keys':g['keys'],'norm_weights':g['sizes'],'all_four_Grams_sha256':digest(out),'all_kernel_rows_sha256':digest(zero_rows),'all_star_sizes':stars,'family_sha256':digest(S),'unchanged_owned_generator':True}
if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s four-coefficient baselines; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);print(json.dumps(canonical([one(19,5),one(24,6)]),sort_keys=True,separators=(',',':')))
