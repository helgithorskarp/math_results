"""Exact guarded K5 decomposition for the fixed H92 physical geometry.

No solver. Large clause JSONL output belongs in a fresh directory outside Git.
Only the reviewed projection's physical geometry is imported, not arithmetic.
"""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

PARENT = Path(__file__).resolve().parent.parent/'ramsey_r55_antipodal_degree_projection'
PINS = {'model.py':'f93bc5bdb33f920f4c1483652c6fa8478da76464f57d97ece7898f4bdafb7afd',
        'flow.py':'fa9aa09354729c704a5065b8dd7cbefe50a620c048533f23632c0173f2e8dab0',
        'H92.json':'926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466'}


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path,data):
    with path.open('x') as f:
        json.dump(data,f,indent=2,sort_keys=True); f.write('\n')


def build():
    for name,digest in PINS.items():
        need(sha(PARENT/name) == digest,'input source '+name)
    sys.path.insert(0,str(PARENT)); from model import Model
    model = Model(); index = dict(model.index)
    index.update({e:524+i for i,e in enumerate(sorted(model.removed))})
    owner = {}; block_pairs = []
    for k,(L,R) in enumerate(model.blocks):
        pairs = [tuple(sorted((u,v))) for u in L for v in R]; block_pairs.append(pairs)
        for i,e in enumerate(pairs,1):
            owner[index[e]] = (k,i)
    rows = set(); candidates = Counter()
    for S in it.combinations(range(43),5):
        pairs = list(it.combinations(S,2))
        for color in (False,True):
            if any(e in model.fixed and model.fixed[e] != color for e in pairs):
                continue
            row = tuple(sorted((-1 if color else 1)*index[e] for e in pairs if e in index))
            need(row,'no all-fixed monochromatic K5'); rows.add(row)
            candidates['red' if color else 'blue'] += 1
    schema = {'format':'r55-antipodal-guarded-k5-v1','n':43,'visible_pairs':model.visible,
              'blocks':[{'left':L,'right':R,'pairs':pairs} for (L,R),pairs in zip(model.blocks,block_pairs)],
              'fixed_pairs':[[*e,int(c)] for e,c in sorted(model.fixed.items())],
              'degree_targets':[20 if v in (0,1,38) else 21 for v in range(43)],
              'density_equalities':model.densities,'residuals':model.residuals,
              'parent_pins':PINS,'warning':'All visible colors must be fixed before the conditional gluing oracle; this interface is not a SAT witness.'}
    encoded = []; counts = Counter(); residual_patterns = [set(),set(),set()]
    for row in sorted(rows,key=lambda c:(len(c),c)):
        guard = []; support = {}
        for literal in row:
            if abs(literal) not in owner:
                guard.append(literal)
            else:
                k,i = owner[abs(literal)]; support.setdefault(k,[]).append(i if literal > 0 else -i)
        support = [[k,sorted(xs)] for k,xs in sorted(support.items())]
        need(len(support) <= 2,'at most two lift blocks')
        shape = tuple(sorted(len(xs) for k,xs in support))
        need(shape in ((),(1,),(2,),(3,),(4,),(6,),(1,1),(1,2)),'complete support-shape bound')
        counts[','.join(map(str,shape)) if shape else 'visible-only'] += 1
        residual_patterns[len(support)].add(tuple((k,tuple(xs)) for k,xs in support))
        encoded.append([guard,support])
    report = {'format':schema['format'],'physical_clauses':len(rows),
              'candidate_five_sets':dict(candidates),'shape_counts':dict(sorted(counts.items())),
              'distinct_residual_patterns':[len(s) for s in residual_patterns],
              'visible_variables':523,'hidden_variables':104,'block_sizes':[[4,8],[4,9],[4,9]]}
    return schema,encoded,report


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    a = p.parse_args(); a.work.mkdir(exist_ok=False); schema,rows,report = build()
    dump(a.work/'schema.json',schema)
    with (a.work/'clauses.jsonl').open('x') as f:
        for row in rows:
            f.write(json.dumps(row,separators=(',',':'))+'\n')
    report.update(schema_sha256=sha(a.work/'schema.json'),clauses_sha256=sha(a.work/'clauses.jsonl'),
                  clauses_bytes=(a.work/'clauses.jsonl').stat().st_size)
    dump(a.work/'summary.json',report); print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
