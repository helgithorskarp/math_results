"""SAT-free witness and terminal-threshold audit; imports no other checker."""
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEP=HERE.parent/'sorting13_pruned10_mixed_kernels'


def execute(v,word):
    v=list(v)
    for a,b in word:
        if v[a]>v[b]:v[a],v[b]=v[b],v[a]
    return v


def threshold_events(n,x,word):
    v=[x>>i&1 for i in range(n)];total=0
    for a,b in word:
        total+=bool(v[a] or v[b])
        v=execute(v,[(a,b)])
    return total


def small_controls():
    checked=0;admissible=0
    for n in (3,4):
        d,e,f=n-3,n-2,n-1
        pairs=list(itertools.combinations(range(n),2))
        for depth in range(5):
            for word in itertools.product(pairs,repeat=depth):
                for i,j in itertools.combinations(range(n-1),2):
                    rows=[1<<d,1<<e,(1<<i)|(1<<j)]
                    sorts=all(execute([x>>k&1 for k in range(n)],word)==sorted(x>>k&1 for k in range(n)) for x in rows)
                    if sorts and sum(f in gate for gate in word)==1:
                        assert threshold_events(n,(1<<d)|(1<<f),word)>=3
                        admissible+=1
                    checked+=1
    return checked,admissible


def main():
    f=json.loads((DEP/'fixture.json').read_text())
    data=json.loads((HERE/'pruning.json').read_text())
    controls,admissible=small_controls()
    checks=[]
    for case in data['cases']:
        J=set()
        for mask in range(2048):
            values=[mask>>i&1 for i in range(11)]
            out=execute(values,f['prefix']);out=[out[i] for i in f['prefix_output_order']]
            out=execute(out,[(3,10),(6,9),(9,10)]+case['prefix'])
            assert out[9:]==sorted(values)[-2:]
            J.add(sum(v<<i for i,v in enumerate(out[:9])))
        assert J==set(case['residual_states'])
        assert {64,128,256,320,509}<=J
        assert all(not (x>>1&1) or x>>8&1 for x in J)
        two=next(x for x in sorted(J) if x.bit_count()==2 and not x>>8&1)
        assignment_checks=0
        for x,D,k,cap in ((256,17,7,2),(320,20,6,3)):
            r=next(r for r in case['selected_mixed_bounds'] if (r['x'],r['y'])==(x,509))
            assert (r['deleted'],r['middle_count'],r['cap'])==(D,k,cap)
            assert 35-({6:12,7:16}[k])-D==cap
            high=set(r['fixed_high']);low=set(r['fixed_low'])
            free=[i for i in range(11) if i not in high|low]
            assert not high&low and len(free)==k
            for bits in itertools.product((0,1),repeat=k):
                v=[2 if i in high else -1 if i in low else bits[free.index(i)] for i in range(11)]
                deleted=0
                for section_id,word in enumerate((f['prefix'],[(3,10),(6,9),(9,10)]+case['prefix'])):
                    for a,b in word:
                        deleted+=v[a] in (-1,2) or v[b] in (-1,2)
                        v=execute(v,[(a,b)])
                    if section_id==0:v=[v[i] for i in f['prefix_output_order']]
                assert deleted==D
                assert sum((v[i]==2)<<i for i in range(9))==x
                assert sum((v[i]!=-1)<<i for i in range(9))==509
                assignment_checks+=1
        row=dict(case=case['case'],status='elementary_witnesses_verified',states=len(J),
                 original_inputs=2048,mixed_caps=[2,3],free_scalar_assignments=assignment_checks,
                 one_hot_rows=[64,128,256],two_one_final_wire_empty=two,
                 proof='Written ordered-route lemma forces q8=r1=1; H320<=2 contradicts terminal-threshold lemma H320>=3')
        checks.append(row);print(json.dumps(row),flush=True)
    result=dict(agent='six-sorting-2',role='researcher',cases=checks,
                small_word_row_controls=controls,admissible_one_final_gate_controls=admissible)
    scratch=HERE/'scratch';scratch.mkdir(exist_ok=True)
    (scratch/'elementary-checked.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'small_word_row_controls':controls,'admissible_one_final_gate_controls':admissible}))


if __name__=='__main__':main()
