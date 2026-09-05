#!/usr/bin/env python3
"""Solver-free finite checks for the interface QBF reduction and controls."""
from hashlib import sha256
import json
from pathlib import Path
import controls
import encode
import verify_controls as audit

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def compute():
    checks=[audit.inspect(case) for case in controls.controls()]
    source,U=encode.pool_input()
    raw,meta=encode.encode(**source,budget=134)
    table=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    leak=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/s_vertex_leaks.json').read_text())['leaks']['397'][0]
    p=leak['class_index']
    indices=[i for i,v in enumerate(U) if v<509 and v!=397]
    H=encode.restrict(source,indices)
    c=leak['witness_colouring_S_minus_v']
    encode.require(len(c)==134 and set(c)<=set('0123'),'leak format')
    colors=list(map(int,c))
    encode.require(all(colors[a]!=colors[b] for a,b in H['edges']),'S-minus-397 colouring')
    encode.require(all(colors[v]!=H['patterns'][p][a] for a,v in H['cross']),'leak interface')
    # All L colours were checked by pool_input; this is a whole 508-point colouring.
    child,child_meta=encode.encode(**H,budget=134,fixed=set(range(134)))
    prefix,rows=audit.parse(child)
    universal=next(vs for q,vs in prefix if q=='a')
    encoded_colors=sum(col<<(5+2*i) for i,col in enumerate(colors)) | p
    assumptions=list(range(1,135))+[v if (encoded_colors>>j)&1 else -v for j,v in enumerate(universal)]
    encode.require(not audit.sat(rows,assumptions),'proper colouring must refute fixed-selection QBF')
    compact_meta={k:v for k,v in meta.items() if k not in ['pattern_variables','color_variables']}
    return dict(status='QUANTIFIED SELECTOR FINITE CHECKS VERIFIED',
                abstract_cases=len(checks),matrix_assignments_checked=sum(r['matrix_assignments_checked'] for r in checks),
                abstract_controls=checks,full_instance=compact_meta,
                geometric_vertices=677,geometric_unit_edges=3400,interface_vertices=len(table['interface_L']),
                exact_L_witnesses_checked=20,
                fixed_508_control=dict(deleted_vertex=397,class_index=p,vertices=508,
                    unit_edges=1860+len(H['edges'])+len(H['cross']),qdimacs_sha256=sha256(child).hexdigest(),
                    proper_colouring_checked=True,universal_counterexample_refutes_matrix=True))


def main():
    result=compute()
    expected=json.loads((HERE/'expected.json').read_text())
    encode.require(result==expected,'recorded results differ')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
