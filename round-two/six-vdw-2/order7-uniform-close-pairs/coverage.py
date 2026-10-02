"""Elementary 44-cycle bounds and separate tiny-cycle rotation controls."""
import itertools
import json
import time
from common import require


def fixed(cycle,d,b):
    selected={0,d}
    return {i:1-b if i in selected else b for i in range(cycle)
            if i in selected or i==cycle-1 or
            any(min((i-a)%cycle,(a-i)%cycle)<d for a in selected)}


def main():
    began=time.monotonic()
    # If m>=10 selected points are mutually at least3 apart, m<=14.
    # If their minimum is at least5, the cycle would have length>=50.
    possible=[]
    for m in range(10,45):
        require(5*m>44,'five-distance pigeonhole bound changed')
        if 3*m<=44:possible.append(m)
    require(possible==[10,11,12,13,14],'joint selected-count coverage differs')
    for d in [3,4]:
        require(44//d=={3:14,4:11}[d],'wrong branch upper count')
    require(all(3*m>44 for m in range(15,45)),
            'large selected set does not force a close pair')
    branch_free={}
    for d in [1,2,3,4]:
        for b in [0,1]:
            mapping=fixed(44,d,b)
            require(sum(v!=b for v in mapping.values())==2,'wrong selected anchors')
            branch_free[d]=44-len(mapping)
    require(branch_free=={1:41,2:39,3:36,4:33},'wrong normalized dimensions')

    checked=0
    for n in range(5,13):
        for word in itertools.product([0,1],repeat=n):
            for b in [0,1]:
                points=[i for i,v in enumerate(word) if v!=b]
                if not 2<=len(points)<n:continue
                gaps=[(points[(i+1)%len(points)]-p)%n
                      for i,p in enumerate(points)]
                d=min(gaps)
                if d>2:continue
                if d==1:
                    # Start a selected-color run of length at least two.
                    starts=[i for i in points if word[(i-1)%n]==b
                            and word[(i+1)%n]!=b]
                else:
                    starts=[p for p,g in zip(points,gaps) if g==d]
                require(starts,'missing permitted rotation')
                origin=starts[0]
                rotated=[word[(origin+i)%n] for i in range(n)]
                require(all(rotated[i]==v for i,v in fixed(n,d,b).items()),
                        'normalized fixed neighborhood differs')
                require(sum(v!=b for v in rotated)==len(points),
                        'rotation changes selected count')
                checked+=1
    # The result on 44 points uses the accompanying analytic argument; tiny
    # controls do not enumerate or certify all 2^44 phase words.
    result=dict(agent='six-vdw-2',role='researcher',
                status='EXACT_ANALYTIC_AND_TINY_ROTATION_COVER',
                selected_counts_requiring_computation=possible,
                computed_minimum_distances=[4,3],backgrounds=[0,1],
                normalized_minimum_distances=[1,2],
                normalized_free_phase_counts=[41,39],
                phase_and_color_variables_before_counters=[126,122],
                tiny_rotations_checked=checked,seconds=time.monotonic()-began)
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
