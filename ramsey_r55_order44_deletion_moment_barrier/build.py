"""Generate both orders of the common-density deletion test, outside Git."""
from pathlib import Path
from math import comb, gcd
from functools import reduce
import json
import numpy as np
from graph_types import adj
from generate_base import build as base_build
from generate_integer import augment, poly_values
from generate_squares import build as square_build

def degree_identity(graphs, n=44):
    if n != 44:
        raise ValueError('The recorded degree-support identity is for order 44.')
    cs = poly_values(list(range(19,25)))
    row=[]
    for g in graphs:
        value=0
        for mask in (g, ((1<<21)-1)^g):
            for neighbours in adj(7,mask):
                d=neighbours.bit_count()
                value += sum(c*comb(d,s)*(60*comb(n-1,s)//comb(6,s))
                             for s,c in enumerate(cs))
        row.append(value)
    factor=reduce(gcd,row)
    return [v//factor for v in row], factor

def build_all(work):
    work=Path(work)
    models=[]
    for n in (43,44):
        A, graphs, labels, Q, base_meta = base_build(n=n,M=13,lo=n-25,hi=24)
        AA, QQ, polys = augment(graphs,n=n,lo=n-25,hi=24,M=13)
        scalar_bounds=[(840 if kind=='degree_indicator' else 420)*
                       sum(abs(c)*comb(n-(1 if kind=='degree_indicator' else 2),s)
                           for s,c in enumerate(cs)) for kind,label,cs in polys]
        if max(scalar_bounds)>=2**63:
            raise ArithmeticError('scalar generation exceeds the documented integer domain')
        Qs, square_meta = square_build(graphs,n=n)
        matrices=Q+QQ+Qs
        np.savez(work/f'model_{n}.npz',graphs=np.array(graphs),A=np.concatenate([A,AA]),
                 **{f'Q{i}':q for i,q in enumerate(matrices)})
        meta={'n':n,'degree_window':[n-25,24],'same_colour_codegree_cap':13,
              'base':base_meta,'scalar_labels':labels,'polynomials':polys,
              'matrix_dimensions':[q.shape[1] for q in matrices],'squares':square_meta}
        (work/f'model_{n}.json').write_text(json.dumps(meta,indent=2)+'\n')
        models.append(meta)
    row,factor=degree_identity(graphs)
    (work/'degree_identity.json').write_text(json.dumps(
        {'n':44,'graphs':graphs,'row':row,'divided_by':factor},indent=2)+'\n')
    return models
