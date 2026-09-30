"""Established7356/7402 K18 necessities; exact selected-prefix scope.

Author: six-sorting-2, researcher. Mathematical derivations are cited in
PROOF.md. All gates remain sequential and every pair remains selectable.
"""
import hashlib
from pathlib import Path
from sequential_sat import neg

HERE = Path(__file__).resolve().parent

def augment(w,choices,pairs,bits,pruning,gates,branch,frozen,tight=False):
    events_by_pair={}
    def events(x,y):
        if (x,y) in events_by_pair:return events_by_pair[x,y]
        hits=[w.var() for _ in range(gates)]
        for t in range(gates):
            for j,(a,b) in enumerate(pairs):
                c=choices[t][j]
                outside=[bits[x][t][a],bits[x][t][b],neg(bits[y][t][a]),neg(bits[y][t][b])]
                for v in outside:w.add(-c,neg(v),hits[t])
                w.add(-c,-hits[t],*outside)
        events_by_pair[x,y]=hits
        return hits
    for r in pruning['critical_single_bounds']+pruning['selected_mixed_bounds']:
        w.at_most(events(r['x'],r['y']),r['cap']+gates-18)
    if gates==18:
        phases=[[w.var() for _ in range(3)] for _ in range(gates+1)]
        for p in phases:w.exactly_one(p)
        w.add(phases[0][0]);w.add(phases[-1][2])
        for t in range(gates):
            for s in range(3):
                for j,pair in enumerate(pairs):
                    if s==0:dest=1 if pair==(6,8) else 0 if 6 not in pair and 9 not in pair else None
                    elif s==1:dest=2 if pair==(8,9) else 1 if 8 not in pair and 9 not in pair else None
                    else:dest=2 if 9 not in pair else None
                    if dest is None:w.add(-phases[t][s],-choices[t][j])
                    else:w.add(-phases[t][s],-choices[t][j],phases[t+1][dest])
        # OR separate one-hot trajectory passages, rather than their input OR.
        kernel=[w.var() for _ in range(gates)]
        rows=[events(1<<i,1023) for i in (4,5,6,8,9)]
        for t in range(gates):w.equivalent_or(kernel[t],[r[t] for r in rows])
        w.at_most([neg(v) for v in kernel],gates-5)
        post=[]
        for t in range(gates):
            incidence=w.var()
            w.equivalent_or(incidence,[choices[t][j] for j,(a,b) in enumerate(pairs) if b==8])
            p=w.var();post.append(p)
            w.add(-p,phases[t][2]);w.add(-p,incidence)
            w.add(p,-phases[t][2],-incidence)
        w.add(*post)
        minimum=events(0,1021)
        if branch==1:w.at_most(minimum,1)
        elif branch==2:w.at_most([neg(v) for v in minimum],gates-2)
        if tight:
            assert branch==1
            w.exactly_one(post)
            for t in range(gates):
                for j,(a,b) in enumerate(pairs):
                    if b==8 and a<6:w.add(-phases[t][2],-choices[t][j])
            early_seven=[]
            j78=pairs.index((7,8));j68=pairs.index((6,8))
            for t in range(gates):
                v=w.var();early_seven.append(v)
                w.add(-v,phases[t][0]);w.add(-v,choices[t][j78])
                w.add(v,-phases[t][0],-choices[t][j78])
            some_early_seven=w.var();w.equivalent_or(some_early_seven,early_seven)
            for t in range(gates):w.add(-phases[t][2],-choices[t][j68],some_early_seven)
            minphase=[[w.var(),w.var()] for t in range(gates+1)]
            for p in minphase:w.exactly_one(p)
            w.add(minphase[0][0]);w.add(minphase[-1][1])
            for t in range(gates):
                for s in range(2):
                    for j,pair in enumerate(pairs):
                        dest=1 if s==0 and pair==(0,1) else 0 if s==0 and 1 not in pair else 1 if s==1 and 0 not in pair else None
                        if dest is None:w.add(-minphase[t][s],-choices[t][j])
                        else:w.add(-minphase[t][s],-choices[t][j],minphase[t+1][dest])
    else:assert branch==0,'Lower-target phase/branch conditions only apply at budget18'
    if frozen:
        assert len(frozen)==gates
        for t,pair in enumerate(frozen):w.add(choices[t][pairs.index(tuple(pair))])
    return dict(reference_budget=18,minimum1_branch=branch,single_bounds=len(pruning['critical_single_bounds']),
                mixed_bounds=len(pruning['selected_mixed_bounds']),maximum_kernel_hits_at_least=5 if gates==18 else None,
                post_root_wire8_gate=gates==18,forced_two_step_maximum_path=gates==18,
                checked_cut_tightening=tight,
                minimum_cut_source='aedd5f48b84a375cbd671d1daf331ede87815959' if tight else None,
                minimum_cut_graph='bafkreidz4bwlbltow7uuh33gz7xzdaqb5423jdieri23sg4zcsiwfwawzi' if tight else None,
                post_root_lower_endpoints=[6,7] if tight else None,
                refill6_requires_early78=tight,
                checked_cut_sha256='1c27e4f8f939e60a1d3a625f3f3f8ae92e4d65ef56e765433b8ef2dae5a353d5' if tight else None,
                source_dependency='22df206b4e24029da4d90c9831a45ebc99e2d51a',
                graph_dependency='bafkreig6zqoz7ozhoct65mt3v4amdp7p3da54wyefgo3ljw5m4zwyvcuzu',
                pruning_sha256=hashlib.sha256((HERE/'pruning.json').read_bytes()).hexdigest(),
                filters='No lex, interval, fixed depth, maximum DFA, repeated-pair or nonredundancy filter')
