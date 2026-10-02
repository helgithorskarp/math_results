"""Optional late comparison with an explicit author EXPECTED file; no author code."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,signal
from linear import need,digest,canonical
from affine import matrices,mix,orbit_data,orbit_form

def main():
 signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('fixed60s late comparison')));signal.alarm(60)
 p=argparse.ArgumentParser();p.add_argument('expected');p.add_argument('phase',choices=['calibrations','negative','positive']);p.add_argument('--q',type=int);a=p.parse_args();root=Path(__file__).resolve().parent
 author=json.loads(Path(a.expected).read_text());rows=[]
 def compare(v,target):
  need(all(canonical(x)==target[k]for k,x in v.items()),'every named independent shared field');rows.append(v)
 if a.phase=='calibrations':
  ours=json.loads((root/'EXPECTED-calibrations.json').read_text())['records'];their=author['phases'][0]['calibrations'];need(len(ours)==len(their)==35,'complete calibration list')
  for r,t in zip(ours,their):
   q,k=r['q'],r['k'];e,aa=r['mean_pair_Gram'][0];T=r['mean_pair_Gram'][1][1];S=r['four_derivative'][0][0];h=F(1,3*q+5);B=F(T)*F(S)-2*F(aa)*q*h
   compare({'q':q,'k':k,'N':r['N'],'E':e,'A':aa,'T':T,'S':S,'B':B,'F0':r['F0'],'P':int(4*q*q*F(r['F0'])),'stronger_Q0':r['Q0'],'stronger_Delta':r['D4']},t)
 elif a.phase=='negative':
  ours=json.loads((root/'EXPECTED-negative.json').read_text())['cases'];their=author['phases'][1]['all_real_ansatz_exclusions'];need(len(ours)==len(their)==14,'complete negative list')
  for t in their:
   r=ours[str(t['q'])]['records'][0];compare({'q':r['q'],'k':5,'N':r['N'],'s':3*r['q']+4,'U0':r['negative_U0'],'Delta':r['positive_Delta'],'R':'0','lower_z_Delta':r['lower_alpha']},t)
 else:
  q=a.q;need(q is not None and 19<=q<=23,'complete positive fixture');r=json.loads((root/'EXPECTED-positive.json').read_text())['cases'][str(q)]['records'][0];t=next(z for z in author['phases'][2:7]if z['q']==q)
  S,Z,C0,D,R,U0=matrices(q,5);N=len(S);s=3*q+4;kap=F(1,4096);C=mix(mix(C0,D,kap),R,4);U=mix(mix(U0,D,-kap),R,-4);sums=[sum(x)for x in C];L=[[1+sum(sums)]+[1-x for x in sums]]+[[1-sums[i]]+[1+x for x in row]for i,row in enumerate(C)]
  need(digest(L)==r['whole_L_sha256'],'late reconstructed whole matrix matches sealed original record')
  M=[[(L[i][j]-s*(i==j))/F(N-s)for j in range(N)]for i in range(N)];keys,groups,w=orbit_data(S,Z,q,5);G=orbit_form(C,groups);H=orbit_form(U,groups)
  need(digest(G)==r['orbit_Gram_sha256']and digest(H)==r['orbit_cap_sha256'],'late original forms match sealed hashes')
  compare({'q':q,'N':N,'s':s,'kappa':kap,'t':F(4),'whole_ordered_entries':N*N,'M_empty_empty':r['actual_empty_M_loop'],'whole_M_digest':digest(M),'star_census':[s,s-5,s-5]+[q+5]*5+[q+6]*(q-5)},t)
  compare({'q':q,'N':N,'orbit_count':23,'orbit_keys':keys,'orbit_sizes':w,'complement_dimension':N-1-23,'whole_lower_rank':N-1,'whole_cap_rank':N-1,'lower_nonempty_floor':r['nonempty_lower_floor'],'physical_projected_cap_floor':r['physical_whole_cap_floor'],'complement_lower_floor':kap/2,'complement_cap_floor':N-2*s,'Gram_digest':digest([G,H])},t['orbit_certificate'])
 print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','phase':a.phase,'q':a.q,'shared_fields':sum(len(z)for z in rows),'whole_compared_field_values':canonical(rows),'trust':'late explicitly read author EXPECTED; no author modules; characteristic coefficient fingerprints and narrative fields not independently regenerated'},sort_keys=True,indent=2));signal.alarm(0)
if __name__=='__main__':main()
