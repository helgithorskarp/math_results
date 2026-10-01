#!/usr/bin/env python3
"""Independent definition audit for the seeded field and mixed-cover models."""
import argparse,hashlib,importlib.util,itertools,json,math
from pathlib import Path
COUNTER_SHA='dfca6ef3ae727a669f5318406e4e33ab2c7fcb3436ec3cc5b0a5f9c0b0307a34'

def need(ok,message):
 if not ok:raise ValueError(message)

def load_counter(path):
 need(hashlib.sha256(path.read_bytes()).hexdigest()==COUNTER_SHA,'Pinned independent counter auditor differs')
 s=importlib.util.spec_from_file_location('independent_counter',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def field_audit(text,q,L,c):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)) and 2<L<q,'Prime/interior-cap domain')
 n,actual=c.parse(text);expected=set()
 for x in range(1,q):
  for y in range(x+1,q):
   z=c.label(q,x,y);expected.update(((x,y,-z),(x,-y,z),(-x,y,z),(-x,-y,-z)))
 xor_count=len(expected);ladders=set()
 for a in range(q):
  for r in range(1,q):
   row=tuple(sorted(c.label(q,(a+j*r)%q,(a+(j+3)*r)%q) for j in range(4)))
   need(len(set(row))==4,'Repeated ladder edge');ladders.add(row);expected.update((row,tuple(-v for v in row)))
 base=q*(q-1)//2;cells,extra=c.counter_clauses([-i for i in range(1,q)],L-1,base)
 extra.remove((cells[q-1,L-1],));expected.update(extra);expected.update(((-1,),(-2,)))
 need(actual==expected and n==base+len(cells),'Full mathematical clause/variable coverage differs')
 return {'q':q,'minority_weight_cap':L,'counted_color':0,'count_target_cap':L-1,'variables':n,'clauses':len(actual),
         'directed_ladders':q*(q-1),'distinct_ladders':len(ladders),'xor_clauses':xor_count,
         'counter_variables':len(cells),'model_sha256':hashlib.sha256(text.encode()).hexdigest()}

def mixed_audit(text,n,c):
 need(n>=7,'Mixed domain');variables,actual=c.parse(text);expected=set();counts={3:set(),7:set()}
 # All ordered choices of the actual first two points, both directions.
 # This does not reuse the encoder's bounded positive-step loops.
 for a in range(1,n+1):
  for b in range(1,n+1):
   if a==b:continue
   for k in (3,7):
    positions=[a+j*(b-a) for j in range(k)]
    if all(1<=v<=n for v in positions):
     row=tuple(sorted(((-v if k==3 else v) for v in positions),key=abs));expected.add(row);counts[k].add(row)
 need(actual==expected and variables==n,'Mixed-cover definition coverage differs')
 return {'n':n,'variables':n,'clauses':len(actual),'three_APs':len(counts[3]),'seven_APs':len(counts[7]),
         'model_sha256':hashlib.sha256(text.encode()).hexdigest()}

def field_valid(u):
 q=len(u)
 return all(len({u[(a+j*r)%q]^u[(a+(j+3)*r)%q] for j in range(4)})==2 for a in range(q) for r in range(1,q))

def field_values(u,L,c):
 q=len(u);v={c.label(q,x,y):bool(u[x]^u[y]) for x in range(q) for y in range(x+1,q)}
 for (i,k),label in c.counter_cells(q-1,L-1,q*(q-1)//2).items():v[label]=sum(x==0 for x in u[1:i+1])>=k
 return v

def small_field(text,q,L,c):
 field_audit(text,q,L,c);_,clauses=c.parse(text);accepted=normalizations=APs=valid_words=0
 for tail in itertools.product((0,1),repeat=q-1):
  u=(0,)+tail;valid=field_valid(u);valid_words+=valid
  expected=valid and u[1]==u[2]==0 and u.count(0)<=L
  need(c.satisfied(clauses,field_values(u,L,c))==expected,'Complete small seeded model differs')
  if valid:
   for color in (0,1):
    if u.count(color)>L:continue
    for a in range(q):
     for r in range(1,q):
      if not all(u[(a+j*r)%q]==color for j in range(3)):continue
      U=tuple(u[(a+r*x)%q]^color for x in range(q))
      need(U.count(0)==u.count(color) and c.satisfied(clauses,field_values(U,L,c)),'Colored three-AP normalization lost a case');normalizations+=1
  if expected:
   accepted+=1;word=[u[t%q]^int(t%6>=3) for t in range(6*q)]
   for a in range(6*q):
    for d in range(1,6*q):
     need(len({word[(a+j*d)%(6*q)] for j in range(7)})==2,'Actual cyclic positive control failed');APs+=1
 return {'q':q,'minority_weight_cap':L,'normalized_words':1<<(q-1),'full_family_words':valid_words,
         'accepted_seeded_words':accepted,'colored_three_AP_normalizations':normalizations,'literal_positive_cyclic_APs':APs}

def mixed_valid(bits):
 n=len(bits)
 for a in range(n):
  for b in range(n):
   if a==b:continue
   for k,color in ((3,1),(7,0)):
    pos=[a+j*(b-a) for j in range(k)]
    if all(0<=x<n for x in pos) and all(bits[x]==color for x in pos):return False
 return True

def small_mixed(text,n,c):
 mixed_audit(text,n,c);_,clauses=c.parse(text);accepted=0
 for bits in itertools.product((0,1),repeat=n):
  valid=mixed_valid(bits);need(c.satisfied(clauses,{i+1:bool(b) for i,b in enumerate(bits)})==valid,'Mixed Boolean relation differs');accepted+=valid
 return {'n':n,'assignments':1<<n,'accepted':accepted}

def controls(text,q,L,c):
 n,rows=c.parse(text);cells=c.counter_cells(q-1,L-1,q*(q-1)//2);upper=cells[q-1,L]
 mutations=[rows-{min(rows)},rows|{(1,)},(rows-{(-upper,)})|{(upper,)}]
 damaged=[f'p cnf {n} {len(r)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(r)) for r in mutations]
 damaged.append(text.replace(f'p cnf {n} ',f'p cnf {n+1} ',1))
 for bad in damaged:
  try:field_audit(bad,q,L,c)
  except ValueError:pass
  else:raise ValueError('Corrupted seeded model was accepted')
 return len(damaged)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('model',type=Path);p.add_argument('--q',type=int,default=103);p.add_argument('--limit',type=int);p.add_argument('--mixed-n',type=int);p.add_argument('--counter-source',type=Path,required=True);p.add_argument('--small',action='store_true');p.add_argument('--controls',action='store_true');a=p.parse_args()
 need((a.limit is None)!=(a.mixed_n is None),'Choose one model kind');c=load_counter(a.counter_source);text=a.model.read_text()
 if a.mixed_n is not None:
  need(not a.small or a.mixed_n==9,'Bound complete mixed controls to9')
  result=small_mixed(text,a.mixed_n,c) if a.small else mixed_audit(text,a.mixed_n,c)
 else:
  need(not a.small or a.q in (7,13),'Bound complete seeded controls to7/13')
  result=small_field(text,a.q,a.limit,c) if a.small else field_audit(text,a.q,a.limit,c)
  if a.controls:result['model_corruptions_rejected']=controls(text,a.q,a.limit,c)
 print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
