"""Literal standard-library audit; imports neither encoder nor SAT solver."""
import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def literal_model():
    special=set(range(0,108,2))
    free=sorted(set(range(109))-special)
    def axis(x,c):
        q=min(x,109-x)
        if q in (1,2):return c==q-1
        return False if c<2 else 4*(q-3)+c-1
    def column(x,c):
        if x in special:return c==0
        return False if c<2 else 208+4*free.index(x)+c-1
    clauses=set()
    def forbid(values):
        if any(v is False for v in values):return
        clauses.add(tuple(sorted({-v for v in values if v is not True})))
    for row in [[axis(q,c) for c in range(2,6)] for q in range(3,55)]+[
                [column(q,c) for c in range(2,6)] for q in free]:
        clauses.add(tuple(sorted(row)))
        for x,y in itertools.combinations(row,2):forbid([x,y])
    for x in range(1,109):
        for y in range(1,109):
            z=(x+y)%109
            if z:
                for c in range(6):forbid([axis(x,c),axis(y,c),axis(z,c)])
    for x in range(109):
        for y in range(x+1,109):
            for c in range(6):forbid([column(x,c),column(y,c),axis(y-x,c)])
    for q in range(3,55):
        for c in range(3,6):
            clauses.add(tuple(sorted([-axis(q,c)]+[axis(old,c-1) for old in range(3,q)])))
    return clauses


def audit(cnf=None,proof=None,drat_trim=None,seconds=120):
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    S=set(data['normalized_special_support'])
    require(S==set(range(0,108,2)),'special support')
    require(len(S)==54 and not any((q+1)%109 in S for q in S),'cycle independence')
    rotations={tuple(sorted((q+t)%109 for q in S)) for t in range(109)}
    require(len(rotations)==109,'rotations')
    for support in rotations:
        gaps=[(support[(j+1)%54]-q)%109 for j,q in enumerate(support)]
        require(gaps.count(2)==53 and gaps.count(3)==1,'gap pattern')
    expected=literal_model()
    require(len(expected)==10161,'literal clause count')
    result=dict(status='LITERAL_MODEL_AND_CYCLE_NORMALIZATION_CHECKED',
                variables=428,clauses=10161,special_support_size=54,common_column_positions=55,
                maximum_cycle_rotations=109,cnf_checked=False,proof_checked=False)
    require(proof is None or (cnf is not None and drat_trim is not None),'proof requires CNF and checker')
    if cnf is not None:
        require(digest(cnf)==data['cnf_sha256'],'CNF hash')
        require(Path(cnf).stat().st_size==data['cnf_bytes'],'CNF size')
        lines=Path(cnf).read_text().splitlines()
        require(lines[0]=='p cnf 428 10161','CNF header')
        rows=[]
        for line in lines[1:]:
            values=list(map(int,line.split()))
            require(values and values[-1]==0 and 0 not in values[:-1],'CNF terminator')
            require(all(1<=abs(v)<=428 for v in values[:-1]),'literal domain')
            require(len(set(values[:-1]))==len(values[:-1]),'repeated literal')
            rows.append(tuple(sorted(values[:-1])))
        require(len(rows)==10161 and set(rows)==expected,'literal clause mismatch')
        result.update(cnf_checked=True,cnf_sha256=data['cnf_sha256'])
    if proof is not None:
        with tempfile.TemporaryFile() as log:
            proc=subprocess.run([str(drat_trim),str(cnf),str(proof),'-I','-U','-t',str(seconds)],
                                stdout=log,stderr=subprocess.STDOUT,timeout=seconds+10)
            log.seek(0);output=log.read().decode(errors='replace')
        require(proc.returncode==0 and 's VERIFIED' in output.splitlines(),'RUP check failed: '+output[-1200:])
        sha=digest(proof)
        result.update(status='FIRST_SPECIAL_COLUMN_UPPER_BOUND_53_VERIFIED',proof_checked=True,
                      first_special_column_upper_bound=53,sharpness_established=False,
                      proof_bytes=Path(proof).stat().st_size,proof_sha256=sha,
                      matches_reference_proof=(sha==data['proof_sha256']))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cnf',type=Path);parser.add_argument('--proof',type=Path)
    parser.add_argument('--drat-trim',type=Path);parser.add_argument('--seconds',type=int,default=120)
    a=parser.parse_args();print(json.dumps(audit(a.cnf,a.proof,a.drat_trim,a.seconds),indent=2))
