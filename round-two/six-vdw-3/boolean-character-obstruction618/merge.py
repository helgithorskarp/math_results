"""Check complete disjoint batch coverage; merge every per-case commitment.

No producer/checker import. This is the finite replay's completion gate.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def combine(cover,controls,batches):
    need(cover['status']=='COMPLETE_PARAMETER_COVER_AND_REPRESENTATIVE_APS','complete cover stage')
    need(controls['status']=='COMPLETE_BOOLEAN_NORMALIZATION_AND_PHASE_CONTROLS','complete controls stage')
    canonical=cover['canonical_states']
    need(len(canonical)==2176 and canonical==sorted(canonical)
        and len({tuple(z) for z in canonical})==2176,'complete unique ordered cover')
    commit=hashlib.sha256();states=APs=points=next_case=0;flips={};gcds={};orbits={'1':{},'2':{},'3':{}}
    for batch in batches:
        need(batch['status']=='COMPLETE_SPECIFIED_POSITIVE_TRANSPORT_BATCH','complete positive transport child')
        need(batch['certificate_sha256']==cover['certificate_sha256']
            and batch['certificate_bytes']==cover['certificate_bytes'],'same whole certificate in every stage')
        first,last=batch['first'],batch['last']
        need(type(first) is int and type(last) is int and first==next_case and first<last<=2176,
            'disjoint contiguous transport ranges')
        cases=batch['case_commitments']
        need(len(cases)==last-first and [z[0] for z in cases]==canonical[first:last],
            'every transported case present in canonical order')
        for state,size,digest in cases:
            need(type(size) is int and size in (1,2,3,6),'positive complete parameter orbit size')
            need(isinstance(digest,str) and len(digest)==64 and all(x in '0123456789abcdef' for x in digest),
                'per-case literal transcript digest')
            commit.update((json.dumps([state,size,digest],separators=(',',':'))+'\n').encode('ascii'))
            k=str(state[0]);h=str(size);orbits[k][h]=orbits[k].get(h,0)+1
        total=sum(z[1] for z in cases)
        need(batch['transported_states']==total and batch['transported_APs']==9*total
            and batch['transported_points']==63*total,'every batch state/AP/point accounted for')
        need(sum(batch['transport_color_flip_state_histogram'].values())==total
            and sum(batch['transported_step_gcd_histogram'].values())==9*total,'complete batch histograms')
        for k,v in batch['transport_color_flip_state_histogram'].items():flips[k]=flips.get(k,0)+v
        for k,v in batch['transported_step_gcd_histogram'].items():gcds[k]=gcds.get(k,0)+v
        states+=total;APs+=9*total;points+=63*total;next_case=last
    need(next_case==2176 and states==12938 and APs==116442 and points==815094,
        'complete2176-case/12938-state transport replay')
    need(orbits==cover['orbit_size_histograms_by_original_root_count'],'entry-level root-count/orbit-size coverage')
    need(controls['certificate_sha256']==cover['certificate_sha256']
        and controls['certificate_bytes']==cover['certificate_bytes'],'same certificate in controls stage')
    return {k:v for k,v in cover.items() if k not in ('status','canonical_states')}|{
        'status':'EXACT_BOOLEAN_THREE_AFFINE_CHARACTER618_REPAIR_AT_LEAST9',
        'transported_states':states,'transported_APs':APs,'transported_points':points,
        'transport_color_flip_state_histogram':flips,'transported_step_gcd_histogram':gcds,
        'transported_case_commitment_root_sha256':commit.hexdigest(),'controls':controls['controls'],
        'transport_commitment_encoding':'SHA256 of ordered newline compact JSON [state,orbit_size,SHA256 of all actual AP event lines for this state]',
        'trust_boundary':'ordinary Boolean folding/normalization/CRT/Burnside/disjointness/lift proof plus exact stdlib finite checker; no imported numerical bound',
        'scope':'arbitrary Boolean rule on three affine F103 character inputs, ALL original roots free; any six-row phase/palette; arbitrary nonperiodic nonroot column edits; cyclic618 or N>=2466; no W bound or optimum'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--parts',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();cover=json.loads((args.parts/'cover.json').read_text());controls=json.loads((args.parts/'controls.json').read_text())
    batches=[json.loads((args.parts/('transport-'+str(first)+'.json')).read_text()) for first in range(0,2176,256)]
    result=combine(cover,controls,batches)
    damages=[]
    def trial(name,change):
        damaged=copy.deepcopy(batches);change(damaged)
        try:combine(cover,controls,damaged)
        except ValueError:damages.append(name)
        else:raise ValueError('damaged merge accepted: '+name)
    trial('missing final range',lambda b:b.pop())
    trial('duplicate range',lambda b:b.__setitem__(1,b[0]))
    trial('gap between ranges',lambda b:b[0].__setitem__('last',255))
    trial('missing transported case',lambda b:b[0]['case_commitments'].pop())
    trial('duplicate transported case',lambda b:b[0]['case_commitments'].__setitem__(1,b[0]['case_commitments'][0]))
    trial('mismatched certificate',lambda b:b[0].__setitem__('certificate_sha256','0'*64))
    trial('incorrect AP total',lambda b:b[0].__setitem__('transported_APs',0))
    trial('malformed transcript digest',lambda b:b[0]['case_commitments'][0].__setitem__(2,'not a digest'))
    need(len(damages)==8,'all merge semantic damages rejected');result['merge_semantic_damage_rejections']=damages
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
