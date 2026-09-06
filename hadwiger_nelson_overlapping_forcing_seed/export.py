"""Export compact coordinates and checked upper-bound colouring witnesses."""
import json
from pathlib import Path
from itertools import combinations
from pysat.solvers import Glucose3
from lattice import edges
from graph import spindle
ROOT=Path(__file__).resolve().parent

def colour(n,es,k):
    s=Glucose3()
    for v in range(n):
        s.add_clause([k*v+c+1 for c in range(k)])
        for c,d in combinations(range(k),2):s.add_clause([-k*v-c-1,-k*v-d-1])
    for i,j in es:
        for c in range(k):s.add_clause([-k*i-c-1,-k*j-c-1])
    if not s.solve():raise ValueError('Upper-bound colouring not found')
    model=set(s.get_model());cs=[next(c for c in range(k) if k*v+c+1 in model) for v in range(n)]
    if any(cs[i]==cs[j] for i,j in es):raise ValueError('Invalid colouring')
    s.delete();return cs

def make(w):
    out={}
    for key,name,status in [('unequal','inequality_union_reduced','complete'),('equal','equality_frozen','frozen_for_target_gate')]:
        x=json.loads((w/(name+'.json')).read_text())
        if x['status']!=status:raise ValueError('Wrong discovery state')
        pts=x['points'];den=x['denominator'];es=edges(pts,den)
        out[key]={'points':pts,'denominator':den,'colouring':colour(len(pts),es,4),'retained_union_indices':x['retained']}
    labels,es,cross=spindle(out['equal']['points'],out['equal']['denominator'])
    if cross!=[[1,1]]:raise ValueError('Unexpected cross edge')
    n=len(out['equal']['points']);base=out['equal']['colouring']
    word=[base[i if i<n else i-n+1] for i in range(len(labels))];word[n]=4
    if any(word[a]==word[b] for a,b in es):raise ValueError('Spindle colouring failed')
    out['retained_spindle_indices']=list(range(len(labels)))
    out['g40_pair_indices']=json.loads((w/'g40_kernel.json').read_text())['pair_indices']
    out['five_colouring']=word
    return out
if __name__=='__main__':
    w=ROOT/'out';x=make(w)
    gate=json.loads((w/'gate_colourings.json').read_text())
    if gate['status']!='target_closed' or len(gate['colourings'])<253:raise ValueError('Target gate not closed')
    (w/'mandatory_vertices.json').write_text(json.dumps(gate['colourings'][:253],separators=(',',':'))+'\n')
    (w/'certificate.json').write_text(json.dumps(x,separators=(',',':'))+'\n')
    print(json.dumps({'unequal_vertices':len(x['unequal']['points']),'equal_vertices':len(x['equal']['points']),'final_vertices':len(x['retained_spindle_indices'])},sort_keys=True))
