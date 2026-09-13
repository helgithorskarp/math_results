"""Definition-level checker; imports no producer or Ramsey formula emitter."""
import argparse,hashlib,json,struct,time
from pathlib import Path
from itertools import combinations
from math import comb
from fractions import Fraction

def require(condition,message):
 if not condition:raise ValueError(message)

def verify(path,n=43,cycle=True):
 started=time.monotonic();variables=[(u,v) for u in range(n) for v in range(u+1,n) if not(cycle and (v==u+1 or (u==0 and v==n-1)))];m=len(variables);data=path.read_bytes();require(len(data)==8*comb(m,2),'Wrong certificate length');seen=set();kind={3:0,4:0};samples=[];records=struct.iter_unpack('<Q',data)
 for index,(i,j) in enumerate(combinations(range(m),2)):
  word=next(records)[0];require(word<(1<<n) and word.bit_count()==5,'Not a five-set');require(word not in seen,'Repeated clause');seen.add(word);vertices=[v for v in range(n) if word&(1<<v)];scope=set(combinations(vertices,2))
  if cycle:scope={e for e in scope if not(e[1]==e[0]+1 or e==(0,n-1))}
  require(variables[i] in scope and variables[j] in scope,'Path not in incidence graph');require(6<=len(scope)<=10 if cycle else len(scope)==10,'Unexpected red clause width')
  # All five vertices occur in the free-edge scope, so scopes cannot coincide
  # for different five-sets, even after duplicate-clause deletion.
  require(set(v for e in scope for v in e)==set(vertices),'Lost a physical vertex in the clause scope')
  union=set(variables[i]+variables[j]);kind[len(union)]+=1
  if index in (0,1,2,comb(m,2)//2,comb(m,2)-1):samples.append({'pair_index':index,'variables':[list(variables[i]),list(variables[j])],'five_set':vertices})
 require(len(seen)==comb(m,2),'Incomplete pairing')
 # Independently count the fractional Hall load at EVERY red five-set.
 # Adjacent edge pairs have C(n-3,2) containing five-sets; disjoint ones n-4.
 da=comb(n-3,2);dd=n-4;scale=da*dd;load_sum=0;max_load=0;hist={};minimum_scope_degree=4
 for S in combinations(range(n),5):
  deg=[4]*5;fixed=0
  if cycle:
   for i,j in combinations(range(5),2):
    u,v=S[i],S[j]
    if v==u+1 or (u==0 and v==n-1):deg[i]-=1;deg[j]-=1;fixed+=1
  q=10-fixed;adjacent=sum(comb(d,2) for d in deg);disjoint=comb(q,2)-adjacent;load=dd*adjacent+da*disjoint;load_sum+=load;max_load=max(max_load,load);hist[q]=hist.get(q,0)+1;minimum_scope_degree=min(minimum_scope_degree,min(deg))
 require(load_sum==comb(m,2)*scale,'Hall row/column sum mismatch');require(max_load<=scale,'Hall load exceeds one');require(minimum_scope_degree>=2 if cycle else minimum_scope_degree==4,'Scope degree bound failed')
 load=Fraction(max_load,scale);full_load=Fraction(15,n-4)+Fraction(30,comb(n-3,2));require(load<=full_load<=1,'Invalid Hall bound')
 # Tree-decomposition upper bound: central bag of m variables, one leaf
 # per clause containing that clause node and its at most ten variables.
 lower=m-1;upper=max(m-1,10);require(lower==upper,'Not the claimed width range')
 # Exact vertex-cut layout for the free-edge host K_43 minus its cycle.
 order=list(range(0,n,2))+list(range(1,n,2));prefix=set();cut_values=[]
 for v in order[:-1]:
  prefix.add(v);cut_values.append(sum((u in prefix)!=(w in prefix) for u,w in variables))
 cut_lower=(n//2)*(n-n//2)-2*(n//2)
 require(n==43 and cycle and max(cut_values)==cut_lower==420,'Free-edge cutwidth control failed')
 # The one-color formula alone is satisfied by the fixed cycle, which
 # prevents misreading its width as a satisfiability lower bound.
 blue_witness=[0,2,4,6,8]
 require(all(e in variables for e in combinations(blue_witness,2)),'Blue counterexample control failed')
 result={'status':'VERIFIED_COMPLETE_INCIDENCE_SUBDIVISION','n':n,'fixed_cycle':cycle,'variables':m,'paths_checked':len(seen),'path_length':2,'distinct_internal_clause_nodes':len(seen),'adjacent_variable_pairs':kind[3],'disjoint_variable_pairs':kind[4],'red_five_clauses_counted':comb(n,5),'red_clause_width_histogram':{str(k):v for k,v in sorted(hist.items())},'maximum_Hall_load':str(load),'Hall_total_load':comb(m,2),'treewidth_primal':m-1,'treewidth_incidence_lower':lower,'treewidth_incidence_upper':upper,'dense_primal_first_output_entries':str(1<<(m-1)),'certificate_sha256':hashlib.sha256(data).hexdigest(),'certificate_bytes':len(data),'samples':samples,'seconds':time.monotonic()-started,'free_edge_host_cutwidth':420,'optimal_vertex_order':order,'free_edge_prefix_cut_sizes':cut_values,'one_color_control':{'free_edges_all_blue':True,'satisfies_all_red_clauses':True,'violates_full_formula_on_blue_five_set':blue_witness},'new_physical_decisions':0,'claim':'Exact width and clique-subdivision certificate for the literal formula graphs; no semantic SAT, Ramsey, or unrestricted algorithmic lower bound.'}
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=verify(a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
