"""Actual positive tiny row-cut cores and meaningful full-model damages."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('new_cut_'+name,Path(__file__).resolve().parent/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def main(model,part):
    support=load('support');require=support.require;audit=load('audit').audit
    source=json.loads(model.read_text());forbidden=set(source['forbidden_masks'])
    require(len(forbidden)==160,'whole proved class')
    if part=='tiny':
        # q3 has two independent phase rows: actual regular APs stay in one field row.
        d,certs,r=support.load('controls').small(3,10,7,[1],34,only_fixed_cylinder=True)
        require(r['inputs']==1024 and r['positives']==580,'all original fixed-row cylinder truth inputs')
        cuts=[[ -(10*g+j+1) if(m>>j)&1 else 10*g+j+1 for j in range(10)] for g in range(2) for m in sorted(forbidden)]
        positive=0;retained=[]
        checker=support.load('check_partial').check_word
        for assign,word in certs:
            ones={v for v in assign if v>0};m=sum(2**j for j in range(10) if 11+j in ones)
            encoded=all(any((abs(v) in ones)==(v>0) for v in c) for c in cuts)
            require(encoded==(m not in forbidden),'original phase input/entire necessary-cut clause equivalence')
            if encoded:
                checker(d,assign,word,target=False)
                retained.append((assign,word));positive+=1
        require(positive==420 and len(cuts)==320,'genuine positive actual tiny row-cut cores')
        first_truths=0
        for rep in support.REPS:
            units=[[j+1 if(rep>>j)&1 else -(j+1)] for j in range(10)]
            for raw in range(1024):
                require(all(((raw>>(abs(c[0])-1))&1)==int(c[0]>0) for c in units)==(raw==rep),'all original first masks in six-case cylinders')
                first_truths+=1
        return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_NEW_H3_CUT_TINY_CONTROLS',
                'tiny_original_inputs':1024,'tiny_original_AP_positives':580,'tiny_true_cut_positives':positive,
                'tiny_point_identities':r['point_identities'],'tiny_cut_clauses':320,
                'six_absolute_first_row_truths':first_truths,
                'scope':'Actual positive tiny voluntary row-cut cores and all6 absolute unit cylinders; not H3 production feasibility.'}
    damaged=[]
    x=copy.deepcopy(source);x['base_model']['fixed_first_coset_row']=16;damaged.append(x)
    x=copy.deepcopy(source);x['cut_premise']['artifact_ref']='wrong';damaged.append(x)
    x=copy.deepcopy(source);x['variables']=True;damaged.append(x)
    x=copy.deepcopy(source);x['forbidden_masks'][0]=float(x['forbidden_masks'][0]);damaged.append(x)
    x=copy.deepcopy(source);x['necessary_cut_clauses'][0][0]=True;damaged.append(x)
    x=copy.deepcopy(source);x['necessary_cut_clauses'].pop();damaged.append(x)
    x=copy.deepcopy(source);x['necessary_cut_clauses'][0][0]=101;damaged.append(x)
    x=copy.deepcopy(source);x['scope']='all regular cores';damaged.append(x)
    x=copy.deepcopy(source);old=x['necessary_cut_clauses'][0][:];x['necessary_cut_clauses'][0][0]*=-1
    x['clauses'].remove(old);x['clauses'].append(x['necessary_cut_clauses'][0][:]);x['clauses'].sort();damaged.append(x)
    x=copy.deepcopy(source);i=next(i for i,c in enumerate(x['base_model']['clauses']) if len(c)>1)
    removed=x['base_model']['clauses'].pop(i);x['base_model']['distinct_AP_clauses']-=1;x['clauses'].remove(removed);damaged.append(x)
    x=copy.deepcopy(source);x['clauses'].append([11]);x['clauses'].sort();damaged.append(x)
    require(part in ['damages-first','damages-second'],'explicit production control domain')
    damaged=damaged[:6] if part=='damages-first' else damaged[6:]
    rejected=0
    for x in damaged:
        try:audit(x,34)
        except (ValueError,KeyError,TypeError,StopIteration):rejected+=1
        else:raise ValueError('semantic production damage accepted')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_NEW_H3_CUT_PRODUCTION_DAMAGE_CONTROLS',
            'production_damages_rejected':rejected,
            'scope':'Listed meaningful production definition/cut damages reject; no new exclusion/W bound.'}



if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('part',choices=['tiny','damages-first','damages-second']);a=p.parse_args()
    print(json.dumps(main(a.model,a.part),sort_keys=True),flush=True)
