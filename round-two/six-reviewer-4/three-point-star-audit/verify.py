"""Literal independent certificate checker: no census/color producer imported."""
from pathlib import Path
from itertools import combinations
import json,hashlib,sys
HERE=Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise RuntimeError(message)
def digest(z):return hashlib.sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()
def mask(points):return sum(1<<p for p in points)
def integer(v):return type(v)is int
def pack(words):
 need(len(words)==len(set(words))==36,'36 distinct words')
 need(all(integer(w)and 0<=w<1<<18 and w.bit_count()==5 for w in words),'literal words')
 need(all((a&b).bit_count()<=2 for a,b in combinations(words,2)),'literal core collision')
 return words

def physical(words,x,y,u,v,branch):
 pack(words)
 r=lambda p:sum(bool(w>>p&1)for w in words)
 pair=lambda p,q:sum(bool(w>>p&1 and w>>q&1)for w in words)
 covered=lambda p,q,s:any(all(w>>t&1 for t in (p,q,s))for w in words)
 need(len({x,y,u,v})==4,'four distinct roles')
 need(r(x)==r(y)==20 and pair(x,y)==4,'actual saturated centers/common4')
 need(pair(x,v)==5 and not covered(x,y,v),'actual first low v leave')
 high={p for p in range(18)if p!=x and pair(x,p)<5}
 need(u in high and all(covered(x,u,p)for p in high-{u}),'actual first isolation')
 need(all(pair(y,p)in (4,5)for p in range(18)if p!=y),'actual unit second row')
 need(branch==str(pair(y,u))+str(pair(y,v)),'actual branch')
 if branch[0]=='4':
  need(pair(x,u)==4 and all(pair(x,p)in (4,5)for p in range(18)if p!=x),'new branch first unit readout')
  need(pair(y,v)==5 and covered(y,u,v),'new branch structural readout')
 return {'x_pair_u':pair(x,u),'h':len(high),'yuv':covered(y,u,v)}

def residual(words,x,y):
 # Definition-level intersection check, independent of producer's triple flags.
 vertices=[];trials=0
 for points in combinations([p for p in range(18)if p not in (x,y)],5):
  trials+=1;w=mask(points)
  if all((w&a).bit_count()<=2 for a in words):vertices.append(w)
 need(trials==4368,'complete physical residual universe');vertices.sort()
 return vertices

def proper(vertices,colors,capacity):
 need(len(colors)==len(vertices),'one color per actual vertex')
 need(integer(capacity)and 0<=capacity<=31,'honest color bound')
 need(all(integer(c)and 0<=c<capacity for c in colors),'integer color domain')
 need(set(colors)==set(range(capacity)),'actual capacity')
 edges=0
 for i,j in combinations(range(len(vertices)),2):
  if (vertices[i]&vertices[j]).bit_count()<=2:
   edges+=1;need(colors[i]!=colors[j],'proper color on actual compatible pair')
 return edges

def check(entry,fixtures):
 need(integer(entry['index'])and integer(entry['own_product']),'actual identifiers')
 fi,se=entry['first_fixture'],entry['second_fixture'];m1,m2=entry['first_mark'],entry['second_mark'];mapping=entry['map'];u,v,y=m1
 need(all(integer(z)for z in mapping)and sorted(mapping)==[p for p in range(18)if p!=y],'actual source bijection')
 need(len(m1)==len(set(m1))==len(m2)==len(set(m2))==3,'actual marks')
 need(mapping[m2[0]]==u and mapping[m2[1]]==v and mapping[m2[2]]==17,'actual role images')
 first={mask([17,*r])for r in fixtures[fi]};second={mask([y,*(mapping[p]for p in r)])for r in fixtures[se]}
 need(len(first)==len(second)==20 and len(first&second)==4,'actual common words')
 words=sorted(first|second);need(words==entry['words'],'actual physical image arrays')
 structure=physical(words,17,y,u,v,entry['branch']);vertices=residual(words,17,y)
 need(len(vertices)==entry['candidate_count']and digest(vertices)==entry['candidate_sha256'],'whole actual vertex array')
 edges=proper(vertices,entry['colors'],entry['capacity']);need(edges==entry['edges']and entry['upper']==36+entry['capacity'],'edges and color bridge')
 return {'index':entry['index'],'product':entry['own_product'],'branch':entry['branch'],'core_sha256':digest(words),'candidate_count':len(vertices),'candidate_sha256':digest(vertices),'edges':edges,'capacity':entry['capacity'],'upper':entry['upper'],**structure},vertices

def check_all(entries,fixtures):
 need([e['index']for e in entries]==list(range(121)),'whole core index coverage')
 keys=[(e['own_product'],tuple(e['map']))for e in entries];need(len(set(keys))==121,'no duplicated core')
 records=[check(e,fixtures)[0]for e in entries]
 return {'cores':len(records),'residual_trials':4368*len(records),'candidates':sum(z['candidate_count']for z in records),'compatible_pairs':sum(z['edges']for z in records),'maximum_upper':max(z['upper']for z in records),'records':records}

if __name__=='__main__':
 fixtures=json.loads((HERE/'fixtures.json').read_text())['stars'];entries=json.loads((HERE/'cores.json').read_text());record=check_all(entries,fixtures)
 print(json.dumps(record,sort_keys=True,separators=(',',':')))
