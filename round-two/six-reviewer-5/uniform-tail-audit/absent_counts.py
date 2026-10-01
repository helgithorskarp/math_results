"""Independent complete aggregate m=0 readout, no code-packing enumeration.

Rows are necessary integer inventories. Scalar survivors are not constructions.
The two survivors are excluded by the written literal uncovered-pair capacity.
"""
from itertools import product
from hashlib import sha256
from pathlib import Path
import argparse
import json

from local_pair import encode, require

HERE = Path(__file__).resolve().parent


def candidates(du, dv):
    require(du+dv == 20 and (du,dv) in [(16,4),(12,8)], 'two profiles')
    checked, survivors = 0, []
    # A/B good points have deficit1 or2 after the degree-zero exclusion.
    # A T0 point has its two positive deficits summing5; T3 has1,1.
    # All total T counts are <=4 from the cross-excess equation.
    for t0 in range(5):
        for heavy in product(range(1,5), repeat=t0):
            for t3 in range(5-t0):
                t = t0+t3
                wa, wb = du-sum(heavy)-t3, dv-sum(5-h for h in heavy)-t3
                if wa < 0 or wb < 0:
                    continue
                for a2 in range(wa//2+1):
                    a1 = wa-2*a2
                    for b2 in range(wb//2+1):
                        b1 = wb-2*b2
                        if a1+a2+b1+b2+t != 16:
                            continue
                        checked += 1
                        da, db, dt = 4*a1+3*a2, 4*b1+3*b2, 3*t3
                        require(da+db+dt == 60, 'deficit degree accounting')
                        # A and B independent. T0 is isolated in G.
                        for tt in range(min(t3*(t3-1)//2,dt//2)+1):
                            external = dt-2*tt
                            if (external+da-db) % 2:
                                continue
                            at = (external+da-db)//2
                            bt = external-at
                            ab = da-at
                            if min(at,bt,ab) < 0 or ab != db-bt:
                                continue
                            if at > (a1+a2)*t3 or bt > (b1+b2)*t3 or ab > (a1+a2)*(b1+b2):
                                continue
                            require(ab+at+bt+tt == 30, 'whole edge sum')
                            survivors.append(dict(a1=a1,a2=a2,b1=b1,b2=b2,
                                                  t0=t0,t3=t3, heavy_u=list(heavy),
                                                  da=da,db=db,at=at,bt=bt,ab=ab,tt=tt))
    return dict(profile=[du,dv], checked_inventories=checked, survivors=survivors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path)
    args = parser.parse_args()
    records = [candidates(16,4),candidates(12,8)]
    require(records[0]['survivors'] == [], 'no16/19 scalar candidates')
    require(records[1]['survivors'] == [
        dict(a1=5,a2=3,b1=7,b2=0,t0=0,t3=1,heavy_u=[],da=29,db=28,at=2,bt=1,ab=27,tt=0),
        dict(a1=6,a2=2,b1=6,b2=0,t0=0,t3=2,heavy_u=[],da=30,db=24,at=6,bt=0,ab=24,tt=0)],
        'complete17/18 aggregate domain')
    require(29-3*2 == 23 > 7*6//2 == 21, 'first uncovered B-pair capacity')
    require(6*4+2*3 == 30 > 8*7//2 == 28, 'second uncovered A-pair capacity')
    exact = dict(agent='six-reviewer-5',role='independent mathematical reviewer',
                 profiles=records, final_pair_obstructions=[[23,21],[30,28]])
    digest = sha256(encode(exact)).hexdigest()
    if (HERE/'ABSENT_EXPECTED.json').exists():
        require(json.loads((HERE/'ABSENT_EXPECTED.json').read_text()) == exact,
                'frozen aggregate readout changed')
    result = dict(status='COMPLETE',exact_sha256=digest,**exact)
    if args.out:
        args.out.write_bytes(encode(result))
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
