#!/usr/bin/env python3
"""Definition audit for no-three-periodic-seven-AP word weight fibers."""
import argparse,hashlib,importlib.util,itertools,json,math
from pathlib import Path
COUNTER_AUDIT_SHA='dfca6ef3ae727a669f5318406e4e33ab2c7fcb3436ec3cc5b0a5f9c0b0307a34'

def need(ok,message):
 if not ok:raise ValueError(message)

def load_counter(path):
 need(hashlib.sha256(path.read_bytes()).hexdigest()==COUNTER_AUDIT_SHA,'Pinned independent counter auditor differs')
 spec=importlib.util.spec_from_file_location('independent_counter_audit',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def audit(text,q,limit,counter,encoding='cut'):
 need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)) and 0<limit<q-1,'Domain requires prime q and interior cap')
 need(encoding in ('cut','word'),'Unsupported encoding')
 variables,actual=counter.parse(text);expected=set();label=lambda x,y:counter.label(q,x,y)
 xor_count=0;ladders=set()
 if encoding=='cut':
  for x in range(1,q):
   for y in range(x+1,q):
    a,b,z=x,y,label(x,y)
    expected.update(((a,b,-z),(a,-b,z),(-a,b,z),(-a,-b,-z)))
  xor_count=len(expected)
  # Full directed domain. Only OR-of-differences; all-one is permitted.
  for a in range(q):
   for r in range(1,q):
    edges=tuple(sorted(label((a+j*r)%q,(a+(j+3)*r)%q) for j in range(4)))
    need(len(set(edges))==4,'Repeated edge')
    ladders.add(edges);expected.add(edges)
  base=q*(q-1)//2
 else:
  # Derive the forbidden relation from all128 bit strings, independently
  # of the encoder's three-bit-prefix construction and reversal cover.
  forbidden=[b for b in itertools.product((0,1),repeat=7) if all(b[j]==b[j+3] for j in range(4))]
  need(len(forbidden)==8,'Wrong three-periodic truth relation')
  for a in range(q):
   for r in range(1,q):
    positions=tuple((a+j*r)%q for j in range(7))
    need(len(set(positions))==7,'Repeated progression point')
    for bits in forbidden:
     if any(v==0 and bit for v,bit in zip(positions,bits)):continue
     expected.add(tuple(sorted(((-v if bit else v) for v,bit in zip(positions,bits) if v),key=abs)))
  base=q-1
 criterion_count=len(expected);cells,clauses=counter.counter_clauses(list(range(1,q)),limit,base)
 # Keep only the upper threshold unit: count <=limit, not exact count.
 clauses.remove((cells[q-1,limit],));expected.update(clauses);expected.add((1,))
 need(actual==expected,'Full definition-level model coverage differs')
 need(variables==base+len(cells),'Variable coverage differs')
 return {'encoding':encoding,'q':q,'weight_limit':limit,'variables':variables,'clauses':len(actual),'base_variables':base,
         'xor_clauses':xor_count,'unoriented_ladders':len(ladders),'directed_ladders':q*(q-1),
         'criterion_clauses':criterion_count,
         'counter_variables':len(cells),'model_sha256':hashlib.sha256(text.encode()).hexdigest()}

def criterion(u):
 q=len(u)
 return all(any(u[(a+j*r)%q]!=u[(a+(j+3)*r)%q] for j in range(4))
            for a in range(q) for r in range(1,q))

def assign(u,limit,counter,encoding='cut'):
 q=len(u)
 values=({counter.label(q,x,y):bool(u[x]^u[y]) for x in range(q) for y in range(x+1,q)}
         if encoding=='cut' else {x:bool(u[x]) for x in range(1,q)})
 base=q*(q-1)//2 if encoding=='cut' else q-1
 cells=counter.counter_cells(q-1,limit,base)
 for (i,k),v in cells.items():values[v]=sum(u[1:i+1])>=k
 return values

def small(text,q,limit,counter,encoding='cut'):
 audit(text,q,limit,counter,encoding);_,clauses=counter.parse(text)
 accepted=good=normalized=actual_APs=0
 for tail in itertools.product((0,1),repeat=q-1):
  u=(0,)+tail;valid=criterion(u);good+=valid
  expected=valid and sum(u)<=limit and u[1]==1
  need(counter.satisfied(clauses,assign(u,limit,counter,encoding))==expected,'Small exact Boolean model differs')
  if valid and sum(u)<=limit:
   p=u.index(0);z=u.index(1)
   U=tuple(u[(p+(z-p)*x)%q] for x in range(q))
   need(sum(U)==sum(u) and U[0]==0 and U[1]==1,'Affine normalization changed weight or anchors')
   need(counter.satisfied(clauses,assign(U,limit,counter,encoding)),'Affine normalization lost a valid low-weight word')
   normalized+=1
  if expected:
   accepted+=1;word=[u[x%q]^int(x%3==2) for x in range(3*q)]
   for a in range(3*q):
    for d in range(1,3*q):
     need(len({word[(a+j*d)%(3*q)] for j in range(7)})==2,'Positive three-factor product has an actual cyclic AP')
     actual_APs+=1
 return {'encoding':encoding,'q':q,'weight_limit':limit,'normalized_words':1<<(q-1),'criterion_valid_words':good,
         'accepted_fiber_words':accepted,'affine_low_weight_cases':normalized,'literal_positive_cyclic_APs':actual_APs}

def controls(text,q,limit,counter,encoding):
 n,rows=counter.parse(text);base=q*(q-1)//2 if encoding=='cut' else q-1
 cells=counter.counter_cells(q-1,limit,base);upper=cells[q-1,limit+1]
 mutations=[rows-{min(rows)},rows|{(-1,)},(rows-{(-upper,)})|{(upper,)}]
 damaged=[f'p cnf {n} {len(r)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in sorted(r)) for r in mutations]
 damaged.append(text.replace(f'p cnf {n} ',f'p cnf {n+1} ',1))
 for bad in damaged:
  try:audit(bad,q,limit,counter,encoding)
  except ValueError:pass
  else:raise ValueError('Corrupted model was accepted')
 return len(damaged)

def counter_controls(counter):
 cases=0
 for n in range(2,9):
  for cap in range(1,n):
   for sign in (-1,1):
    cells,clauses=counter.counter_clauses([sign*(i+1) for i in range(n)],cap,n)
    clauses.remove((cells[n,cap],))
    for bits in itertools.product((False,True),repeat=n):
     values={i+1:bit for i,bit in enumerate(bits)};counted=[bit if sign==1 else not bit for bit in bits]
     for (i,k),v in cells.items():values[v]=sum(counted[:i])>=k
     need(counter.satisfied(clauses,values)==(sum(counted)<=cap),'At-most counter truth mismatch');cases+=1
 return cases

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('model',type=Path);p.add_argument('--q',type=int,default=103);p.add_argument('--encoding',choices=['cut','word'],default='cut');p.add_argument('--limit',type=int,required=True);p.add_argument('--counter-source',type=Path,required=True);p.add_argument('--small',action='store_true');p.add_argument('--controls',action='store_true');a=p.parse_args()
 c=load_counter(a.counter_source);need(a.q>=7 and 0<a.limit<a.q-1,'Parameter range')
 need(not a.small or a.q in (7,13),'Complete small controls are bounded to7/13')
 text=a.model.read_text();out=small(text,a.q,a.limit,c,a.encoding) if a.small else audit(text,a.q,a.limit,c,a.encoding)
 if a.controls:out.update(model_corruptions_rejected=controls(text,a.q,a.limit,c,a.encoding),small_counter_truth_cases=counter_controls(c))
 print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
