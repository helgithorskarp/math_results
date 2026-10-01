#!/usr/bin/env python3
"""Exact controls for the five triplet extensions and moment inequalities."""
import itertools,json

def need(ok,message):
 if not ok:raise ValueError(message)

def full_window(bits):return len({bits[j]^bits[j+3] for j in range(4)})==2

def main():
 # Multiply normalized coordinates by6. The17 integers are distinct for
 # any prime q>=53, and encode every rational-coordinate extension.
 windows=[tuple(range(0,13,2)),tuple(range(-3,16,3)),tuple(range(-18,19,6)),
          tuple(range(-12,25,6)),tuple(range(-6,31,6))]
 positions=sorted(set().union(*map(set,windows)));seeds={0,6,12};free=sorted(set(positions)-seeds)
 need(len(positions)==17 and len(free)==14,'Triplet coordinate union differs')
 local=valid=six=seven=0
 groups=[{2,4,8,10},{-3,3,9,15},{-18,-12,-6,18},{-12,-6,18,24},{-6,18,24,30}]
 for tail in itertools.product((0,1),repeat=14):
  assignment={v:1 for v in seeds};assignment.update(zip(free,tail));local+=1
  if not all(full_window(tuple(assignment[v] for v in row)) for row in windows):continue
  valid+=1
  need(all(any(assignment[v] for v in group) for group in groups),'A local extension implication failed')
  adjacent=bool(assignment[-6] or assignment[18])
  outer=(assignment[-18] and assignment[24]) or (assignment[-12] and assignment[24]) or (assignment[-12] and assignment[30])
  need(adjacent or outer,'Three-window outer cover failed')
  size=sum(assignment.values());need(size>=6 if adjacent else size>=7,'Disjoint cluster lower bound failed')
  six+=size==6;seven+=size==7
 identities=full_cases=ternary_cases=0
 for q in (11,13):
  half=pow(2,-1,q);third=pow(3,-1,q)
  patterns={'P':(0,1,2),'E':(0,1,2,3),'F34':(-3,0,1,2,4),'F25':(-2,0,1,2,5),'F24':(-2,0,1,2,4),'R':(-2,0,3,5),
            'A':(0,1,3),'B':(0,1,4),
            'Q13':(0,1,2,third),'Q23':(0,1,2,2*third),'Q43':(0,1,2,4*third),'Q53':(0,1,2,5*third),
            'Qm12':(0,1,2,-half),'Q12':(0,1,2,half),'Q32':(0,1,2,3*half),'Q52':(0,1,2,5*half)}
  masks={key:[sum(1<<((a+t*r)%q) for t in pattern) for a in range(q) for r in range(1,q)] for key,pattern in patterns.items()}
  need(all(mask.bit_count()==len(patterns[key]) for key,rows in masks.items() for mask in rows),'Repeated pattern point')
  ladders=[tuple(((a+j*r)%q,(a+(j+3)*r)%q) for j in range(4)) for a in range(q) for r in range(1,q)]
  for w in range(1<<(q-1)):
   word=w<<1;counts={key:sum(word&mask==mask for mask in rows) for key,rows in masks.items()};identities+=1
   need(counts['F34']==counts['F25'] and counts['Q13']==counts['Q53'] and counts['Q23']==counts['Q43']
        and counts['Qm12']==counts['Q52'] and counts['Q12']==counts['Q32'],'Reflection identity failed')
   mass=word.bit_count();maskq=(1<<q)-1
   intersections=[(word&(((word<<h)|(word>>(q-h)))&maskq)).bit_count() for h in range(1,q)]
   D=sum(i>0 for i in intersections)
   need(sum(intersections)==mass*(mass-1),'Difference-mass identity failed')
   need(counts['R']<=mass*(mass-1)-D,'Proper-set cyclic overlap bound failed')
   ternary_valid=all(any(((word>>x)^(word>>y))&1 for x,y in row) for row in ladders)
   if ternary_valid:
    ternary_cases+=1;need(2*(counts['A']+counts['B'])>=D,'Triple-only difference-support inequality failed')
   valid_word=all(len({((word>>x)^(word>>y))&1 for x,y in row})==2 for row in ladders)
   if valid_word:
    full_cases+=1;P=counts['P']
    need(P<=2*counts['E']+2*counts['F34']+counts['F24'],'Outer moment inequality failed')
    need(P<=2*(counts['Q13']+counts['Q23']),'Third-fraction moment inequality failed')
    need(P<=2*(counts['Qm12']+counts['Q12']),'Half-fraction moment inequality failed')
 print(json.dumps({'status':'TRIPLET_EXTENSION_CLUSTER_AND_MOMENTS_CHECKED','local_assignments':local,
                   'five_window_valid_assignments':valid,'valid_six_point_clusters':six,'valid_seven_point_clusters':seven,
                   'complete_small_word_moment_identities':identities,'full_family_moment_cases':full_cases,
                   'ternary_difference_support_cases':ternary_cases},sort_keys=True))

if __name__=='__main__':main()
