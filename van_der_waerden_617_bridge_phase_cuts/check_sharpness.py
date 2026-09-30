#!/usr/bin/env python3
"""Independent exhaustive test of two specified criterion exceptions.

This checks only absence of opposed symmetric AP completions at width1108.
It does not certify an AP-free bridge filling. All geometric possibilities
are visited directly, without the generator's reduced center/step bounds.
"""
import json
import time

P, N, C, H = 617, 3704, 1852, 554


def run():
    start = time.monotonic()
    if any(P % d == 0 for d in range(2, 25)):
        raise ValueError('617 is not prime')
    q = [-1]+[int(pow(r,308,P) == P-1) for r in range(1,P)]
    lo, hi = C-H, C+H
    cases = []
    for s,t,g in [(463,154,1),(464,155,1)]:
        word = [None]*N
        for x in range(N):
            if lo <= x < hi:
                continue
            r = (x-C+(s if x<lo else t)) % P
            if r:
                word[x] = q[r] ^ (0 if x<lo else g)
        geometric = protected = homogeneous = 0
        forced_centers = [0,0]
        centers = []
        for v in range(lo, hi):
            colors = set()
            for d in range(1, (N-1)//6+1):
                if v-3*d < 0 or v+3*d >= N:
                    continue
                points = [v+j*d for j in (-3,-2,-1,1,2,3)]
                if any(lo <= x < hi for x in points):
                    continue
                geometric += 1
                values = [word[x] for x in points]
                if any(value is None for value in values):
                    continue
                protected += 1
                if all(value == values[0] for value in values):
                    homogeneous += 1
                    colors.add(1-values[0])
            if len(colors) == 2:
                raise ValueError(f'opposed symmetric completions exist for {(s,t,g,v)}')
            if colors:
                b = next(iter(colors))
                forced_centers[b] += 1
                centers.append([v,b])
        cases.append({'key':[s,t,g],'geometric_symmetric_AP_frames':geometric,
                      'protected_nonpole_frames':protected,
                      'homogeneous_six_premise_frames':homogeneous,
                      'centers_forcing_each_color':forced_centers,
                      'forced_centers':centers,
                      'opposed_symmetric_completion_pairs':0})
    return {'agent':'six-vdw-3','role':'researcher',
            'status':'VERIFIED_SPECIFIED_CRITERION_EXCEPTIONS',
            'half_width':H,'bridge':[lo,hi],
            'center_difference_combinations_visited_per_case':2*H*((N-1)//6),
            'cases':cases,'seconds':time.monotonic()-start,
            'scope':'No opposed symmetric completion pair for these two keys; no extendibility or AP-free full coloring is asserted.'}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
