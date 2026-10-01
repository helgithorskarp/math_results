"""Generate or replay one complete dyadic packing-exclusion certificate.

Run check.py and audit.py first. Bulky generated traces stay in local scratch;
the publication retains only exact summary statistics and trace hashes.
"""
from pathlib import Path
import argparse,hashlib,json
import intervals as e
HERE=Path(__file__).resolve().parent
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def summary(index,rows):
 branch=e.BRANCHES[index];trace=e.manifest(rows)
 return {'branch':index,'sign':branch[0],'factor':branch[1],'pair':list(branch[-1]),
         'pieces':len(rows),'max_depth':max(a[-1] for a in rows),
         'minimum_gap':str(min(e.Q(a[-2],e.S) for a in rows)),
         'trace_sha256':hashlib.sha256(canonical(trace).encode()).hexdigest()}
def replay(index,trace):
 sign,factor,a,b,pair=e.BRANCHES[index]
 rows=[];next_left=e.LO
 for item in trace:
  e.require(len(item)==6,'literal trace record')
  left,right,aa,bb,gap=map(e.Q,item[:5]);depth=item[5]
  e.require(next_left==left<right<=e.HI,'entire closed partition in order')
  e.require(a<=aa<bb<=b,'retained root bracket')
  e.require(type(depth)is int and 0<=depth<=14,'bounded proof subdivision')
  polynomial=e.factor_bernstein(sign,factor,left,right)
  e.require(e.point_sign(polynomial,aa)*e.point_sign(polynomial,bb)==-1,'uniform root coverage')
  P,H=e.build(e.I(left,right),e.I(aa,bb),sign)
  bound=e.dot(P[pair[0]],P[pair[1]],H)-e.I(left,right)
  e.require(bound.l>0 and gap==e.Q(bound.l,e.S),'replayed exact positive packing gap')
  rows.append((left,right,aa,bb,bound.l,depth));next_left=right
 e.require(rows and next_left==e.HI,'no missing parameter endpoint or interval')
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--branch',type=int,choices=range(6),required=True)
 p.add_argument('--trace',type=Path)
 p.add_argument('--replay',type=Path)
 args=p.parse_args()
 expected=json.loads((HERE/'SELECT_EXPECTED.json').read_text())[args.branch]
 if args.replay:rows=replay(args.branch,json.loads(args.replay.read_text()))
 else:rows=e.prove(e.BRANCHES[args.branch],e.LO,e.HI)
 actual=summary(args.branch,rows)
 e.require(actual==expected,'complete branch certificate matches the published exact summary')
 e.require(e.Q(actual['minimum_gap'])>e.Q(1,10000),'uniform positive exclusion margin')
 if args.trace:args.trace.write_text(canonical(e.manifest(rows))+'\n')
 print(json.dumps(actual,sort_keys=True))
