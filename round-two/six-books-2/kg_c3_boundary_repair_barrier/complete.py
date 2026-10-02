from pathlib import Path
from itertools import combinations
import hashlib,json,resource,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
work=Path(sys.argv[1])
import model,literal
start=time.monotonic();deadline=start+25
g=model.geometry();cases=json.loads((work/'unresolved.json').read_text())
reports=[];valid=[];total=0
for case in cases:
 pool=case['eligible_promotions'];rows=model.graph(g,case['J'],case['P'],case['D'])
 previous=0;red_ok=0;blue_ok=0;both=0;red_hist={}
 for step in range(1<<len(pool)):
  gray=step^(step>>1);changed=gray^previous
  if changed:model.toggle(rows,g[3][pool[changed.bit_length()-1]])
  previous=gray;total+=1
  red=all((rows[u]&rows[v]).bit_count()<4 for u,v in model.PAIRS if rows[u]>>v&1)
  blue=model.blue_bad(rows) is None
  red_ok+=red;blue_ok+=blue;both+=red and blue
  if red and blue:
   P=sorted(case['P']+[p for i,p in enumerate(pool) if gray>>i&1])
   native=literal.rows(literal.geometry(),case['J'],P,case['D'])
   summary=model.literal_summary(native)
   if summary['violations']:raise ValueError('candidate fails independent literal all-spine audit')
   valid.append(dict(J=case['J'],P=P,D=case['D'],rows=rows[:],summary=summary))
  if time.monotonic()>deadline:raise TimeoutError('predeclared25-second completion guard')
 reports.append(dict(J=case['J'],P=case['P'],D=case['D'],pool=pool,
                     subsets=1<<len(pool),red_valid=red_ok,blue_valid=blue_ok,both_valid=both))
out=work
body=json.dumps(reports,sort_keys=True,separators=(',',':'))+'\n';(out/'case-records.json').write_text(body)
(out/'valid.json').write_text(json.dumps(valid,indent=2)+'\n')
report=dict(status='COMPLETE_ALL_RESIDUAL_PROMOTION_SUBSETS',author='six-books-2',role='researcher',
            remaining_pools=len(cases),complete_subset_tests=total,
            red_valid=sum(r['red_valid'] for r in reports),blue_valid=sum(r['blue_valid'] for r in reports),
            both_valid=len(valid),seconds=time.monotonic()-start,
            case_records_sha256=hashlib.sha256(body.encode()).hexdigest(),
            peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            scope='All promotion subsets in all residual individually-red-valid pools, no degree bound or edge-count filtering. Other1634-10 repaired recipes are blue-obstructed even in the full pool. Parent completeness comes from the credited p4/q9 census. No genericp5 or arbitrary22-host claim.')
(out/'completion-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
