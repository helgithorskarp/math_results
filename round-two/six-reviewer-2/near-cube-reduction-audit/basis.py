"""Every cutoff and EVERY active affine coordinate at n6..14; no author imports."""
from fractions import Fraction as F
import hashlib,json,signal
from linear import need,canonical,digest,psd
from core import constants,architecture,pairs,free_pairs,complete,sector,embedding,core_upper_form

def audit():
 rows=[];directions=0;full_positions=0;embedding_positions=0;norms=0;automatic_positions=0;stream=hashlib.sha256();all_case_sectors=0
 for n in range(6,15):
  r,N,s,h=constants(n)
  for k in range(1,r+1):
   d,q=architecture(n,k);active=free_pairs(n,k);excluded=len(free_pairs(n))-len(active);t=max(d-k,0);need(excluded==(t*t if n%2 else t*(t-1)),'ALL proper excluded-coordinate counts');need(len(pairs(n))==n*n//4-1 and len(free_pairs(n))==(n-2)**2//4,'whole star-coordinate dimensions')
   vectors=[[F(0)]*len(active)]+[[F(i==p)for i in range(len(active))]for p in range(len(active))]+[[F((-1)**i*(2*i+3),i+1)for i in range(len(active))],[F((i%3)-1)for i in range(len(active))]];case_positions=0;case_hash=hashlib.sha256()
   for values in vectors:
    free={p:F(0)for p in free_pairs(n)};free.update(zip(active,values));beta=complete(n,free);sectors=[sector(n,beta,j)for j in range(d+1)];all_case_sectors+=len(sectors);need(sum(len(z['layers'])*z['multiplicity']for z in sectors)==N-1,'ENTIRE original harmonic dimension for every case');e=embedding(n,k,beta,sectors);embedding_positions+=e['positions'];norms+=e['nonzero_complement_norm_checks'];mathematics=[[z['layers'],z['metric'],z['K'],z['U'],z['Q'],z['G'],z['H'],z['W']]for z in sectors];raw=json.dumps(canonical(mathematics),sort_keys=True,separators=(',',':')).encode();case_hash.update(len(raw).to_bytes(8,'big'));case_hash.update(raw);stream.update(len(raw).to_bytes(8,'big'));stream.update(raw);positions=6*sum(len(z['layers'])**2 for z in sectors);full_positions+=positions;case_positions+=positions;directions+=1
   # Extremal signed complementary coefficients meet abs<=s exactly.
   # This is CONDITIONAL high-block validation, not claimed low0/1 positivity.
   for sign in[-1,1]:
    free={p:(F(sign*s)if sum(p)==n else F(0))for p in free_pairs(n)};beta=complete(n,free)
    for j in range(k+1,d+1):
     g=sector(n,beta,j);certificate=psd(core_upper_form(g,F(n-1)));automatic_positions+=len(g['layers'])**2
     need(certificate['rank']<=len(g['layers']),'entire automatic endpoint floor')
   rows.append({'n':n,'k':k,'d':d,'q':q,'star_rank':r,'all_free_coordinates':len(free_pairs(n)),'active_coordinates':len(active),'excluded_coordinates':excluded,'complete_affine_vectors':len(vectors),'whole_full_field_positions':case_positions,'entire_case_fields_sha256':case_hash.hexdigest()})
 need(len(rows)==72,'EVERYn6..14 cutoff1..n-2')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','cases':rows,'complete_case_count':len(rows),'affine_vectors':directions,'full_sector_evaluations':all_case_sectors,'whole_full_field_positions':full_positions,'all_omitted_action_positions':embedding_positions,'all_physical_complement_norm_checks':norms,'all_signed_extremal_auto_floor_positions':automatic_positions,'whole_basis_field_stream_sha256':stream.hexdigest(),'scope':'Entire active affine coordinate basis PLUS affine constant and two signed rational mixtures, all72 original domains. Formula identities/coverage all-order proved ordinarily in PROOF.md, not extrapolated. Extremal automatic floors conditional on abs(beta_complement)<=s, not a low-sector feasibility claim.'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s complete basis audit; incomplete is not exclusion')));signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
