"""Explicit semantic damages, actual covariance, and small exact controls."""
from pathlib import Path
from itertools import combinations,permutations
from copy import deepcopy
from collections import Counter
import json
import census,verify,reproduce
HERE=Path(__file__).resolve().parent
need=verify.need

def rejects(function,*args):
 try:function(*args)
 except (RuntimeError,ValueError,IndexError,KeyError):return
 raise RuntimeError('damaged semantic input was accepted')
def permute(word,permutation):return sum(1<<permutation[v]for v in range(18)if word>>v&1)
def first_role_map(first,second,m1,m2):
 u,v,y=m1;us,vs,xs=m2
 ta=sorted(tuple(p for p in r if p!=y)for r in first['q']if y in r);sa=sorted(tuple(p for p in r if p!=xs)for r in second['q']if xs in r)
 tu=next(r for r in ta if u in r);su=next(r for r in sa if us in r);mapping=[-1]*17;mapping[xs]=17;mapping[us]=u;mapping[vs]=v
 for a,b in zip([p for p in su if p!=us],[p for p in tu if p!=u]):mapping[a]=b
 for a,b in zip([r for r in sa if r!=su],[r for r in ta if r!=tu]):
  for p,q in zip(a,b):mapping[p]=q
 remaining=[p for p in range(18)if p!=y and p not in mapping]
 for a,b in zip([p for p in range(17)if mapping[p]<0],remaining):mapping[a]=b
 return mapping

def main():
 raw=json.loads((HERE/'fixtures.json').read_text());data=census.fixture_data();first,second,domain=census.marking_domains(data);entries=json.loads((HERE/'cores.json').read_text());fixtures=raw['stars'];damage=[]
 for name,mutate in [
  ('duplicate block',lambda z:z['stars'][0].__setitem__(0,z['stars'][0][1])),
  ('misaligned fixture groups',lambda z:z['groups'].pop()),
  ('out-of-domain point',lambda z:z['stars'][0][0].__setitem__(0,17)),
  ('nonbijection group',lambda z:z['groups'][1][0].__setitem__(0,z['groups'][1][0][1])),
  ('missing identity subgroup',lambda z:z['groups'][1].__setitem__(slice(None),[g for g in z['groups'][1]if g!=list(range(17))])),
  ('nonpreserving point map',lambda z:z['groups'][1].append([1,0,*range(2,17)])),
 ]:
  changed=deepcopy(raw);mutate(changed);rejects(census.fixture_data,changed);damage.append(name)
 base=entries[0];_,vertices=verify.check(base,fixtures)
 adjacent=next((i,j)for i,j in combinations(range(len(vertices)),2)if (vertices[i]&vertices[j]).bit_count()<=2)
 def clash(z):z['colors'][adjacent[1]]=z['colors'][adjacent[0]]
 for name,mutate in [
  ('noninjective map',lambda z:z['map'].__setitem__(0,z['map'][1])),
  ('missing word',lambda z:z['words'].pop()),
  ('invented physical image',lambda z:z['words'].__setitem__(0,z['words'][0]^1)),
  ('missing color',lambda z:z['colors'].pop()),
  ('Boolean color',lambda z:z['colors'].__setitem__(0,True)),
  ('compatible same-color pair',clash),
  ('understated capacity',lambda z:z.__setitem__('capacity',z['capacity']-1)),
  ('vertex population gap',lambda z:z.__setitem__('candidate_count',z['candidate_count']-1)),
  ('edge population gap',lambda z:z.__setitem__('edges',z['edges']-1)),
  ('wrong physical branch',lambda z:z.__setitem__('branch','44')),
  ('wrong role transport',lambda z:z['second_mark'].__setitem__(0,z['second_mark'][1])),
 ]:
  changed=deepcopy(base);mutate(changed);rejects(verify.check,changed,fixtures);damage.append(name)
 rejects(verify.check_all,entries[:-1],fixtures);damage.append('missing positive core')
 changed=deepcopy(entries);changed[1]=deepcopy(changed[0]);changed[1]['index']=1;rejects(verify.check_all,changed,fixtures);damage.append('duplicated positive core')
 # Bounded coverage-validator controls; the whole regenerated record is checked by reproduce.py.
 skeleton=[{'product':i,'partial_maps':2592,'represented_full_maps':15552,'expanded_full_maps':0,'surviving_partials':0,'first_fixture':0,'first_mark':(0,1,2),'second_fixture':0,'second_mark':(0,1,i)}for i in range(1652)]
 for name,mutate in [('missing product',lambda z:z.pop()),('partial universe gap',lambda z:z[0].__setitem__('partial_maps',2591)),('missing extension',lambda z:z[0].__setitem__('expanded_full_maps',1)),('duplicate product',lambda z:z.__setitem__(1,deepcopy(z[0])))]:
  changed=deepcopy(skeleton);mutate(changed);rejects(reproduce.coverage,changed);damage.append(name)
 # A real complete role-preserving common-tail bijection with a physical collision.
 (fi,m1),(se,m2)=first[0],second[0];mapping=first_role_map(data[fi],data[se],m1,m2);need(sorted(mapping)==[p for p in range(18)if p!=m1[2]],'negative map bijection')
 first_words={verify.mask([17,*r])for r in data[fi]['q']};second_words={verify.mask([m1[2],*(mapping[p]for p in r)])for r in data[se]['q']}
 need(len(first_words)==len(second_words)==20 and len(first_words&second_words)==4,'negative map actual common4')
 need([mapping[p]for p in m2]==[m1[0],m1[1],17],'negative map role images');rejects(verify.pack,sorted(first_words|second_words));damage.append('real role-preserving colliding map');negative_map={'first':[fi,m1],'second':[se,m2],'map':mapping}
 # Small graph checks distinguish a compatibility graph from its complement.
 a=verify.mask([0,1,2,3,4]);b=verify.mask([0,1,5,6,7]);c=verify.mask([0,1,2,5,6]);need(verify.proper([a,c],[0,0],1)==0,'incompatible vertices may share color');rejects(verify.proper,[a,b],[0,0],1)
 small=0
 for subset in combinations(range(7),5):
  q=verify.mask(subset)
  for subset2 in combinations(range(7),5):
   r=verify.mask(subset2)
   need((q&r).bit_count()==len(set(subset)&set(subset2)),'small literal intersection');small+=1
 # Whole final core/domain/color covariance under three actual18-point permutations.
 permutations_18=[[(v+1)%18 for v in range(18)],[17-v for v in range(18)],[(5*v+7)%18 for v in range(18)]];transports=0;transport_candidates=0
 for permutation in permutations_18:
  need(sorted(permutation)==list(range(18)),'actual transport bijection')
  for e in entries:
   _,vertices=verify.check(e,fixtures);u,v,y=e['first_mark'];words=sorted(permute(w,permutation)for w in e['words'])
   verify.physical(words,permutation[17],permutation[y],permutation[u],permutation[v],e['branch'])
   expected=sorted((permute(w,permutation),e['colors'][i])for i,w in enumerate(vertices));actual=verify.residual(words,permutation[17],permutation[y]);need(actual==[w for w,c in expected],'whole transported physical residual universe')
   need(verify.proper(actual,[c for w,c in expected],e['capacity'])==e['edges'],'all transported proper colors');transports+=1;transport_candidates+=len(actual)
 automatic=[];new_uv_leave=0;old_b_equals_v=0
 for fi,d in enumerate(data):
  for u in d['high']:
   if any(tuple(sorted((u,z)))in d['leave']for z in d['high']-{u}):continue
   for y in d['high']-{u}:
    if d['rho'][y]!=4:continue
    low=[v for v in range(17)if d['rho'][v]==5 and tuple(sorted((y,v)))in d['leave']]
    need(len(low)>=6-len(d['high']),'ordinary automatic-v multiplicity');need(len(low)==2,'generic exact-two automatic-v refinement');automatic.append([fi,u,y,len(d['high']),len(low)])
 for d in data:
  if min(d['rho'])<4:continue
  for x in d['high']:
   for u in range(17):
    if u==x or tuple(sorted((u,x)))in d['leave']:continue
    for v in range(17):
     if v in (u,x)or tuple(sorted((x,v)))not in d['leave']:continue
     if d['rho'][u]==4 and tuple(sorted((u,v)))in d['leave']:new_uv_leave+=1
     if d['rho'][u]==5 and d['rho'][v]==4 and tuple(sorted((u,v)))in d['leave']:old_b_equals_v+=1
 need(new_uv_leave==82 and old_b_equals_v==110,'boundary cases retained')
 new_entries=[e for e in entries if e['branch'][0]=='4'];need(len(new_entries)==3 and all(e['first_fixture']==e['second_fixture']==17 for e in new_entries),'both new stars are generic class17')
 d=data[17];hh=sorted(p for p in d['leave']if set(p)<=d['high']);degree=Counter(sum(v in e for e in hh)for v in d['high']);need(degree==Counter({2:4,0:1})and len(hh)==4,'unit high leave is isolated point plus C4')
 result={'new_branch_high_leave':hh,'new_branch_high_leave_degrees':dict(sorted(degree.items())),'automatic_v_exact_two':True,'damages_rejected':damage,'small_pair_checks':small,'actual_core_transports':transports,'transport_candidates':transport_candidates,'automatic_v_pairs':automatic,'new_raw_source_uv_leave':new_uv_leave,'old_raw_b_equals_v':old_b_equals_v,'coverage_controls_are_synthetic':True,'negative_colliding_map':negative_map}
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
