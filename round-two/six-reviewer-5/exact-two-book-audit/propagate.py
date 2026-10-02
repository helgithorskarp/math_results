"""Fresh first-support AC3 with literal22-point pages and fixed guards."""
from collections import deque
import time
from common import require,ALL22,digest


def compatible(profile,x,sx,y,sy,blue_caps=True,k4=True):
    red = bool(sx >> y & 1)
    if red != bool(sy >> x & 1):return False
    rx = (sx << 4)|profile['types'][x]; ry = (sy << 4)|profile['types'][y]
    if red:
        if (rx & ry).bit_count()>3:return False
        if k4:
            lows = profile['types'][x] & profile['types'][y]
            common_high = sx & sy
            if any(common_high & profile['low_masks'][i] for i in range(4) if lows >> i & 1):
                return False
    elif blue_caps:
        bx = ALL22 ^ rx ^ (1 << (x+4)); by = ALL22 ^ ry ^ (1 << (y+4))
        if (bx & by).bit_count()>6:return False
    return True


def close(profile,initial,blue_caps=True,k4=True):
    started = time.monotonic(); domains = [set(row) for row in initial]
    if any(not row for row in domains):
        return {'empty':True,'initial_empty':True,'batches':[],'tests':0,'remaining_sizes':[len(r) for r in domains]}
    queue = deque((x,y) for y in sorted(range(18),key=lambda y:(len(domains[y]),y))
                  for x in range(18) if x != y)
    queued = set(queue); support = {}; batches = []; tests = 0
    while queue:
        require(time.monotonic()-started<45,'INCOMPLETE fixed45-second AC3 guard')
        x,y = queue.popleft(); queued.remove((x,y)); removed = []; candidates = sorted(domains[y])
        for sx in sorted(domains[x]):
            key = (x,y,sx); prior = support.get(key)
            if prior in domains[y]:continue
            found = None
            for sy in candidates:
                tests += 1
                require(tests <= 20000000,'INCOMPLETE fixed20-million support-test guard')
                if compatible(profile,x,sx,y,sy,blue_caps,k4):found = sy;break
            if found is None:removed.append(sx)
            else:support[key] = found
        if removed:
            domains[x].difference_update(removed)
            batches.append({'target':x,'other':y,'removed':removed})
            if not domains[x]:
                return {'empty':True,'initial_empty':False,'batches':batches,'tests':tests,
                        'remaining_sizes':[len(r) for r in domains]}
            for z in range(18):
                if z not in (x,y) and (z,x) not in queued:
                    queue.append((z,x));queued.add((z,x))
    return {'empty':False,'initial_empty':False,'batches':batches,'tests':tests,
            'remaining_sizes':[len(r) for r in domains]}
