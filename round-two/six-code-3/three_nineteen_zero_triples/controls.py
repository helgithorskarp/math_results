"""Small exhaustive graph controls and malformed exact-evidence rejection."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import produce
import verify
import verify_capacity

HERE=Path(__file__).resolve().parent


def run(work):
    labels=(0,3,9,18,32)
    edges=list(combinations(range(5),2))
    decisions=0
    for graph in range(1 << len(edges)):
        neighbors=[set() for _ in range(33)]
        for j,(a,b) in enumerate(edges):
            if graph & (1 << j):
                neighbors[labels[a]].add(labels[b]);neighbors[labels[b]].add(labels[a])
        bit_rows=[sum(1 << j for j in n) for n in neighbors]
        for size in range(1,6):
            brute=sorted(q for q in combinations(labels,size)
                         if all(b in neighbors[a] for a,b in combinations(q,2)))
            primary,_=produce.cliques(bit_rows,sum(1 << i for i in labels),target=size)
            secondary,_=verify.nine_cliques(neighbors,labels,target=size)
            verify.compare(primary,brute,'color recursion small-graph disagreement')
            verify.compare(secondary,brute,'maximal recursion small-graph disagreement')
            decisions+=1
    core=json.loads((work/'joints-0.json').read_text())[0]
    data=json.loads((HERE/'capacity.json').read_text())
    certificate=next(c for c in data['certificates'] if c['core_sha256']==core['core_sha256'])
    verify_capacity.check_one(core,certificate)
    rejections=0
    def reject(function,exception=ValueError,contains=None):
        nonlocal rejections
        try:
            function()
        except exception as error:
            if contains is not None:
                verify.check(contains in str(error),'wrong guard result')
            rejections+=1
        else:
            raise ValueError('bad control accepted')
    for edit in ['empty','negative','duplicate','covered','bool_denominator','hash','sum']:
        bad=deepcopy(certificate)
        if edit=='empty':bad['weights']=[];bad['numerator']=0
        elif edit=='negative':bad['weights'][0][-1]=-1
        elif edit=='duplicate':bad['weights'].append(bad['weights'][0][:])
        elif edit=='covered':
            word=next(frozenset(i for i in range(15) if w & (1 << i))
                      for w in core['blocks'] if (w & ((1 << 15)-1)).bit_count()>=3)
            bad['weights'].append([*sorted(word)[:3],1])
        elif edit=='bool_denominator':bad['denominator']=True
        elif edit=='hash':bad['candidate_sha256']='0'*64
        elif edit=='sum':bad['numerator']+=1
        reject(lambda:verify_capacity.check_one(core,bad))
    bad_core=deepcopy(core);bad_core['blocks'][0]=bad_core['blocks'][1]
    reject(lambda:verify_capacity.check_one(bad_core,certificate))
    # Recreate the specific omitted-anchor failure that the pilot decoder caught.
    words=[verify.points(w) for w in core['blocks']]
    anchor=next(w for w in words if {16,17}<=w)
    old=sorted(anchor-{16,17})
    extra=next(i for i in range(15) if i not in old)
    replacement=frozenset(old+[extra,15])
    position=next(i for i,w in enumerate(words) if 15 in w and 16 not in w and 17 not in w)
    words[position]=replacement
    reject(lambda:verify.packing(words,42))
    complete=[set(range(5))-{i} for i in range(5)]
    bit_complete=[sum(1 << j for j in n) for n in complete]
    reject(lambda:produce.cliques(bit_complete,31,target=3,node_cap=1),
           RuntimeError,'INCOMPLETE')
    reject(lambda:verify.nine_cliques(complete,range(5),target=3,node_cap=1),
           RuntimeError,'INCOMPLETE')
    reject(lambda:produce.cliques(bit_complete,31,target=3,node_cap=0))
    reject(lambda:verify.nine_cliques(complete,range(5),target=3,node_cap=0))
    result={'status':'PASSED','small_graphs':1024,'clique_decisions':decisions,
            'sparse_vertex_labels':list(labels),'bad_evidence_or_guard_rejections':rejections,
            'positive_core_words':42}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    run(args.work)
