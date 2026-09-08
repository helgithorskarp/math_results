import copy,itertools,json,pathlib
import verify as v

def main():
 cert=json.loads((pathlib.Path(__file__).resolve().parent/'certificate.json').read_text());bad=[]
 def reject(name,change):
  c=copy.deepcopy(cert);change(c)
  try:v.validate(c)
  except (ValueError,KeyError,TypeError):bad.append(name);return
  raise RuntimeError('control accepted: '+name)
 reject('missing_rotation_orbit',lambda c:c['cases'].pop())
 reject('duplicate_rotation_orbit',lambda c:c['cases'][1].update(angle=c['cases'][0]['angle']))
 reject('nonunit_rotation',lambda c:c['cases'][0]['angle'].__setitem__(5,2))
 reject('noncanonical_rational_field',lambda c:c['cases'][0]['angle'].__setitem__(2,1))
 reject('improper_edge_word',lambda c:c['cases'][0].update(colours=c['cases'][0]['colours'][1]+c['cases'][0]['colours'][1:]))
 def collision(c):
  w=list(c['cases'][0]['colours']);w[20]=str((int(w[0])+1)%3);c['cases'][0]['colours']=''.join(w)
 reject('inconsistent_coincident_labels',collision)
 reject('false_four_chromatic_claim',lambda c:c['cases'][0].update(chi=4))
 reject('wrong_physical_order',lambda c:c['cases'][0].update(vertices=62))
 reject('wrong_family',lambda c:c.update(family='H3+uH3'))
 # Independent small combinatorial fixture: every proper colouring of K3 square K3.
 es=[(3*a+b,3*c+d) for a,b in itertools.product(range(3),repeat=2) for c,d in itertools.product(range(3),repeat=2) if 3*a+b<3*c+d and ((a==c) != (b==d))]
 proper={w for w in itertools.product(range(3),repeat=9) if all(w[a]!=w[b] for a,b in es)}
 predicted={tuple(p[(a+sign*b)%3] for a,b in itertools.product(range(3),repeat=2)) for p in itertools.permutations(range(3)) for sign in (-1,1)}
 v.require(proper==predicted and len(proper)==12,'Cartesian three-pattern fixture')
 # A genuine generic physical placement u=i, in Q(sqrt(3))^2.
 h=v.patch();ps=[(2*a+b,-d,2*c+d,b) for a,b in h for c,d in h];word=[(a-b+c-d)%3 for a,b in h for c,d in h];edges=0
 v.require(len(set(ps))==361,'generic distinctness')
 for i,p in enumerate(ps):
  for j,q in enumerate(ps[:i]):
   A,B,C,D=[x-y for x,y in zip(p,q)]
   if A*A+3*B*B+C*C+3*D*D==4 and A*B+C*D==0:
    edges+=1;v.require(word[i]!=word[j],'generic proper three-colouring')
 v.require(edges==1596,'generic Cartesian edge census')
 print(json.dumps({'rejected_controls':bad,'K3_square_K3_three_colourings':len(proper),'generic_u_i_vertices':361,'generic_u_i_edges':edges,'generic_u_i_checked_pairs':64980},sort_keys=True,indent=2))
if __name__=='__main__':main()
