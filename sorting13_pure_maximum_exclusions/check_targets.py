"""Scalar, rank/port audit; imports neither ternary generator nor SAT encoder."""
import copy
import itertools
import json
import random
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEP=next(p/'sorting13_pruned10_mixed_kernels' for p in (HERE.parent,HERE.parents[2])
         if (p/'sorting13_pruned10_mixed_kernels').is_dir())
LOWER=[0,0,1,3,5,9,12,16,19,25,29,35]
SORT9=[(0,3),(1,7),(2,5),(4,8),(0,7),(2,4),(3,8),(5,6),
       (0,2),(1,3),(4,5),(7,8),(1,4),(3,6),(5,7),
       (0,1),(2,4),(3,5),(6,8),(2,3),(4,5),(6,7),(1,2),(3,4),(5,6)]
AFTER=[(3,10),(6,9),(9,10)]


def execute(v,word):
    v=list(v)
    for a,b in word:
        if v[a]>v[b]:v[a],v[b]=v[b],v[a]
    return v


def sorts(states,word):
    return all(execute([x>>i&1 for i in range(9)],word)==sorted(x>>i&1 for i in range(9)) for x in states)


def witness(w,fixture,prefix,n=9):
    high,low=set(w['fixed_high']),set(w['fixed_low'])
    assert not high&low and high|low<=set(range(11))
    free=[i for i in range(11) if i not in high|low]
    assert len(free)==w['middle_count']
    assert w['cap']==35-LOWER[len(free)]-w['deleted']
    count=0
    for bits in itertools.product((0,1),repeat=len(free)):
        values=[100 if i in high else -100 if i in low else bits[free.index(i)] for i in range(11)]
        labels=[2 if i in high else 0 if i in low else 1 for i in range(11)]
        ports=[None if i in high|low else free.index(i) for i in range(11)]
        retained=[];deleted=0
        for section_id,section in enumerate((fixture['prefix'],AFTER+prefix)):
            for a,b in section:
                hit=labels[a]!=1 or labels[b]!=1
                deleted+=hit
                if not hit:retained.append((ports[a],ports[b]))
                if labels[a]>labels[b]:
                    labels[a],labels[b]=labels[b],labels[a]
                    ports[a],ports[b]=ports[b],ports[a]
                if values[a]>values[b]:values[a],values[b]=values[b],values[a]
            if section_id==0:
                order=fixture['prefix_output_order']
                values=[values[i] for i in order]
                labels=[labels[i] for i in order]
                ports=[ports[i] for i in order]
        assert deleted==w['deleted']
        assert sum((v==2)<<i for i,v in enumerate(labels[:n]))==w['x']
        assert sum((v!=0)<<i for i,v in enumerate(labels[:n]))==w['y']
        assert values[n:] == sorted(values)[-(11-n):]
        middle_out=execute(bits,retained)
        assert [middle_out[p] for p in ports if p is not None]==[v for v in values if v in (0,1)]
        count+=1
    return count


def main():
    assert sorts(range(512),SORT9)
    f=json.loads((DEP/'fixture.json').read_text())
    data=json.loads((HERE/'pruning.json').read_text())
    X=set(json.loads((DEP/'certificate.json').read_text())['states'])
    image=set();closed=set()
    for x in X:
        v=[x>>i&1 for i in range(11)]
        assert max(v[:3])<=v[10]
        z=execute(v,[(3,10)])
        closed.add(sum(value<<i for i,value in enumerate(z)))
        assert max(z[:4])<=z[10]
        k=execute(z,[(6,9),(9,10)])
        assert k[10]==max(v)
        image.add(sum(value<<i for i,value in enumerate(k[:10])))
    assert len(closed)==132 and closed<=X
    assert len(image)==127 and image==set(data['kernel_states'])
    assert sorted(x.bit_length()-1 for x in image if x.bit_count()==1)==[4,5,6,8,9]
    for w in data['kernel_bounds']:witness(w,f,[],n=10)
    assert [w['cap'] for w in data['kernel_bounds']]==[2,1]
    # Independent support/coalescence enumeration of all binary-only kernels.
    completed=set()
    def dfs(positions,counts,word):
        if counts[2]>2 or counts[4]>1:return
        support=set(positions)
        if len(support)==1:
            if support=={9}:completed.add(tuple(word))
            return
        for a,b in itertools.combinations(sorted(support),2):
            q=tuple(v+int(pos in (a,b)) for pos,v in zip(positions,counts))
            nxt=tuple(b if pos==a else pos for pos in positions)
            dfs(nxt,q,word+[(a,b)])
    dfs((4,5,6,8,9),(0,0,0,0,0),[])
    expected={tuple(map(tuple,c['prefix'])) for c in data['cases']}
    assert completed==expected and len(completed)==3
    reports=[]
    for c in data['cases']:
        image=set()
        for mask in range(2048):
            inp=[mask>>i&1 for i in range(11)]
            out=execute(inp,f['prefix'])
            out=[out[i] for i in f['prefix_output_order']]
            out=execute(out,AFTER+c['prefix'])
            assert out[9:]==sorted(inp)[-2:]
            image.add(sum(v<<i for i,v in enumerate(out[:9])))
            assert execute(out[:9],SORT9)+out[9:]==sorted(inp)
        assert image==set(c['residual_states'])
        assert len(image)==[81,82,80][c['case']]
        candidates=sorted(x.bit_length()-1 for x in image if x.bit_count()==1)
        minima=sorted((511^x).bit_length()-1 for x in image if x.bit_count()==8)
        assert candidates==c['maximum_candidates'] and minima==c['minimum_candidates']
        assert all(not (x>>1&1) or (x>>8&1) for x in image)
        assert next(r for r in c['selected_mixed_bounds'] if (r['x'],r['y'])==(256,509))['cap']==2
        rows=c['all_single_bounds']+c['selected_mixed_bounds']
        seen=set();assignments=0
        for w in rows:
            key=tuple(w['fixed_high']),tuple(w['fixed_low'])
            if key not in seen:
                assignments+=witness(w,f,c['prefix']);seen.add(key)
        bad=copy.deepcopy(rows[0]);bad['deleted']+=1
        try:witness(bad,f,c['prefix'])
        except AssertionError:pass
        else:raise AssertionError('Corrupt deletion count accepted')
        # Cheap construction control: delete redundant gates in many orders.
        rng=random.Random(13000+c['case']);best=list(SORT9)
        for attempt in range(32):
            word=list(SORT9);order=list(range(25));rng.shuffle(order)
            removed=set()
            for index in order:
                trial=[gate for j,gate in enumerate(SORT9) if j not in removed|{index}]
                if sorts(image,trial):removed.add(index);word=trial
            if len(word)<len(best):best=word
        assert sorts(image,best)
        report=dict(case=c['case'],status='scalar_rank_port_verified',states=len(image),
                    original_inputs=2048,distinct_witnesses=len(seen),free_boolean_assignments=assignments,
                    maximum_caps=c['maximum_caps'],minimum_caps=c['minimum_caps'],
                    control_network=best,control_size=len(best),
                    greedy_control_trials=32,lower_bound=14,
                    corruption_control='Changed prefix deletion count rejected')
        reports.append(report)
        print(json.dumps({k:v for k,v in report.items() if k!='control_network'}),flush=True)
    (HERE/'targets-checked.json').write_text(json.dumps(dict(agent='six-sorting-2',role='researcher',cases=reports),indent=2)+'\n')


if __name__=='__main__':main()
