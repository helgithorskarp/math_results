#!/usr/bin/env python3
"""Optional author-source bridge; separate from the independent checker."""
import argparse
import importlib.util
from pathlib import Path
import json
import audit as independent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author-dir',type=Path,required=True)
    p.add_argument('--check',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    spec=importlib.util.spec_from_file_location('pinned_author',args.author_dir/'verify.py')
    author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
    ours=independent.baseline()
    theirs=[author.cube(n) for n in range(1,5)]+[author.proper_cube(2),author.proper_cube(3),
            author.path3(),author.matching2(),author.uniform_rank2(4)]
    pairs=list(zip(ours,theirs))
    for n,r in [(2,2),(2,3),(2,4),(3,2),(3,3),(4,2),(4,3)]:
        pairs.append((independent.union([independent.cube(n)]*r),author.union_parts([author.cube(n)]*r)))
    for ix in [(2,8),(5,6),(1,7,1)]:
        pairs.append((independent.union([ours[i] for i in ix]),author.union_parts([theirs[i] for i in ix])))
    u2=independent.union([independent.cube(2)]*2);u3=independent.union([independent.cube(2)]*3)
    a2=author.union_parts([author.cube(2)]*2);a3=author.union_parts([author.cube(2)]*3)
    for o,a in [([u2,u2],[a2,a2]),([u2,u3],[a2,a3])]+[([independent.cube(c),u2],[author.cube(c),a2]) for c in (1,2,3)]:
        pairs.append((independent.tensor(o),author.tensor_parts(a)))
    for a,b in [(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,2),(5,4),(6,1)]:
        pairs.append((independent.unequal(a,b)[0],author.unequal_cubes(a,b)[0]))
    for c,a,b in [(1,3,1),(2,3,2)]:
        pairs.append((independent.tensor([independent.cube(c),independent.unequal(a,b)[0]]),
                      author.tensor_parts([author.cube(c),author.unequal_cubes(a,b)[0]])))
    fixture=json.loads((args.author_dir/'RESULTS.json').read_text())
    fixtures={r['label']:r for key in ('baselines','unions','products','unequal_cube_repairs') for r in fixture[key]}
    entries=0;labels=[]
    for ours,theirs in pairs:
        independent.need(ours[0]==theirs[0] and ours[2:]==theirs[2:], 'index/star/label mismatch')
        n=len(ours[0])
        for i in range(n):
            for j in range(n):
                independent.need(ours[1][i][j]==theirs[1][i][j], 'literal matrix mismatch')
                entries+=1
        observed=independent.check(*ours[:3]);expected=fixtures[ours[3]]
        independent.need(all(observed[k]==expected[k] for k in observed), 'fixture mismatch')
        labels.append(ours[3])
    result=dict(agent='six-reviewer-1',role='independent reviewer',matrices=len(pairs),
                entries_compared=entries,labels=labels,author_fixture_sha256=independent.sha256((args.author_dir/'RESULTS.json').read_bytes()).hexdigest())
    content=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:independent.need(args.check.read_text()==content,'bridge receipt bytes')
    if args.output:args.output.write_text(content)
    print(json.dumps(dict(ok=True,matrices=len(pairs),entries_compared=entries),sort_keys=True))


if __name__=='__main__':main()
