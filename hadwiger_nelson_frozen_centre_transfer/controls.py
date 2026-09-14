"""Encoding, finite-search, geometry and deliberate-corruption controls."""
from pathlib import Path
from itertools import combinations,product
from tempfile import TemporaryDirectory
import copy,json
import model as m
import verify as v

def run():
 # Every four-vertex graph and every choice of restricted two-colour domains.
 possible=list(combinations(range(4),2));tests=0
 for mask in range(1<<len(possible)):
  E=[e for j,e in enumerate(possible)if mask>>j&1]
  for restrict in range(16):
   allowed=[3 if restrict>>i&1 else 15 for i in range(4)]
   naive=any(all(allowed[i]>>w[i]&1 for i in range(4))and all(w[a]!=w[b]for a,b in E)
             for w in product(range(4),repeat=4))
   ans,_=v.search(4,E,allowed)
   v.need((ans is not None)==naive,'finite-search/brute-force disagreement');tests+=1
 # Full exact geometry agreement, including independent collision handling.
 full,S=v.source();mf,ms=m.sources()
 v.need([v.ecoord(p)for p in full]==mf and [v.ecoord(p)for p in S]==ms,'source arithmetic disagreement')
 N=[i for i,z in enumerate(S)if v.unit(z)];frames=list(m.frames());j=0;checks=0
 for a,b in combinations(N,2):
  A,B=S[a],S[b];centre=v.add(A,B)
  if centre==v.ZERO:continue
  AB=v.mul(A,B);moved=[v.add(centre,v.neg(v.mul(AB,v.conj(z))))for z in S]
  P=list(S)+sorted(set(moved)-set(S),key=v.ecoord)
  chord,mp,me,T=frames[j];j+=1
  v.need(chord==(a,b)and [v.ecoord(z)for z in P]==mp,'frame point disagreement')
  v.need(v.edges(P)==me,'complete all-pairs edge disagreement')
  checks+=len(P)*(len(P)-1)//2
 v.need(j==86,'frame coverage')
 good=json.loads((Path(__file__).parent/'certificate.json').read_text());bad=[]
 c=copy.deepcopy(good);w=list(c['source_word']);e=m.edges(ms)[0];w[e[1]]=w[e[0]];c['source_word']=''.join(w);bad.append(c)
 c=copy.deepcopy(good);c['source_deletions'].pop();bad.append(c)
 c=copy.deepcopy(good);c['frames'].pop();bad.append(c)
 c=copy.deepcopy(good);c['frames'][0]['words'].pop();bad.append(c)
 c=copy.deepcopy(good);c['frames'][0]['chord'].reverse();bad.append(c)
 c=copy.deepcopy(good);w=c['frames'][0]['words'][0];c['frames'][0]['words'][0]=''.join(str((int(x)+1)%4)for x in w);bad.append(c)
 c=copy.deepcopy(good);c['source_deletions'][0]=c['source_word'];bad.append(c)
 c=copy.deepcopy(good);c['source_word']=c['source_word'][:-1]+'4';bad.append(c)
 rejected=0
 with TemporaryDirectory(prefix='hn-frozen-controls-')as td:
  p=Path(td)/'mutated.json'
  for c in bad:
   p.write_text(json.dumps(c))
   try:v.run(p)
   except ValueError:rejected+=1
   else:raise ValueError('malformed certificate accepted')
 return {'status':'VERIFIED','complete_small_search_cases':tests,'full_frame_pair_checks':checks,
         'rejected_corruptions':rejected,'independent_geometry_agreement':True}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
