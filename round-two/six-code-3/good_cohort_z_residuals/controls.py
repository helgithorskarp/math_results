"""Semantic certificate damages and actual point/color transport controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import random
from verify import check,domain_and_role,digest,need

def controls(bridge,certificate):
    damages=[]
    def damaged(name,change):
        b,c=copy.deepcopy(bridge),copy.deepcopy(certificate)
        change(b,c)
        try:
            check(b,c)
        except(ValueError,KeyError,TypeError,IndexError):
            damages.append(name)
            return
        raise ValueError('Damaged input accepted: '+name)
    damaged('missing certificate entry',lambda b,c:c['entries'].pop())
    damaged('duplicate certificate index',lambda b,c:c['entries'][-1].update(index=0))
    damaged('boolean certificate index',lambda b,c:c['entries'][0].update(index=False))
    damaged('wrong product attribution',lambda b,c:c['entries'][0].update(product_index=-1))
    damaged('wrong first fixture',lambda b,c:c['entries'][0].update(first_fixture=-1))
    damaged('wrong candidate population',lambda b,c:c['entries'][0].update(candidate_count=0))
    damaged('wrong candidate hash',lambda b,c:c['entries'][0].update(candidate_sha256='0'*64))
    damaged('wrong compatible edge population',lambda b,c:c['entries'][0].update(edges=0))
    damaged('missing color entry',lambda b,c:c['entries'][0]['colors'].pop())
    damaged('boolean color',lambda b,c:c['entries'][0]['colors'].__setitem__(0,False))
    damaged('negative color',lambda b,c:c['entries'][0]['colors'].__setitem__(0,-1))
    damaged('color outside capacity',lambda b,c:c['entries'][0]['colors'].__setitem__(0,1000))
    damaged('boolean capacity',lambda b,c:c['entries'][0].update(capacity=True))
    damaged('unused color class',lambda b,c:c['entries'][0].update(capacity=100))
    damaged('wrong total upper bound',lambda b,c:c['entries'][0].update(upper_bound=0))
    damaged('forged triangle statistic',lambda b,c:c['entries'][0].update(triangle_count=0))
    candidates=domain_and_role(bridge['raw_positive_maps'][0])[1]
    edge=next((i,j) for i,j in itertools.combinations(range(len(candidates)),2) if len(candidates[i]&candidates[j])<=2)
    def improper(b,c):
        i,j=edge
        c['entries'][0]['colors'][j]=c['entries'][0]['colors'][i]
    damaged('actual compatible edge shares a color',improper)
    damaged('missing raw interface',lambda b,c:b['raw_positive_maps'].pop())
    damaged('duplicate actual relative map',lambda b,c:b['raw_positive_maps'].__setitem__(1,copy.deepcopy(b['raw_positive_maps'][0])))
    damaged('repeated point image',lambda b,c:b['raw_positive_maps'][0]['point_map'].__setitem__(0,b['raw_positive_maps'][0]['point_map'][1]))
    damaged('invalid five-subset mask',lambda b,c:b['raw_positive_maps'][0]['word_masks'].__setitem__(0,1))
    damaged('duplicate core word',lambda b,c:b['raw_positive_maps'][0]['word_masks'].__setitem__(0,b['raw_positive_maps'][0]['word_masks'][1]))
    damaged('invalid marked point',lambda b,c:b['raw_positive_maps'][0]['first'][1].__setitem__(0,17))
    damaged('forged actual triangle list',lambda b,c:b['raw_positive_maps'][0].update(triangle_points=[]))
    reference=check(bridge,certificate)
    summary_keys=('interfaces','total_residual_candidates','total_compatible_edges','maximum_upper_bound',
                  'color_range','upper_bound_census','lambda_xu_subscopes','triangle_uncovered_interfaces','triangle_witnesses')
    for seed in(19,47,101):
        perm=list(range(17))
        random.Random(seed).shuffle(perm)
        perm.append(17)
        b,c=copy.deepcopy(bridge),copy.deepcopy(certificate)
        def image(mask):
            return sum(1<<perm[p] for p in range(18) if mask>>p&1)
        for i,(old,row) in enumerate(zip(bridge['raw_positive_maps'],b['raw_positive_maps'])):
            old_masks=domain_and_role(old)[2]
            assigned={image(m):color for m,color in zip(old_masks,certificate['entries'][i]['colors'])}
            row['first'][1]=[perm[p] for p in row['first'][1]]
            row['point_map']=[perm[p] for p in row['point_map']]
            row['word_masks']=sorted(image(m) for m in row['word_masks'])
            row['triangle_points']=sorted(perm[p] for p in row['triangle_points'])
            new_masks=domain_and_role(row)[2]
            need(set(new_masks)==set(assigned),'transported candidate universe differs')
            c['entries'][i]['candidate_sha256']=digest(new_masks)
            c['entries'][i]['colors']=[assigned[m] for m in new_masks]
        result=check(b,c)
        need(all(result[k]==reference[k] for k in summary_keys),'actual relabelled certificate summary differs')
    return dict(status='PASS_SEMANTIC_DAMAGE_AND_POINT_TRANSPORT_CONTROLS',damages=len(damages),
                damaged_kinds=damages,relabelings=3,transported_interfaces=102)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bridge',required=True)
    parser.add_argument('--certificate',required=True)
    args=parser.parse_args()
    print(json.dumps(controls(json.loads(Path(args.bridge).read_text()),json.loads(Path(args.certificate).read_text())),sort_keys=True))

if __name__=='__main__':
    main()
