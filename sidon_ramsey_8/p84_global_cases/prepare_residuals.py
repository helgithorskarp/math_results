"""Validate selected global anchor tuples and deduplicate their complements."""
import csv,hashlib,json
from pathlib import Path

def prepare(work,jobs):
    ordered=[list(map(int,l.split())) for l in (work/'orbit_catalog.txt').read_text().splitlines()]
    weights=list(map(int,(work/'weights.txt').read_text().split()))
    masks=[sum(1<<x for x in r) for r in ordered]
    counts=[int(r['count']) for r in csv.DictReader((work/'anchored.csv').open())]
    selected=set(map(int,(work/'selected_cases.txt').read_text().split()))
    assert selected=={j for j,c in enumerate(counts) if 0<c<=100}
    tuples=[tuple(map(int,l.split())) for l in (work/'selected_tuples.txt').read_text().splitlines()]
    assert len(tuples)==len(set(tuples))
    actual=[0]*len(counts);residuals={}
    threshold=sum(weights)-8000000
    for ids in tuples:
        assert len(ids)==4 and list(ids)==sorted(set(ids)) and ids[0]%2==0 and ids[0]//2 in selected
        used=0
        for i in ids:
            assert 0<=i<len(masks) and not used&masks[i]
            used|=masks[i]
        assert sum(sum(weights[x] for x in ordered[i]) for i in ids)>=threshold
        actual[ids[0]//2]+=1
        residual=((1<<84)-1)^used
        residuals.setdefault(residual,[]).append(ids)
    for j,c in enumerate(actual):assert c==(counts[j] if j in selected else 0)
    rows=[' '.join(str(x) for x in range(84) if (r>>x)&1)+'\n' for r in sorted(residuals)]
    (work/'residuals.txt').write_text(''.join(rows))
    for i in range(jobs):(work/f'domains_{i}.txt').write_text(''.join(rows[i::jobs]))
    record={'selected_cases':len(selected),'selected_packings':len(tuples),'distinct_residuals':len(rows),'threshold_per_case':100,'tuple_sha256':hashlib.sha256((work/'selected_tuples.txt').read_bytes()).hexdigest(),'residual_sha256':hashlib.sha256((work/'residuals.txt').read_bytes()).hexdigest()}
    (work/'residuals.json').write_text(json.dumps(record,indent=2)+'\n');return record

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--jobs',type=int,default=4);a=p.parse_args();print(json.dumps(prepare(a.work,a.jobs)))
