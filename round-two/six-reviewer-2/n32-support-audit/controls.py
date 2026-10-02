"""Exact adverse controls for ORIGINAL coordinates, complete sectors and guards."""
from fractions import Fraction as F
from pathlib import Path
from tempfile import TemporaryDirectory
import json,signal
from linear import need,canonical,psd,mv,digest
from core import read_seed,complete,sector,constants,choose,floor
from literal import original,column,basis_span

def audit():
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,ZeroDivisionError)as e:rejected.append({'name':name,'failure':str(e)});return
  raise ValueError('damaged control unexpectedly passed: '+name)
 free=read_seed();beta,dec=complete(32,free);n=32;r,N,s,h=constants(n)
 with TemporaryDirectory(prefix='reviewer2-n32-controls-')as td:
  seed=json.loads((Path(__file__).parent/'seed.json').read_text())
  changes=[('wrong-original-n',lambda z:z.update(n=31)),('wrong-ground-order',lambda z:z.update(N=N+1)),('missing-seed-coordinate',lambda z:z['free_values'].pop()),('duplicate-seed-coordinate',lambda z:z['free_pairs'].__setitem__(1,z['free_pairs'][0])),('inexact-seed-value',lambda z:z['free_values'].__setitem__(0,0.25)),('foreign-denominator',lambda z:z['free_values'].__setitem__(0,'1/7')),('wrong-support-metadata',lambda z:z.update(proper_support_cutoff=7)),('wrong-common-denominator',lambda z:z.update(common_denominator=10**23))]
  for name,change in changes:
   z=json.loads(json.dumps(seed));change(z);p=Path(td)/'bad.json';p.write_text(json.dumps(z));reject(name,lambda:read_seed(p))
 reject('missing-affine-coordinate',lambda:complete(32,{k:v for k,v in free.items()if k!=(2,2)}))
 reject('original-n32-allocation',lambda:original(32))
 reject('foreign-parameter-domain',lambda:sector(7,beta,0))
 reject('uncovered-high-sector',lambda:sector(32,beta,17))
 reject('negative-schur-diagonal',lambda:psd([[1,2],[2,1]]))
 reject('zero-diagonal-nonzero-residual',lambda:psd([[0,1],[1,0]]))
 reject('asymmetric-physical-form',lambda:psd([[1,1],[0,1]]))
 # Above-middle action has odd-degree sign and nontrivial physical norm.
 small,decoder=complete(6,{(2,2):-3,(2,3):4,(2,4):5,(3,3):-7});S=original(6)[1:];_,NN,ss,hh=constants(6)
 C=[[F(ss*(A==B)-1)+small.get(tuple(sorted((A.bit_count(),B.bit_count()))),F(0))*int(not(A&B))for B in S]for A in S]
 vectors=[column(S,((0,1),),a)for a in range(1,5)];g=sector(6,small,1);actual=mv(C,vectors[3]);good=[sum(g['K'][i][3]*vectors[i][x]for i in range(4))for x in range(56)]
 need(actual==good,'positive-control above-middle action')
 wrong=[ss*vectors[3][x]+sum(small.get(tuple(sorted((a,4))),F(0))*choose(6-a-1,3)*vectors[i][x]for i,a in enumerate(range(1,5)))for x in range(56)]
 reject('odd-harmonic-sign-omitted',lambda:need(actual==wrong,'literal above-middle disjoint action distinguishes odd sign'))
 reject('high-layer-norm-replaced-by-unit',lambda:need(sum(x*x for x in vectors[3])==2,'above-middle actual norm is 8, not 2'))
 # Literal actual-star and empty checks, rather than metadata changes alone.
 damaged=[row[:]for row in C];damaged[0][2]+=1;damaged[2][0]+=1;stars=[[F(bool(A&(1<<i)))for A in S]for i in range(6)]
 reject('damaged-original-star-entry',lambda:need(all(not any(mv(damaged,v))for v in stars),'literal point-star kernel violated'))
 cr=[sum(row)for row in C];empty=1+sum(cr);er=[1-v for v in cr]
 reject('empty-loop-omitted',lambda:need(sum(er)==NN,'actual empty row including loop is necessary'))
 reject('noncentered-empty-row-held-at-one',lambda:need(all(v==1 for v in er),'actual empty offdiagonal row is not centered'))
 # Dropping j16 loses its whole one-dimensional multiplicity, not a sample.
 dimension=sum(len(sector(32,beta,j)['layers'])*sector(32,beta,j)['multiplicity']for j in range(16))
 reject('last-harmonic-sector-dropped',lambda:need(dimension==N-1,'complete original harmonic census'))
 largest=sector(32,beta,16);too_large=F(h)+abs(beta[16,16])+1
 reject('false-whole-cap-floor',lambda:floor(largest,too_large))
 # High/mean principal cap is retained: ordinary uncapped H is a negative control.
 reference={p:F(s-1)if sum(p)==32 else F(0)for p in free};rb,_=complete(32,reference);ug=sector(32,rb,0)
 reject('ordinary-H-assumed-capped-without-mean',lambda:psd(ug['H']))
 positive=psd([[2,1],[1,2]]);semidefinite=psd([[1,1],[1,1]]);need(positive['rank']==2 and semidefinite['rank']==1,'positive exact Schur controls')
 need(len(rejected)==23,'whole adverse control census')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','rejected':rejected,'rejections':len(rejected),'positive_schur_controls':[positive,semidefinite],'whole_original_above_middle_good_action_sha256':digest(actual),'missing_last_sector_dimension':dimension,'last_sector_multiplicity':choose(32,16)-choose(32,15),'literal_adverse_seed_is_not_psd_claim':True,'scope':'Explicit exceptions survive python-O; guards are not mathematical exclusions. All false witnesses/decoder/sign/whole mean/empty/coverage failures apply to original domains.'}

if __name__=='__main__':
 def alarm(*args):raise TimeoutError('fixed45s controls; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
