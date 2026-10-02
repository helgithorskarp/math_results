"""Postseal framing adapter; imports own code only, late original EXPECTED input explicitly pinned."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
import argparse,signal
parser=argparse.ArgumentParser(description='Late own-only numeric and whole-stream comparison, not primary proof evidence')
parser.add_argument('--author-expected',required=True,type=Path)
args=parser.parse_args()
def guarded(signum,frame):raise TimeoutError('unchanged60s late comparison guard; not mathematical exclusion')
signal.signal(signal.SIGALRM,guarded);signal.alarm(60)
source=Path(__file__).resolve().parent;sys.path.insert(0,str(source))
from linear import need,canonical,digest
from variance import scalar,constant_row
from physical import singleton,entry
from affine import table
from sparse import b0,scale,serial,x,y
own=json.loads((source/'EXPECTED.json').read_text());native=json.loads(args.author_expected.read_text());records={tuple(r['phase']):r['record']for r in own['records']}
count=0;compared=[]
mapping={'q':'q','k':'k','N':'N','s':'s','g':'g','e':'e','V':'V','strict_scalar_margin':'m','variance':'h0','nonempty_cap_floor_at_zero':'mu','kappa':'kappa','t':'t'}
def compare_scalar(a,b):
 global count
 fields=[]
 for key,value in b.items():
  if key=='certified_nonempty_and_projected_cap_floor':wanted=3*F(a['mu'])/4
  elif key=='alpha':wanted=F(a['q']*(a['q']+1),2)+F(3*(a['q']+1),3*a['q']+5)
  elif key in mapping:wanted=F(a[mapping[key]])
  else:continue
  need(wanted==F(value),'every native scalar field '+key);count+=1;fields.append(key)
 return fields
closure=records[('variance.py',)]
need(len(closure['cases'])==len(native['finite_closure'])==192,'full finite case list')
for a,b in zip(closure['cases'],native['finite_closure']):
 fields=compare_scalar(a,b);compared.append({'q':a['q'],'k':a['k'],'fields':fields})
pell=[]
for b in native['Pell_calibrations_only']:
 a=scalar(b['q'],b['k']);fields=compare_scalar(a,b);pell.append({'q':b['q'],'k':b['k'],'fields':fields})
need(len(pell)==42,'full native Pell calibration list')
point=records[('physical.py','point','24','6')];p=native['exceptional_point']
need(point['orbit_keys']==p['orbit_keys']and point['norm_weights']==p['orbit_sizes'],'every native orbit key and physical norm')
need(digest([point['whole_lower_Gram'],point['whole_upper_Gram']])==p['Gram_digest'],'complete native two-Gram hash framing from independently frozen forms')
for ownkey,nativekey in [('N','N'),('q','q'),('k','k'),('s','s'),('kappa','kappa'),('t','t'),('lower_floor','lower_nonempty_floor'),('upper_floor','physical_projected_cap_floor'),('complement_dimension','complement_dimension'),('complement_lower_floor','complement_lower_floor'),('complement_upper_floor','complement_cap_floor'),('whole_lower_rank','whole_lower_rank'),('whole_cap_rank','whole_cap_rank'),('whole_original_nonempty_positions','original_nonempty_positions'),('actual_empty_M','M_empty_empty')]:
 need(F(point[ownkey])==F(p[nativekey]),'all exceptional scalar/rank/gap fields');count+=1
need(point['all_star_sizes']==p['star_census']and[p['strict_fixed_floor_ranks'][0],p['strict_fixed_floor_ranks'][1]]==[point['lower_certificate']['rank'],point['upper_certificate']['rank']],'all star sizes/fixed-floor ranks')
for a,b in zip(records[('physical.py','baseline')],native['original_row_baselines']):
 for key in ['q','k','N','e','V','original_positions']:need(F(a[key])==F(b[key]),'all original row baseline fields');count+=1
alg=native['algebra'];sy=records[('symbolic.py',)]
shift1=next(r['lhs']for r in sy['identities']if r['identity']=='k19 shifted variance lower-bound cubic');shift2=next(r['lhs']for r in sy['identities']if r['identity']=='k49 shifted Pell whole variance lower-bound cubic')
need([r[2]for r in shift1]==alg['all_k19_shifted_positive_cubic']and[r[2]for r in shift2]==alg['Pell_shifted_positive_cubic'],'all complete positive cubic coefficients')
need([[[i,j],v]for i,j,v in serial(scale(b0(x,y),2))]==alg['root_shift_coefficients'],'every root-shift coefficient')
need(F(sy['tail_residual'])==F(alg['tail_residual']),'exact tail residual')
whole=[]
for b in native['whole_entry_baselines']:
 q,k=b['q'],b['k'];a=records[('physical.py','point',str(q),str(k))];S,Z,stars=singleton(q,k);N=a['N'];s=a['s'];kap=F(a['kappa']);t=F(a['t']);Q=table(q,kap);h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
 loop=1+k*(s-k)+kap*(alpha-2*k*h);row={A:constant_row(A,q,k,Z,kap,t)for A in S[1:]};wire=hashlib.sha256()
 for A in S:
  for B in S:
   L=loop if A==B==0 else 1-row[B]if A==0 else 1-row[A]if B==0 else 1+entry(A,B,s,Q,t)
   M=(L-s*(A==B))/(N-s);wire.update(str(M).encode()+b'\n')
 need(wire.hexdigest()==b['whole_M_stream_sha256'],'ENTIRE original whole stream from own-only closed evaluator')
 need(F(a['actual_empty_M'])==F(b['M_empty_empty'])and a['whole_M_positions']==b['whole_positions'],'whole actual empty/positions')
 whole.append({'q':q,'k':k,'positions':N*N,'whole_stream_sha256':wire.hexdigest(),'entire_equal':True})
large=[]
for b in native['large_entry_calibrations_only']:
 r=b['parameters'];a=scalar(r['q'],r['k']);fields=compare_scalar(a,r);q,k=a['q'],a['k'];kap=a['kappa'];t=a['t'];h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
 M00=(1+k*(a['s']-k)+kap*(alpha-2*k*h)-a['s'])/(a['N']-a['s'])
 # At a there are no outside bits; its deleted action is k*(Q(a,bcx)-1).
 Qa=table(q,kap);row_a=kap*h-k*(Qa[tuple(sorted(((1,0),(2,1))))]-1)+2*t
 M0a=(1-row_a)/(a['N']-a['s']);need(M00==F(b['M_empty_empty'])and M0a==F(b['M_empty_a']),'every native large constant-size entry field');count+=2
 large.append({'q':q,'k':k,'all_fields':fields,'M00':M00,'M0a':M0a,'sample_only':True})
report={'agent':'six-reviewer-2','role':'independent mathematical reviewer','all192_native_scalar_cases':True,'all42_native_Pell_scalar_records':True,'all_exceptional_keys_norms_star_sizes_ranks_gaps':True,'complete_native_Gram_pair_hash_from_frozen_independent_forms_equal':True,'all_positive_cubic_root_coefficients_equal':True,'all_original_row_moment_fields_equal':True,'native_scalar_numeric_fields_compared':count,'whole_original_streams':whole,'large_samples':large,'no_author_function_import':True,'scope':'Own-only late framing adapter; full 293165 original whole stream and two frozen529Grams; secondary native characteristic coefficient fingerprints not independently regenerated. Native true flags alone not proof. Infinite coverage is written independent proof.'}
need(canonical(report)==json.loads((source/'COMPARISON.json').read_text()),'ENTIRE frozen late comparison record');signal.alarm(0);print(json.dumps(canonical(report),indent=2))
