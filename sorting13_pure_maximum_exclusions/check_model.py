"""Direct clause, original-input and mixed-marker audit of a SAT model."""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEP=next(p/'sorting13_pruned10_mixed_kernels' for p in (HERE.parent,HERE.parents[2])
         if (p/'sorting13_pruned10_mixed_kernels').is_dir())


def scalar(v,word):
    v=list(v)
    for a,b in word:
        v[a],v[b]=min(v[a],v[b]),max(v[a],v[b])
    return v


def main(path):
    meta=json.loads(path.with_suffix('.meta.json').read_text())
    model=json.loads(path.with_suffix('.model.json').read_text())
    values={abs(v):v>0 for v in model}
    clauses=0
    with path.open() as stream:
        for line in stream:
            if not line.strip() or line[0] in 'cp':continue
            literals=[int(x) for x in line.split()[:-1]]
            assert any(values.get(abs(v),False)==(v>0) for v in literals),(clauses,literals)
            clauses+=1
    assert clauses==meta['clauses']
    word=[]
    for row in meta['choices']:
        choices=[j for j,v in enumerate(row) if values.get(v,False)]
        assert len(choices)==1
        word.append(meta['pairs'][choices[0]])
    f=json.loads((DEP/'fixture.json').read_text())
    case=json.loads((HERE/'pruning.json').read_text())['cases'][meta['extra']['case']]
    for mask in range(2048):
        v=[mask>>i&1 for i in range(11)]
        out=scalar(v,f['prefix']);out=[out[i] for i in f['prefix_output_order']]
        out=scalar(out,[[3,10],[6,9],[9,10]]+case['prefix'])
        assert scalar(out[:9],word)+out[9:]==sorted(v)
    active=[False]*len(word)
    for x in case['residual_states']:
        v=[x>>i&1 for i in range(9)]
        for t,(a,b) in enumerate(word):
            active[t]|=v[a]>v[b]
            v[a],v[b]=min(v[a],v[b]),max(v[a],v[b])
        assert v==sorted(x>>i&1 for i in range(9))
    for r in case['critical_single_bounds']+case['selected_mixed_bounds']:
        x=[r['x']>>i&1 for i in range(9)];y=[r['y']>>i&1 for i in range(9)];count=0
        for a,b in word:
            count+=bool(x[a] or x[b] or not y[a] or not y[b])
            x[a],x[b]=min(x[a],x[b]),max(x[a],x[b])
            y[a],y[b]=min(y[a],y[b]),max(y[a],y[b])
        assert count<=r['cap']+len(word)-14
    result=dict(status='all_clauses_and_original_inputs_verified',clauses=clauses,original_inputs=2048,
                case=case['case'],gates=len(word),network=word,all_gates_nonredundant=all(active))
    path.with_suffix('.model-verified.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path',type=Path);main(ap.parse_args().path)
