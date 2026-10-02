"""Late schema adapter; no original executable is imported."""
import argparse,json,hashlib
from pathlib import Path

def need(x,s):
 if not x:raise ValueError(s)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);p.add_argument('--original-work',type=Path,required=True);a=p.parse_args()
 own=json.loads(a.record.read_bytes());native=json.loads((a.original_work/'primary/catalog.json').read_bytes())['rows']
 rows=[]
 for r in own['rows']:
  rows.append(dict(fixture=r['fixture'],hub_high=r['hubs'],h=r['h'],e=r['e'],k=r['k'],q=r['q'],
   eligible=r['eligible'],g1_S=r['g1'],ss_excess=r['sigma'],hub_weight=sum(5-r['replication'][p]for p in r['hubs']),
   psi=r['psi'],margin=r['margin3']))
 rows.sort(key=lambda r:(r['fixture'],r['hub_high']));need(rows==native,'EVERY original row field differs')
 branches=json.loads((a.original_work/'primary/boundaries.json').read_bytes())['branches']
 need(len(branches)==len(own['boundaries'])==4,'complete four boundary branches')
 fields=['e','k','q','eligible','h','g1_S','psi','margin','ss_excess'];keys=[0,1,2,3,4,5,7,8,6]
 for b,t in zip(own['boundaries'],branches):
  types=sorted({tuple(r[i]for i in keys)for r in b['types']});original_types=[[r[i]for i in keys]for r in b['types']]
  templates=sorted([[sum(row['counts'][i]for i,tt in enumerate(original_types)if tt==list(typ))for typ in types]for row in b['compositions']])
  parity=[]
  for counts in templates:
   mixed=[(typ,count)for typ,count in zip(types,counts)if typ[0]and count];M=sum(count for _,count in mixed)
   need(all(typ[0]==1 and typ[1]==1 and typ[3]and typ[4]==4 and typ[5]==3 for typ,_ in mixed),'actual nonunit category roles')
   need(M%2==1,'odd handshake premise')
   parity.append(dict(nonunit_rows=M,degree_per_nonunit_row=3,degree_sum=3*M,odd_degree_sum=True,
    ordinary_bridge='All these nonunit rows are eligible; local9249 forbids their deficit-one saturated neighbors from being unit.'))
  ref=dict(m=b['m'],n=b['n'],P=b['P'],T=0,X=0,tau=0,Q=b['Q'],E=b['E'],W=b['K']+b['E'],K=b['K'],
   margin_budget=3*b['delta'],category_fields=fields,types=[list(x)for x in types],templates=templates,parity=parity,
   status='NO_NECESSARY_CATEGORY_INVENTORY'if not templates else 'ALL_TEMPLATES_HAVE_ODD_THREE_REGULAR_NONUNIT_BLOCK')
  need(t==ref,'EVERY original category/template/constant/parity differs')
 print(json.dumps({'all_original_row_fields':len(rows),'all_original_boundary_branches':len(branches),
  'projected_original_row_sha256':hashlib.sha256(canonical(rows)).hexdigest(),
  'projected_original_branches_sha256':hashlib.sha256(canonical(branches)).hexdigest(),
  'original_executable_imported':False},sort_keys=True))
if __name__=='__main__':main()
