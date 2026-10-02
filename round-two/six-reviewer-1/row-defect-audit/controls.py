"""Damage checks for the independent mathematics; no asserts or optimization bypass."""
from exact import *
from model import *
from literal import build,inspect
from universal import audit as universal_audit

def rejected(fn,label):
 try:fn()
 except ValueError:return label
 raise ValueError('damage accepted:'+label)

def audit():
 labels=[];domain,C=build(7)
 for mode in ('empty-row','empty-loop','unordered-factor','drop-row','drop-loop'):
  labels.append(rejected(lambda:inspect(7,2,domain,C,mode),mode))
 for mode in ('diagonal','intersecting','disjoint-star','asymmetry'):
  B=[r[:] for r in C]
  if mode=='diagonal':i=j=0
  elif mode=='intersecting':i=domain.index(1);j=domain.index(3)
  else:i=domain.index(1);j=domain.index(2)
  B[i][j]+=1
  if mode!='asymmetry':B[j][i]=B[i][j]
  labels.append(rejected(lambda:inspect(7,2,domain,B),mode))
 p,q,r,f,g=profiles(64,11);beta=debias(64);A=F(133**3,16*64**6);B=F(133**2,16*64**4)
 labels.append(rejected(lambda:need(-beta==A*(3*64-2)/(1+(3*64-2)*B),'wrong_beta_sign'),'wrong_beta_sign'))
 labels.append(rejected(lambda:need(beta==A*(3*64-2),'missing_beta_denominator'),'missing_beta_denominator'))
 labels.append(rejected(lambda:need(F(1,2)<F(3969,11264),'unproved_half_floor'),'unproved_half_floor'))
 labels.append(rejected(lambda:need(F(6,256)*F(21,10)**6+F(3,256)*F(21,10)**4+F(73*73,12288)<F(5,2),'too_small_norm_constant'),'too_small_norm_constant'))
 # Norm must be on actual original sets, not on unweighted layer coordinates.
 true=sum(comb(64,a)*r[a-1]**2 for a in range(1,63));wrong=sum(x*x for x in r)
 labels.append(rejected(lambda:need(true==wrong,'wrong_layer_metric'),'wrong_layer_metric'))
 # A valid generic full cap attains its empty-column bound; H support is not claimed.
 N=7;u=[F(N-1,N)]+[-F(1,N)]*(N-1);norm=dot(u,u);A0=[[F(N)*x*y/norm for y in u] for x in u];sigma=A0[0][0];v=[-x for x in A0[0][1:]]
 need(sigma*sigma+dot(v,v)==N*sigma and sigma==N-1,'generic_cap_bound_tight')
 return {'rejected':labels,'generic_cap_example':{'N':N,'sigma':sigma,'v_norm2':dot(v,v),'H_support_claimed':False}}
