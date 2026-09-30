"""Independent exact audit by six-reviewer-4; CPython 3.11+, stdlib only.

No researcher checker, generator, SAT solver or watched-literal code is
imported. The optional full formula is regenerated separately with the
published generator; its mathematical correspondence is reviewed in REVIEW.md.
"""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAIRS9 = tuple(it.combinations(range(9), 2))
LOWER = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35)
PREFIX = ((0,10),(1,7),(2,5),(4,6),(8,4),(1,2),(5,7),
          (0,3),(8,1),(2,4),(5,6),(3,4),(9,7),(6,10))
ORDER = (0,8,1,2,3,9,4,5,6,7,10)
K_AFTER = ((3,10),(6,9),(9,10))
MINIMUM = ((0,5),(0,1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned_inputs():
    manifest=load(HERE/'provenance.json')
    checked=0
    for name,digest in manifest['target_source_sha256'].items():
        require(sha(ROOT/'sorting13_pure_minimum_exclusion'/name)==digest,'pinned target '+name)
        checked+=1
    for group in ('target_dependency_sha256','additional_reviewed_inputs_sha256'):
        for name,digest in manifest[group].items():
            require(sha(ROOT/name)==digest,'pinned input '+name)
            checked+=1
    return checked


def gate(mask, a, b):
    # Works also for a>b: first endpoint receives the minimum.
    if (mask >> a) & 1 and not (mask >> b) & 1:
        return mask ^ ((1 << a) | (1 << b))
    return mask


def word(mask, network):
    for a, b in network:
        mask = gate(mask, a, b)
    return mask


def ordered(mask, n):
    return ((1 << mask.bit_count()) - 1) << (n - mask.bit_count())


def image(mask, after):
    mask = word(mask, PREFIX)
    mask = sum(((mask >> old) & 1) << new for new, old in enumerate(ORDER))
    return word(mask, after)


def witnesses(entries, after, projection):
    """Color deletion plus independent scalar replay of retained middle ports."""
    assignments = 0
    for w in entries:
        high, low = set(w['fixed_high']), set(w['fixed_low'])
        require(not high & low and high | low <= set(range(11)), 'marker sets')
        middle = sorted(set(range(11)) - high - low)
        colors = [2 if i in high else 0 if i in low else 1 for i in range(11)]
        ports = [middle.index(i) if i in middle else None for i in range(11)]
        retained, deleted = [], 0
        for phase, network in enumerate((PREFIX, after)):
            for a, b in network:
                if colors[a] == colors[b] == 1:
                    retained.append((ports[a], ports[b]))
                else:
                    deleted += 1
                if colors[a] > colors[b]:
                    colors[a], colors[b] = colors[b], colors[a]
                    ports[a], ports[b] = ports[b], ports[a]
            if phase == 0:
                colors = [colors[i] for i in ORDER]
                ports = [ports[i] for i in ORDER]
        terminal = [colors[i] for i in projection]
        x = sum((c == 2) << i for i, c in enumerate(terminal))
        y = sum((c != 0) << i for i, c in enumerate(terminal))
        require((x, y, deleted, len(middle)) ==
                (w['x'], w['y'], w['deleted'], w['middle_count']), 'witness data')
        require(w['cap'] == 35 - LOWER[len(middle)] - deleted, 'pruning bound')
        trials = it.chain(it.product((0,1), repeat=len(middle)),
                          [tuple(range(len(middle))), tuple(range(len(middle)-1,-1,-1))])
        for values in trials:
            full = [100 if i in high else -100 if i in low
                    else values[middle.index(i)] for i in range(11)]
            for phase, network in enumerate((PREFIX, after)):
                for a,b in network:
                    full[a], full[b] = min(full[a],full[b]), max(full[a],full[b])
                if phase == 0:
                    full = [full[i] for i in ORDER]
            small = list(values)
            for a,b in retained:
                small[a], small[b] = min(small[a],small[b]), max(small[a],small[b])
            require([small[p] for p in ports if p is not None] ==
                    [v for v in full if -100 < v < 100], 'middle-port correspondence')
            assignments += 1
    return {'witnesses': len(entries), 'assignments': assignments,
            'distinct_rank_controls': 2*len(entries)}


def deduplicate(entries):
    result = {}
    for w in entries:
        key = (w['x'], w['y'])
        require(key not in result or result[key] == w, 'inconsistent duplicate')
        result[key] = w
    return list(result.values())


def zero_gate_closure():
    # Five complete Boolean masks; no published state table is input.
    initial = (32,128,509,288,40,0,0,0,0)
    seen, queue = {initial}, deque([initial])
    allowed = 0
    while queue:
        s = queue.popleft()
        rows, (q5,q8,u,q0) = s[:5], s[5:]
        require(not (rows == (256,256,510,384,384) and q0 == 2),
                'accepting state in sole-zero-gate closure')
        for a,b in PAIRS9:
            endpoints = (1 << a) | (1 << b)
            costs = (q5 + bool(rows[0] & endpoints), q8 + (8 in (a,b)),
                     u + bool(rows[3] & endpoints or 0 in (a,b)),
                     min(2,q0+(0 in (a,b))))
            if costs[0] > 2 or costs[1] > 1 or costs[2] > 4:
                continue
            allowed += 1
            successor = tuple(gate(r,a,b) for r in rows) + costs
            if successor not in seen:
                seen.add(successor); queue.append(successor)
    published = load(ROOT/'sorting13_maximum_preparation/min0-closure.json')
    converted = {(1 << s[0],1 << s[1],511 ^ (1 << s[2]),*s[3:])
                 for s in published['states']}
    require(seen == converted, 'entry-level sole-zero-gate closure mismatch')
    return {'states':len(seen),'transitions':len(seen)*36,'allowed':allowed}


def binary_closure():
    # Original three F cases need only two types of two-one test mask.
    initials = [(32,64,253,160,test,0,0) for test in (40,48)]
    seen, queue = set(initials), deque(initials)
    allowed = 0
    pairs = tuple(it.combinations(range(8),2))
    while queue:
        s = queue.popleft(); rows,u1,u2 = s[:5],s[5],s[6]
        require(rows != (128,128,254,192,192), 'accepting F state')
        for a,b in pairs:
            endpoints = (1 << a) | (1 << b)
            c1 = u1 + bool(endpoints & 128 or 0 in (a,b))
            c2 = u2 + bool(endpoints & rows[3] or 0 in (a,b))
            if c1 > 2 or c2 > 3:
                continue
            allowed += 1
            successor = tuple(gate(r,a,b) for r in rows)+(c1,c2)
            if successor not in seen:
                seen.add(successor);queue.append(successor)
    published = load(ROOT/'sorting13_double_pure_obstruction/closure.json')
    converted = {(1<<s[0],1<<s[1],255 ^ (1<<s[2]),*s[3:])
                 for s in published['states']}
    require(seen == converted, 'entry-level binary-maximum closure mismatch')
    return {'states':len(seen),'transitions':len(seen)*28,'allowed':allowed}


def kernel_cover():
    # Generate partial forests by occupied group ports and path costs.
    valid = []
    def explore(positions,costs,network):
        if positions == (7,7,7):
            valid.append(network);return
        if len(network) == 3:
            return
        for a,b in it.combinations((1,2,3,4,6,7),2):
            if not {a,b} & set(positions):
                continue
            newcosts = tuple(c+(p in (a,b)) for p,c in zip(positions,costs))
            if max(newcosts)>2:
                continue
            newpositions = tuple(b if p==a else p for p in positions)
            explore(newpositions,newcosts,network+((a,b),))
    explore((3,4,7),(0,0,0),())
    counts = Counter(map(len,valid))
    require(counts == {2:3,3:21}, 'maximum-forest coverage')
    full = {w+((5,7),(7,8)) for w in valid if len(w)==3}
    expected = load(ROOT/'sorting13_maximum_preparation/fixture.json')['maximum_kernel_words']
    require(full == {tuple(map(tuple,w)) for w in expected}, 'entry-level forest mismatch')
    for network in full:
        positions = [3,4,5,7,8];costs = [0]*5
        for a,b in network:
            for i,p in enumerate(positions):
                costs[i] += p in (a,b)
                if p==a:positions[i]=b
        require(costs == [4,4,2,4,1] and positions == [8]*5, 'exact maximum costs')
    return {'binary_words':3,'unary_words':21,'exact_passages':[4,4,2,4,1]}


def mathematics():
    f=load(ROOT/'sorting13_maximum_preparation/fixture.json')
    require(tuple(map(tuple,f['prefix']))==PREFIX and tuple(f['prefix_output_order'])==ORDER,
            'explicit target prefix')
    require(tuple(map(tuple,f['after']))==K_AFTER+MINIMUM, 'explicit target suffix')
    require(tuple(f['lower_sizes'])==LOWER, 'imported lower bounds')
    K,L=set(),set()
    for original in range(2048):
        k=image(original,K_AFTER);ell=image(original,K_AFTER+MINIMUM)
        require((k>>10)==int(original!=0), 'K maximum removal')
        require((ell&1)==int(original==2047) and (ell>>10)==int(original!=0),
                'L extreme removal')
        K.add(k&1023);L.add((ell>>1)&511)
        kout=word(k&1023,f['K_control20']) | (k&1024)
        lout=(ell&1025) | (word((ell>>1)&511,f['control18'])<<1)
        require(kout==ordered(original,11) and lout==ordered(original,11), 'positive control')
    require(K==set(f['K_states']) and L==set(f['states']) and len(L)==109, 'all target rows')
    require({ordered((1<<k)-1,9) for k in range(10)} <= L, 'all sorted weights for normalization')
    old=deduplicate(f['critical_single_bounds']+f['selected_mixed_bounds']+f['designated_bounds'])
    extra=load(ROOT/'sorting13_pure_minimum_exclusion/additional_witnesses.json')
    require(len(old)==53 and len(extra)==92 and len(deduplicate(old+extra))==145,
            'all witness coverage')
    base=witnesses(old,K_AFTER+MINIMUM,range(1,10))
    added=witnesses(extra,K_AFTER+MINIMUM,range(1,10))
    bf=load(ROOT/'sorting13_double_pure_obstruction/fixture.json')
    kmarker=witnesses(bf['K_witnesses'],K_AFTER,range(10))
    fmarker=[]
    for c in bf['cases']:
        network=tuple(map(tuple,c['maximum_prefix']))
        rows={word(r,network)&255 for r in L}
        require(rows==set(c['states']), 'binary F image')
        lift=tuple((a+1,b+1) for a,b in network)
        fmarker.append(witnesses(c['witnesses'],K_AFTER+MINIMUM+lift,range(1,9)))
    return {'original_inputs':2048,'K_states':len(K),'L_states':len(L),
            'original_positive_controls':4096,'old_markers':base,'new_markers':added,
            'K_markers':kmarker,'binary_F_markers':fmarker,
            'sole_zero_gate':zero_gate_closure(),'binary_maximum_exclusion':binary_closure(),
            'maximum_word_cover':kernel_cover()}


def clauses(path,variables=None):
    header=None;rows=[]
    for line in path.read_text().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p'):
            require(header is None,'duplicate DIMACS header')
            h=line.split();require(h[:2]==['p','cnf'] and len(h)==4,'DIMACS header')
            header=tuple(map(int,h[2:]));continue
        ls=tuple(map(int,line.split()))
        require(ls and ls[-1]==0 and all(v!=0 for v in ls[:-1]),'DIMACS clause')
        rows.append(tuple(dict.fromkeys(ls[:-1])))
    require(header is not None and len(rows)==header[1],'DIMACS count')
    require(variables is None or variables==header[0],'variable count')
    require(all(abs(v)<=header[0] for c in rows for v in c),'variable range')
    return header[0],rows


class IncidenceRUP:
    """Scan only clauses containing a newly false literal; no watched literals."""
    def __init__(self,rows):
        self.rows=[];self.lengths=[];self.occ=defaultdict(list);self.units=[];self.empty=False
        for c in rows:self.add(c)

    def add(self,c):
        index=len(self.rows);self.rows.append(c);self.lengths.append(len(c))
        if not c:self.empty=True
        if len(c)==1:self.units.append(c[0])
        for v in c:self.occ[v].append(index)

    def entails(self,c):
        if self.empty:return True
        # Each clause's remaining count is the number of literals not yet
        # false. Decrease it only on a newly false occurrence. Scan a clause
        # only when its counter reaches1; no watch selection/movement exists.
        remaining=self.lengths.copy()
        assigned=set();pending=list(self.units)+[-v for v in c]
        while pending:
            v=pending.pop()
            if -v in assigned:return True
            if v in assigned:continue
            assigned.add(v)
            for index in self.occ.get(-v,()):
                remaining[index]-=1
                if remaining[index]==0:return True
                if remaining[index]==1:
                    for z in self.rows[index]:
                        if -z not in assigned:
                            if z not in assigned:pending.append(z)
                            break

        return False


def slow_rup(rows,c):
    pending=set(-v for v in c)
    while True:
        if any(-v in pending for v in pending):return True
        units=set()
        for row in rows:
            if any(v in pending for v in row):continue
            left=[v for v in row if -v not in pending]
            if not left:return True
            if len(left)==1:units.add(left[0])
        new=units-pending
        if not new:return False
        pending.update(new)


def rup_controls():
    # Deterministic exhaustive three-variable formulas of at most two clauses.
    pool=[tuple((i+1)*v for i,v in enumerate(signs) if v)
          for signs in it.product((-1,0,1),repeat=3)]
    controls=0
    for count in range(3):
        for rows in it.combinations(pool,count):
            checker=IncidenceRUP(rows)
            for c in pool:
                answer=checker.entails(c)
                require(answer==slow_rup(rows,c),'incidence/full-scan unit-propagation mismatch')
                if answer:
                    for bits in it.product((False,True),repeat=3):
                        def satisfied(row):
                            return any(bits[abs(v)-1]==(v>0) for v in row)
                        require(not all(map(satisfied,rows)) or satisfied(c),'RUP soundness truth table')
                controls+=1
    require(not IncidenceRUP([(1,2)]).entails((1,)),'invalid unit control')
    return controls


def certificate(full,seconds):
    start=time.monotonic();directory=ROOT/'sorting13_pure_minimum_exclusion'
    cert=load(directory/'certificate.json')
    require(sha(directory/'core.cnf')==cert['core_sha256'] and
            sha(directory/'proof.rup')==cert['rup_sha256'],'certificate hashes')
    n,core=clauses(directory/'core.cnf',cert['variables'])
    require(len(core)==cert['core_clauses'],'core count')
    require(full is not None,'full source formula required')
    needed={frozenset(c) for c in core};digest=hashlib.sha256();count=0
    with full.open('rb') as stream:
        head=stream.readline();digest.update(head)
        require(head.split()==[b'p',b'cnf',str(n).encode(),str(cert['cnf']['clauses']).encode()],
                'full formula header')
        for line in stream:
            digest.update(line);count+=1;ls=list(map(int,line.split()))
            require(ls[-1]==0 and all(0<abs(v)<=n for v in ls[:-1]),'full formula clause')
            needed.discard(frozenset(ls[:-1]))
    require(not needed and count==cert['cnf']['clauses'] and
            digest.hexdigest()==cert['cnf']['sha256'],'core source membership/hash')
    controls=rup_controls();checker=IncidenceRUP(core)
    require(not checker.entails(()),'premature empty-clause accepted')
    additions=0;ended=False
    for line in (directory/'proof.rup').read_text().splitlines():
        require(not ended,'proof data after empty clause')
        require(not line.startswith('d'),'unsupported proof deletion')
        ls=tuple(map(int,line.split()))
        require(ls and ls[-1]==0 and all(0<abs(v)<=n for v in ls[:-1]),'RUP clause syntax')
        clause=tuple(dict.fromkeys(ls[:-1]))
        require(checker.entails(clause),f'RUP failed at addition {additions+1}')
        checker.add(clause);additions+=1
        ended=not clause
        if additions%100==0:
            require(time.monotonic()-start<seconds,'incomplete replay: operational time bound')
        if additions%2000==0:
            print(f'RUP additions verified: {additions}',file=sys.stderr,flush=True)
    require(ended and additions==cert['proof_additions'],'terminal refutation/count')
    return {'variables':n,'full_source_clauses':count,'core_clauses':len(core),
            'rup_additions':additions,'full_cnf_sha256':digest.hexdigest(),
            'rup_sha256':cert['rup_sha256'],'core_sha256':cert['core_sha256'],
            'tiny_controls':controls,'premature_empty_rejected':True,
            'invalid_unit_rejected':True,'replay_seconds':time.monotonic()-start}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=600)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();start=time.monotonic()
    result={'agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'status':'VERIFIED','pinned_inputs':pinned_inputs(),'mathematics':mathematics(),
            'certificate':certificate(args.full,args.seconds)}
    result.update(seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    print(rendered,end='')


if __name__=='__main__':main()
