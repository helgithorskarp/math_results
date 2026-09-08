from pathlib import Path
from collections import Counter
import json,base64,time
import argparse
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
a=ap.parse_args();OUT=a.work;OUT.mkdir(parents=True,exist_ok=True)
source=json.loads((REPO/'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json').read_text());V=source['labels'];ix={v:i for i,v in enumerate(V)};ex=json.loads((OUT/'exterior.json').read_text());N=len(ex)
old=json.loads((REPO/'hadwiger_nelson_heule516_single_point_h632_closure/certificate.json').read_text())['deletion_rows'];new=json.loads((OUT/'new_deletion_rows.json').read_text())
counts=[[0]*len(V) for _ in ex]
def extensions(row):
    v=row['removed'];raw=base64.b64decode(row['colours']);word=[(raw[i//4]>>(2*(i%4)))&3 for i in range(len(V)-1)];c=dict(zip([u for u in V if u!=v],word))
    return [i for i,r in enumerate(ex) if len({c[V[j]] for j in r['neighbors'] if V[j]!=v})<4]
new_ex=[]
for row in old+new:
    v=ix[row['removed']];covered=extensions(row)
    for i in covered:counts[i][v]+=1
for row in new:new_ex.append(extensions(row))
coverage=[sum(x>0 for x in r) for r in counts];keep=set(range(len(new)))
for j in reversed(range(len(new))):
    v=ix[new[j]['removed']];affected=[i for i in new_ex[j] if counts[i][v]==1]
    if any(coverage[i]<=508 for i in affected):continue
    keep.remove(j)
    for i in new_ex[j]:counts[i][v]-=1
    for i in affected:coverage[i]-=1
rows=sorted([new[j] for j in keep],key=lambda r:(r['removed'],r['colours']))
cert={'source_sha256':'3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51','target_order':508,'outside_H632_points':558,'additional_deletion_rows':rows}
(OUT/'certificate.json').write_text(json.dumps(cert,separators=(',',':'),sort_keys=True)+'\n')
result={'original_additional_rows':len(new),'retained_additional_rows':len(rows),'minimum_coverage':min(coverage),'coverage_histogram':dict(sorted(Counter(coverage).items())),'certificate_bytes':(OUT/'certificate.json').stat().st_size,'method':'Single reverse-order greedy removal of redundant new colour words with existing664 rows fixed.'}
(OUT/'COMPACT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
