"""Accept only a complete good43 SAT model satisfying the refined branch."""
from pathlib import Path
import argparse,json
import base,strengthen

def accept(branch,text,parent):
 if not strengthen.allowed(branch):raise ValueError('Refined branch required')
 graph=parent['decode'].decode(branch,text)
 matrix=parent['verify_target'].adjacency(graph);packing=parent['model'].Packing(branch)
 if strengthen.check_closure(matrix,packing) is not None:raise ValueError('SAT claim violates global greedy closure')
 return graph

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path);p.add_argument('--branch',required=True);p.add_argument('--solver-output',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Output exists')
 graph=accept(list(map(int,a.branch.split(','))),a.solver_output.read_text(),base.load(a.base));a.output.write_text(json.dumps(graph,indent=2,sort_keys=True)+'\n');print('VERIFIED_GOOD43_WITH_GLOBAL_GREEDY_CLOSURE')
