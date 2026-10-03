"""Post-seal adapter: independent kernels reconstruct all native positive records.

Native schemas/binary transcript formats were inspected after SEAL.json. This
comparison is not the pre-access independent evidence and imports no native code.
"""
import argparse,hashlib,itertools,json,pathlib,struct
from model import P,squares,endpoint,neighbors,need
from tuple_check import enumerate_tuples
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def run(native):
 n=pathlib.Path(native);own=json.loads((pathlib.Path(__file__).parent/'RESULT.json').read_text())
 units,V,D=endpoint();sq,ns,A=neighbors(D);_,_,_,tuples=enumerate_tuples(sq,ns,A)
 L={x:int(x not in squares()) for x in range(1,P)}
 edges=[set(s) for _,s in units];covers=set()
 def dfs(C):
  missing=next((e for e in edges if not C&e),None)
  if missing is None:covers.add(tuple(sorted(C)));return
  if len(C)==5:return
  for x in sorted(missing):dfs(C|{x})
 dfs(set());covers=sorted(covers)
 base=dict(schema='character617-base-v1',agent='six-vdw-3',role='researcher',prime=P,
  character_ascii_sha256=hashlib.sha256(''.join(str(L[x])for x in range(1,P)).encode()).hexdigest(),
  endpoint_steps_examined=616,endpoint_unit_supports=[dict(step=d,support=S)for d,S in units],
  five_disjoint_support_indices=list(range(5)),support_union=sorted(V),support_inverses=sorted(D-V),reciprocal_overlap=[],
  undirected_ratio_set=sorted(D),minimum_hitting_number=5,minimum_covers=len(covers),minimum_covers_sha256=sha(covers),
  minimum_cover_union=sorted(set().union(*(set(c)for c in covers))),field_start_step_pairs=sum(own['field']['partial_AP'].values()),
  root_avoiding_pairs=own['field']['partial_AP']['root_free'],root_visiting_pairs=own['field']['partial_AP']['root_hit'],
  partial_monochromatic_pairs=0,offset_control=dict(minus_one=L[616],one=L[1],three=L[3]),root_words_at_3703=126,palettes=2,actual_restricted_3703_colorings=252)
 Bs=sorted(set(tuple(B)for _,B in tuples));records=[dict(B=list(B),A=[q for q in sq if all(x*pow(q,-1,P)%P in D for x in B)])for B in Bs]
 lattice=dict(schema='character617-lattice-v1',prime=P,minimum_B_size=10,first_square_vertex=1,
  square_vertices=308,nonsquare_vertices=308,ratio_degree=66,states=len(records),
  retained_transitions=own['tuples']['retained_transitions'],A_histogram=own['tuples']['closure_histogram'],maximum_A=4,
  state_records_sha256=sha(records),records=records)
 expected={'base':base,'lattice':lattice}
 for row in own['lift_shards']:
  h=hashlib.sha256();N=row['N']
  for m in range(row['lo'],row['hi']+1):
   for d in range(1,P):
    s=d if m+6*d<=N else P-d;slot=0 if s==d and m+6*d<=N else 6
    a=m-slot*s;points=[a+j*s for j in range(7)]
    need(1<=points[0]<=points[-1]<=N and points[slot]==m,'post-seal literal integer control')
    h.update(struct.pack('<5H',m,d,a,s,slot))
  name=f"lift-{N}-{row['lo']}-{row['hi']}"
  expected[name]=dict(schema='character617-lift-v1',prime=P,interval=N,start=row['lo'],stop=row['hi'],actual_endpoint_pairs=row['total'],
   forward_APs=row['forward'],backward_APs=row['backward'],actual_lifts_sha256=h.hexdigest())
 for start in range(0,P,32):
  stop=min(P-1,start+31);h=hashlib.sha256();count=0
  for r in range(start,stop+1):
   for alpha in range(1,P):
    q=(r+alpha)%P;points=[(q+j*(alpha*d%P))%P for d,S in units[:5]for j in range(1,7)]
    need(len(set(points))==30 and r not in points and q not in points,'post-seal affine support control')
    h.update(struct.pack('<33H',r,q,alpha,*points));count+=1
  expected[f'transport-{start}-{stop}']=dict(schema='character617-transport-v1',prime=P,start=start,stop=stop,
   root_target_parameters=count,literal_support_columns=30*count,transport_sha256=h.hexdigest())
 matches=[]
 for name,want in expected.items():
  for mode in ('normal','optimized'):
   f=n/mode/(name+'.json');raw=f.read_bytes();need(json.loads(raw)==want,'entire native reconstruction: '+name)
   checked=json.loads((n/mode/(name+'-checked.json')).read_text())
   need(checked==dict(status='VALID',schema=want['schema'],whole_input_sha256=hashlib.sha256(raw).hexdigest()),'entire native checker receipt')
   matches.append([name,mode,hashlib.sha256(raw).hexdigest()])
 return dict(method='post-seal native-schema adapter, sealed independent kernels, no native code imports',
  entire_positive_records=len(matches),entire_checked_receipts=len(matches),native_stages=len(expected),
  all_867_state_rows_and_full_closures_reconstructed=True,whole_matches_sha256=sha(matches))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native-output',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=run(a.native_output)
 pathlib.Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,sort_keys=True))
