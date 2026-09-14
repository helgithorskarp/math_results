"""Optional deterministic positive-witness generation; SAT is not a proof premise."""
import argparse,json
from pathlib import Path
from pysat.solvers import Cadical153
import model as m

def formula(n,E,selected=None,allowed=None,pins=None):
 s=Cadical153();selected=set(range(n))if selected is None else set(selected)
 for i in selected:s.add_clause([4*i+c+1 for c in range(4)])
 for i,j in E:
  if i in selected and j in selected:
   for c in range(4):s.add_clause([-4*i-c-1,-4*j-c-1])
 for i,colors in (allowed or {}).items():
  if i in selected:
   for c in set(range(4))-set(colors):s.add_clause([-4*i-c-1])
 for i,c in (pins or {}).items():
  if i in selected:s.add_clause([4*i+c+1])
 return s
def word(s,n,E,selected=None,pins=None):
 selected=set(range(n))if selected is None else set(selected);pins=pins or {}
 s.conf_budget(200000);ans=s.solve_limited()
 if ans is not True:raise RuntimeError('positive witness missing: '+str(ans))
 true=set(s.get_model());w=['.']*n
 for i in selected:
  # At-least-one encoding may assign multiple true colours. Honour pins.
  c=pins[i]if i in pins else next(c for c in range(4)if 4*i+c+1 in true)
  if 4*i+c+1 not in true:raise ValueError('pin absent from model')
  w[i]=str(c)
 if any(w[i]==w[j]for i,j in E if i in selected and j in selected):raise ValueError('bad model')
 return ''.join(w)
def run():
 _,S=m.sources();E=m.edges(S);N=[i for i,z in enumerate(S)if m.is_unit(z)]
 with formula(len(S),E,pins={0:0})as s:base=word(s,len(S),E,pins={0:0})
 deletions=[]
 for v in range(1,len(S)):
  selected=set(range(len(S)))-{v}
  with formula(len(S),E,selected,{i:[1,2]for i in N},{0:0})as s:
   deletions.append(word(s,len(S),E,selected,pins={0:0}))
 rows=[]
 for chord,P,es,T in m.frames():
  ws=[]
  for pat in m.bare_patterns(es,T):
   pins=dict(zip(T,pat))
   with formula(len(P),es,pins=pins)as s:ws.append(word(s,len(P),es,pins=pins))
  rows.append({'chord':list(chord),'words':ws})
 return {'format':'literal-colour-words-v1','source_word':base,'source_deletions':deletions,'frames':rows}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 if args.out.exists():raise SystemExit('output already exists')
 out=run();args.out.write_text(json.dumps(out,separators=(',',':'))+'\n')
 print(json.dumps({'status':'POSITIVE_WITNESSES','frames':len(out['frames']),'words':sum(len(r['words'])for r in out['frames'])}))
