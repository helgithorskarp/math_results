#!/usr/bin/env python3
"""Exact local and finite-field controls for the doubling transport proof."""
import itertools,json

def need(ok,message):
 if not ok:raise ValueError(message)

def F(bits):
 q=len(bits)
 return all(len({bits[(x+j*r)%q]^bits[(x+(j+3)*r)%q] for j in range(4)})==2 for x in range(q) for r in range(1,q))

def no_four(S,q):return all(not all((x+j*r)%q in S for j in range(4)) for x in range(q) for r in range(1,q))

def transport(S,q):
 half=pow(2,-1,q);counts={};triples=0
 for r in range(1,q):
  source={x for x in range(q) if all((x+j*r)%q in S for j in range(3))}
  target={x for x in range(q) if all((x+2*j*r)%q in S for j in range(3))}
  image={}
  for x in source:
   left=(x-2*r)%q in S;right=(x+4*r)%q in S
   need(left!=right,'Unique doubled extension failed')
   need((x+5*r)%q in S if left else (x-3*r)%q in S,'Companion outer extension failed')
   y=(x-2*r)%q if left else x
   need(y in target and y not in image,'Doubling map failed to be injective');image[y]=x
   need(((x+half*r)%q in S)!=((x+3*half*r)%q in S),'Unique internal midpoint failed');triples+=1
  need(set(image)==target,'Finite doubling transport failed surjectivity')
  counts[r]=len(source)
 need(all(counts[r]==counts[2*r%q]==counts[-r%q] for r in range(1,q)),'Step-orbit counts differ')
 return triples,counts

def main():
 local=valid=0;positions=list(range(-3,6));seed={0,1,2};free=[x for x in positions if x not in seed]
 for tail in itertools.product((0,1),repeat=6):
  v={x:1 for x in seed};v.update(zip(free,tail));local+=1
  if v[-1] or v[3] or(v[-2] and v[4]):continue
  windows=[tuple(v[a+j] for j in range(7)) for a in (-3,-2,-1)]
  if not all(len({row[j]^row[j+3] for j in range(4)})==2 for row in windows):continue
  valid+=1;need(v[-2]!=v[4],'Local unique extension failed');need(v[5] if v[-2] else v[-3],'Local companion extension failed')
 words=F_words=classes=nontrivial=triples=0
 for q in (7,11,13):
  for tail in itertools.product((0,1),repeat=q-1):
   u=(0,)+tail;words+=1
   if not F(u):continue
   F_words+=1
   for color in (0,1):
    S={x for x,b in enumerate(u) if b==color}
    if not no_four(S,q):continue
    classes+=1;tested,counts=transport(S,q);triples+=tested;nontrivial+=bool(tested)
 S={0,1,2,4};u=tuple(int(x not in S) for x in range(7))
 need(F(u) and no_four(S,7),'Nontrivial q7 literal fixture failed')
 tested,counts=transport(S,7);need(tested==6 and set(counts.values())=={1},'Positive q7 transport differs')
 powers=[];x=1
 while x not in powers:powers.append(x);x=2*x%103
 need(x==1 and len(powers)==51 and len(set(powers)|{-v%103 for v in powers})==102,'q103 signed doubling orbit differs')
 result={'status':'DOUBLING_INJECTION_BIJECTION_AND_MIDPOINT_CONTROLS_CHECKED','local_assignments':local,'valid_local_extensions':valid,
         'complete_small_words':words,'full_F_words':F_words,'no_four_color_classes':classes,
         'nontrivial_transport_classes':nontrivial,'directed_triplets_tested':triples,
         'positive_q7_fixture':{'S':[0,1,2,4],'triplets':tested,'per_direction':1},
         'q103_order_of_two':51,'q103_signed_step_orbit_size':102}
 print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
