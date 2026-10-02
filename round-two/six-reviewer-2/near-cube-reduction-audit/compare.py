"""LATE adapter only: every target/new and prior sector against frozen own basis."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,signal
from core import constants,architecture,pairs,free_pairs,complete,sector,embedding
from linear import need,canonical,digest

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def audit(author):
 native=module('late_target_reduction',author/'reduction.py');prior=module('late_prior_model',author/'model.py');primary=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['phases']['basis'];rows=[];vectors_count=0;beta_positions=0;form_positions=0;transfers=0;stream=hashlib.sha256()
 for saved in primary['cases']:
  n,k=saved['n'],saved['k'];r,N,s,h=constants(n);d,q=architecture(n,k);active=free_pairs(n,k);free=free_pairs(n);meta=native.dimensions(n,k);need(meta=={'n':n,'k':k,'q':q,'supported':len(pairs(n)),'star_rank':r,'free':len(free),'excluded':len(free)-len(active),'active':len(active),'lower_degrees':list(range(q+1)),'upper_degrees':list(range(min(k,d)+1))},'ENTIRE native dimension architecture')
  vectors=[[F(0)]*len(active)]+[[F(i==p)for i in range(len(active))]for p in range(len(active))]+[[F((-1)**i*(2*i+3),i+1)for i in range(len(active))],[F((i%3)-1)for i in range(len(active))]];case_hash=hashlib.sha256();common_hash=hashlib.sha256();positions=0
  for values in vectors:
   fv={p:F(0)for p in free};fv.update(zip(active,values));beta=complete(n,fv);nb=native.complete_stars(n,[fv[p]for p in free]);need(all(nb[a][b]==beta.get(tuple(sorted((a,b))),F(0))for a in range(r+1)for b in range(r+1)),'ALL complete beta positions, including unsupported/zero rows');beta_positions+=(r+1)**2;native.validate(n,k,nb);old=prior.blocks(n,nb);own=[sector(n,beta,j)for j in range(d+1)];fields=[];common=[]
   for j,g in enumerate(own):
    aa,metric,K,U=native.quotient(n,j,nb);need((aa,metric,K,U)==(g['layers'],g['metric'],g['K'],g['U']),'ALL new-native coefficient/metric positions');need(old[j]==(j,aa,metric,K,U),'ALL unchanged prior-reference coefficient/metric positions');G=[[metric[i]*v for v in row]for i,row in enumerate(K)];H=[[metric[i]*v for v in row]for i,row in enumerate(U)];need(G==g['G']and H==g['H'],'ALL complete physical form positions');fields.append([aa,metric,K,U,g['Q'],G,H,g['W']]);common.append([aa,metric,K,U,G,H]);positions+=4*len(aa)**2
   e=embedding(n,k,beta,own);t=native.transfer(n,k,nb);need(t['positions']==e['positions']and t['omitted_degree_parent_order']==[[j,ell,len(aa)]for j,ell,aa,sg,hsh in e['complete_embeddings']],'ENTIRE native/own omitted parent/degree coverage');transfers+=e['positions']
   raw=json.dumps(canonical(fields),sort_keys=True,separators=(',',':')).encode();case_hash.update(len(raw).to_bytes(8,'big'));case_hash.update(raw);stream.update(len(raw).to_bytes(8,'big'));stream.update(raw);raw_common=json.dumps(canonical(common),sort_keys=True,separators=(',',':')).encode();common_hash.update(len(raw_common).to_bytes(8,'big'));common_hash.update(raw_common);vectors_count+=1
  need(case_hash.hexdigest()==saved['entire_case_fields_sha256'],'ENTIRE native reconstruction agrees with original frozen case, not selected fields');form_positions+=positions;rows.append({'n':n,'k':k,'vectors':len(vectors),'all_common_K_U_G_H_positions':positions,'entire_common_field_stream_sha256':common_hash.hexdigest(),'original_frozen_case_sha256':case_hash.hexdigest()})
 need(stream.hexdigest()==primary['whole_basis_field_stream_sha256']and vectors_count==primary['affine_vectors']and len(rows)==72,'ENTIRE frozen72-case basis record boundary')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','all72_cases':rows,'complete_affine_vectors':vectors_count,'all_full_beta_positions':beta_positions,'all_common_full_K_U_G_H_positions':form_positions,'all_complete_transfer_positions':transfers,'entire_frozen_basis_field_stream_sha256':stream.hexdigest(),'all_native_new_prior_own_fields_equal':True,'scope':'Late comparison, BOTH new native quotient and unchanged prior reference, all1476 affine vectors/all complete beta/physical forms/metrics/all72 cases. Q/W are the independently proved new metric and own frozen fields, not claimed native exports. Native count labels/basis43 metadata are different domains, not substituted for the own72-case record.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('author',type=Path);a=ap.parse_args();signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s full late fields')));signal.alarm(45);print(json.dumps(canonical(audit(a.author)),sort_keys=True,separators=(',',':')))
