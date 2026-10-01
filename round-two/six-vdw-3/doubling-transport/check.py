#!/usr/bin/env python3
"""Separate complete definition audit; midpoint clauses use literal triple subsets."""
import argparse,hashlib,importlib.util,itertools,json,math
from pathlib import Path
COUNTER_SHA='dfca6ef3ae727a669f5318406e4e33ab2c7fcb3436ec3cc5b0a5f9c0b0307a34'

def need(ok,message):
 if not ok:raise ValueError(message)

def helper(path):
 need(hashlib.sha256(path.read_bytes()).hexdigest()==COUNTER_SHA,'Changed pinned helper')
 spec=importlib.util.spec_from_file_location('independent_truth_counter',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def audit(text,q,case,L,c):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime audit domain')
 need(case!='four' or 3<L<q,'Interior cap audit domain')
 n,actual=c.parse(text);expected=set();base=q*(q-1)//2
 for x in range(1,q):
  for y in range(x+1,q):
   z=c.label(q,x,y);expected.update(((x,y,-z),(x,-y,z),(-x,y,z),(-x,-y,-z)))
 xor=len(expected);ladders=set()
 for a in range(q):
  for r in range(1,q):
   row=tuple(sorted(c.label(q,(a+j*r)%q,(a+(j+3)*r)%q) for j in range(4)))
   need(len(set(row))==4,'Repeated ladder edge');ladders.add(row);expected.update((row,tuple(-v for v in row)))
 criterion=len(expected);expected.update(((-1,),(-2,)));extras=set();counter_count=0
 if case=='four':
  cells,extra=c.counter_clauses([-i for i in range(1,q)],L-1,base)
  extra.remove((cells[q-1,L-1],));expected.update(extra);expected.add((-3,));counter_count=len(cells)
 else:
  need(case=='no-four','Unknown audit branch')
  # All ordered actual first/second field points, with no reversal quotient.
  for first in range(q):
   for second in range(q):
    if first==second:continue
    row=tuple(sorted(v for j in range(4) if (v:=(first+j*(second-first))%q)!=0))
    need(len(row) in (3,4),'Repeated four-AP point');extras.add(row)
  half=pow(2,-1,q);triple_supports=0;midpoint_clauses=set()
  # Every three-element subset, deciding the middle by 2*b=a+c.
  # This is independent of the generator's (start,step) loops.
  for triple in itertools.combinations(range(q),3):
   centers=[b for b in triple if 2*b%q==(sum(triple)-b)%q]
   if not centers:continue
   need(len(centers)==1,'Nonunique triple midpoint');triple_supports+=1;b=centers[0];a,z=[v for v in triple if v!=b]
   interior=((a+b)*half%q,(b+z)*half%q)
   if 0 in interior:continue  # Negative origin literal is true.
   row=tuple(sorted([v for v in triple if v]+[-v for v in interior],key=abs))
   need(len(set(map(abs,row)))==len(row),'Repeated/tautological midpoint point');midpoint_clauses.add(row)
  extras.update(midpoint_clauses);expected.update(extras)
 need(n==base+counter_count and actual==expected,'Complete variable/clause definition coverage differs')
 result={'q':q,'case':case,'weight_cap':L if case=='four' else None,'variables':n,'clauses':len(actual),
         'directed_ladders':q*(q-1),'distinct_ladders':len(ladders),'xor_clauses':xor,'criterion_clauses':criterion,
         'counter_variables':counter_count,'cnf_sha256':hashlib.sha256(text.encode()).hexdigest()}
 if case=='no-four':result.update({'three_AP_supports':triple_supports,'midpoint_clauses':len(midpoint_clauses),'additional_word_clauses':len(extras)})
 return result

def full(u):
 q=len(u);return all(len({u[(a+j*r)%q]^u[(a+(j+3)*r)%q] for j in range(4)})==2 for a in range(q) for r in range(1,q))

def no_four(u):
 q=len(u);return all(any(u[(a+j*r)%q] for j in range(4)) for a in range(q) for r in range(1,q))

def values(u,case,L,c):
 q=len(u);v={c.label(q,x,y):bool(u[x]^u[y]) for x in range(q) for y in range(x+1,q)}
 if case=='four':
  for (i,k),label in c.counter_cells(q-1,L-1,q*(q-1)//2).items():v[label]=u[1:i+1].count(0)>=k
 return v

def small(text,q,case,L,c):
 audit(text,q,case,L,c);_,clauses=c.parse(text);accepted=0;normalizations=0;valid=0;APs=0
 for tail in itertools.product((0,1),repeat=q-1):
  u=(0,)+tail;F=full(u);valid+=F
  expected=F and u[1]==u[2]==0 and (u[3]==0 and u.count(0)<=L if case=='four' else no_four(u))
  need(c.satisfied(clauses,values(u,case,L,c))==expected,'Complete small literal branch semantics differ');accepted+=expected
  if expected:
   word=[u[t%q]^int(t%6>=3) for t in range(6*q)]
   for first in range(6*q):
    for step in range(1,6*q):
     need(len({word[(first+j*step)%(6*q)] for j in range(7)})==2,'Literal cyclic positive control failed');APs+=1
  if F:
   for color in (0,1):
    if case=='four' and u.count(color)>L:continue
    if case=='no-four' and not no_four(tuple(b^color for b in u)):continue
    length=4 if case=='four' else 3
    for a in range(q):
     for r in range(1,q):
      if not all(u[(a+j*r)%q]==color for j in range(length)):continue
      U=tuple(u[(a+r*x)%q]^color for x in range(q))
      need(U.count(0)==u.count(color) and c.satisfied(clauses,values(U,case,L,c)),'Affine/color branch normalization lost a case');normalizations+=1
 return {'q':q,'case':case,'weight_cap':L if case=='four' else None,'normalized_words':1<<(q-1),'full_words':valid,'accepted':accepted,'all_eligible_normalizations':normalizations,'literal_positive_cyclic_APs':APs}

def controls(text,q,case,L,c):
 n,clauses=c.parse(text)
 wrong=clauses|{(3,)} if case=='four' else clauses|{(-3,)}
 mutations=[clauses-{min(clauses)},wrong]
 if case=='four':
  upper=c.counter_cells(q-1,L-1,q*(q-1)//2)[q-1,L]
  mutations.append((clauses-{(-upper,)})|{(upper,)})
 else:
  row=next(row for row in clauses if len(row)==5 and sum(v<0 for v in row)==2 and all(abs(v)<q for v in row))
  mutations.append(clauses-{row})
 damaged=[f'p cnf {n} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(rows)) for rows in mutations]
 damaged.append(text.replace(f'p cnf {n} ',f'p cnf {n+1} ',1))
 for body in damaged:
  try:audit(body,q,case,L,c)
  except ValueError:pass
  else:raise ValueError('Corrupted model accepted')
 return len(damaged)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('cnf',type=Path);p.add_argument('--q',type=int,default=103);p.add_argument('--case',choices=('four','no-four'),required=True);p.add_argument('--limit',type=int,default=27);p.add_argument('--counter-source',type=Path,required=True);p.add_argument('--small',action='store_true');p.add_argument('--controls',action='store_true');a=p.parse_args();c=helper(a.counter_source);text=a.cnf.read_text()
 need(not a.small or a.q in (7,11,13),'Bound complete Boolean controls to7/11/13')
 result=small(text,a.q,a.case,a.limit,c) if a.small else audit(text,a.q,a.case,a.limit,c)
 if a.controls:result['model_corruptions_rejected']=controls(text,a.q,a.case,a.limit,c)
 print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
