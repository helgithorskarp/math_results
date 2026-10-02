"""Semantic rejection controls, with each damaged certificate rehashed.
Separate decoding and checking of every complete original witness record.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,sys,signal
from checker import check,check_signs,poly
from ring import shifted,record,R
from original import seed,lift
from linear import need,psd,mv,digest,canonical

def literal(d):
 a=seed(d['n'],d['r'],d['l']);N=a['N'];s=a['f']['s'];r=a['r'];sets=[0]+a['sets'];packet=d['matrix_for_late_comparison'];C=[[F(x) for x in row] for row in packet['C']];Q=[[F(x) for x in row] for row in packet['Q']];M=[[F(x) for x in row] for row in packet['M']]
 need(len(C)==N-1 and all(len(x)==N-1 for x in C),'ALL nonempty dimensions');need(len(Q)==len(M)==N and all(len(x)==N for x in Q+M),'ALL actual dimensions including empty');need(Q==lift(C),'ENTIRE actual empty and core lift');L=[[1+Q[i][j] for j in range(N)] for i in range(N)];need(M==[[(L[i][j]-s*F(i==j))/(N-s) for j in range(N)] for i in range(N)],'ENTIRE original M decoding')
 need(all(sum(x)==1 for x in M),'ALL original regularity rows');need(all(M[i][j]==M[j][i] and (not(sets[i]&sets[j]) or M[i][j]==0) for i in range(N) for j in range(N)),'ALL original symmetry/support/diagonal entries');rank=psd(L)['rank'];need(rank==d['lower_rank']==N-r-1+(d['phase']!='seed'),'ENTIRE original lower PSD/rank');gap=F(d['gap']);P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)];need(psd([[(N-gap)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)])['rank']==N-1,'ENTIRE original cap')
 for j in range(r):need(all(v==0 for v in mv(L,[F(bool(A>>j&1))-s/N for A in sets])),'EVERY row of EVERY maximum-star kernel')
 return {'N':N,'phase':d['phase'],'whole_positions':N*N,'all_star_kernel_positions':N*r,'lower_rank':rank,'gap':str(gap),'whole_decoded':digest(packet)}

def run(out):
 out=Path(out);records=[];reject=[]
 for p in sorted(out.glob('original-*.json')):
  d=json.loads(p.read_text())
  if 'matrix_for_late_comparison' in d:records.append(literal(d))
 base=json.loads((out/'generate-uniform.json').read_text());signs=json.loads((out/'generate-signs.json').read_text())
 def trial(name,mut,scalar=False):
  d=deepcopy(signs if scalar else base);mut(d);d.pop('whole_sha256');d['whole_sha256']=digest(d);p=out/'damaged-certificate.json';p.write_text(json.dumps(d))
  try:check_signs(p) if scalar else check(p,'fixed_inverse',1)
  except ValueError as e:reject.append({'name':name,'reason':str(e)});return
  raise ValueError('damaged certificate accepted: '+name)
 def c(d):return d['tests']['fixed_inverse'][0]
 trial('positive numerator wrong',lambda d:c(d)['numerator'][0].__setitem__(3,str(F(c(d)['numerator'][0][3])+1)))
 trial('original numerator wrong',lambda d:c(d)['original_numerator'][0].__setitem__(3,str(F(c(d)['original_numerator'][0][3])+1)))
 trial('negative denominator',lambda d:c(d)['denominator'].__setitem__('constant','-1'))
 trial('wrong positive denominator',lambda d:c(d)['denominator'].__setitem__('constant',str(2*F(c(d)['denominator']['constant']))))
 trial('negative row clearing',lambda d:c(d)['positive_row_clearings'][0].__setitem__('constant','-1'))
 trial('wrong positive removal',lambda d:c(d)['removed'].__setitem__('constant',str(2*F(c(d)['removed']['constant']))))
 trial('wrong cleared original entry',lambda d:c(d)['polynomial_matrix'][0][0]['original'][0].__setitem__(3,'999'))
 trial('wrong cleared shifted entry',lambda d:c(d)['polynomial_matrix'][0][0]['shifted'][0].__setitem__(3,'999'))
 trial('duplicate monomial',lambda d:c(d)['numerator'].append(list(c(d)['numerator'][0])))
 trial('zero coefficient',lambda d:c(d)['numerator'][0].__setitem__(3,'0'))
 trial('degree outside guard',lambda d:c(d)['numerator'][0].__setitem__(0,181))
 def consistent_wrong(d):
  x=c(d);x['original_numerator'][0][3]=str(F(x['original_numerator'][0][3])+1);x['numerator']=record(shifted(poly(x['original_numerator']),False))
 trial('consistent positive numerator but wrong determinant',consistent_wrong)
 trial('wrong norm value',lambda d:d['signs']['mu']['original_numerator'][0].__setitem__(3,'999'),True)
 trial('wrong residual floor',lambda d:d['signs']['pendant_floor']['numerator'][0].__setitem__(3,'999'),True)
 original=json.loads((out/'original-4-2-2-old.json').read_text())
 def whole_trial(name,mut):
  d=deepcopy(original);mut(d)
  try:literal(d)
  except ValueError as e:reject.append({'name':name,'reason':str(e)});return
  raise ValueError('damaged original accepted: '+name)
 whole_trial('missing actual empty',lambda d:d['matrix_for_late_comparison']['Q'].pop(0))
 whole_trial('stale empty loop',lambda d:d['matrix_for_late_comparison']['Q'][0].__setitem__(0,'999'))
 whole_trial('stale empty row',lambda d:d['matrix_for_late_comparison']['Q'][0].__setitem__(1,'999'))
 whole_trial('wrong original support',lambda d:d['matrix_for_late_comparison']['M'][1].__setitem__(1,'1'))
 whole_trial('wrong lower rank',lambda d:d.__setitem__('lower_rank',d['lower_rank']-1))
 whole_trial('false cap',lambda d:d.__setitem__('gap',str(d['N'])))
 whole_trial('wrong original core diagonal',lambda d:d['matrix_for_late_comparison']['C'][0].__setitem__(0,'999'))
 for name,fn in [('float coefficient',lambda:R(0.5)),('literal domain',lambda:seed(4,3,2)),('literal allocation',lambda:seed(7,3,2))]:
  try:fn()
  except ValueError as e:reject.append({'name':name,'reason':str(e)});continue
  raise ValueError('guard accepted '+name)
 need(len(records)==9 and len(reject)==24,'complete literal and rejection census');return {'whole_original_rechecks':records,'semantic_rejections':reject,'rehash_before_check':True}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s semantic phase')));signal.alarm(60);print(json.dumps(canonical(run(sys.argv[1])),sort_keys=True,separators=(',',':')))
