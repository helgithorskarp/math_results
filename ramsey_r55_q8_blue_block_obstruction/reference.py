"""Factorized grounding, independent of the generic forbidden-set encoder."""
from itertools import combinations,permutations
from collections import Counter

def decode(record):
 bits=''.join(format(ord(c)-63,'06b') for c in record[1:]);a=[set() for _ in range(11)];k=0
 for j in range(1,11):
  for i in range(j):
   if bits[k]=='1':a[i].add(j);a[j].add(i)
   k+=1
 return a

def formula(record):
 a=decode(record);rows=[];kinds=Counter()
 # A red K4 has exactly three old vertices and one new vertex.
 for old in combinations(range(11),3):
  if all(v in a[u] for u,v in combinations(old,2)):
   for new in range(4):rows.append(tuple(-(4*u+new+1) for u in old));kinds['red_3_plus_1']+=1
 # A blue K5 has two, three or four new vertices, because the old core is R44.
 for count in (2,3,4):
  for old in combinations(range(11),5-count):
   if any(v in a[u] for u,v in combinations(old,2)):continue
   for new in combinations(range(4),count):
    rows.append(tuple(4*u+w+1 for u in old for w in new));kinds[f'blue_{5-count}_plus_{count}']+=1
 return sorted(tuple(sorted(row)) for row in rows),dict(kinds)

def wagner_join(record):
 a=decode(record);core_edges={tuple(sorted((u,v))) for u in range(8) for v in a[u] if v<8}
 standard={tuple(sorted((i,(i+1)%8))) for i in range(8)}|{(i,i+4) for i in range(4)}
 for perm in permutations(range(8)):
  if {tuple(sorted((perm[u],perm[v]))) for u,v in standard}==core_edges:break
 else:raise ValueError('not the Wagner graph')
 if any(a[v]!=set(range(8)) for v in (8,9,10)):raise ValueError('not the independent-three join')
 return dict(wagner_to_core=list(perm),independent_three=[8,9,10],red_edges=sum(map(len,a))//2)
