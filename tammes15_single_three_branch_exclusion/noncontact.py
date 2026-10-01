"""Exact original-face cover, profile(1,5,0), F-U noncontact.
six-tammes-1, researcher. All15 role allocations, all150 U choices,
paired/unpaired alternatives and original aliases; see PROOF.md.
"""
from itertools import combinations
from collections import Counter
import math
import contact as p
k=p.k
ANCHORS = ('F','U','X','R','S','V','W','B','C')
ENDPOINTS = ('X','S','V','W')
FREE = ('E','G','D')
CORE = (('F','X','R'),('F','R','S'),('F','V','W'),
        ('F','S','B','V'),('F','W','C','X'),
        ('R','L','Q','S'),('R','X','P','L'))

def allocations():
    for n in range(4):
        yield from combinations(ENDPOINTS, n)

def representatives(chosen):
    fixed = ('B','C') + chosen
    free = FREE[:3-len(chosen)]
    deficient = tuple(n for n in ANCHORS + free if n in fixed + free)
    for n in range(len(fixed)+1):
        q = 3-n
        if 0 <= q <= len(free):
            for selected in combinations(fixed,n):
                contacts = selected + free[:q]
                yield tuple(n for n in deficient if n in contacts), math.comb(len(free),q)

def schema(chosen, contacts, stage):
    free = FREE[:3-len(chosen)]
    originals = ANCHORS + free
    ones = ('B','C') + chosen + free
    names, words = originals + ('L','P','Q'), CORE
    if 'X' in chosen:
        names += ('AX',)
        words += (('X','C','AX','P'),)
    else:
        words += (('X','C','P'),)
    if 'S' in chosen:
        names += ('AS',)
        words += (('S','Q','AS','B'),)
    else:
        words += (('S','Q','B'),)
    if stage == 'unpaired':
        if 'V' not in chosen:
            names += ('JV',)
            words += (('V','B','JV'),)
        if 'W' not in chosen:
            names += ('JW',)
            words += (('W','JW','C'),)
    elif stage == 'paired':
        if 'V' in chosen or 'W' in chosen:
            raise RuntimeError('One-T isolated endpoint in paired second T')
        names += ('H','M','N')
        words += (('W','V','H'),('V','B','M','H'),('W','H','N','C'))
        if 'S' in chosen:
            words += (('B','AS','M'),)
        else:
            names += ('JB',)
            words += (('B','Q','JB','M'),)
        if 'X' in chosen:
            words += (('C','N','AX'),)
        else:
            names += ('KC',)
            words += (('C','N','KC','P'),)
    else:
        raise RuntimeError('Unknown original alternative')
    number = {n:i for i,n in enumerate(names)}
    if len(ones) != 5 or len(contacts) != 3 or len(set(contacts)) != 3 or not set(contacts) <= set(ones):
        raise RuntimeError('Wrong deficient-five or U-contact coverage')
    return {'case': 'one_' + (''.join(chosen) or 'outside') + '_U' + ''.join(contacts) + '_' + stage,
            'names':names, 'words':words, 'number':number,
            'faces':tuple(tuple(number[n] for n in w) for w in words),
            'mode':'full', 'maxima':{'F':3}, 'exact':{'F':3,'U':0,**{n:1 for n in ones}},
            'distinct':(), 'initial':tuple(range(len(originals))),
            'contact_edges':tuple((1,number[n]) for n in contacts)}

def ordinary_star(prefix,spec):
    role = k.triangle_role(prefix,spec,'L')
    if role not in (0,1,2):
        raise RuntimeError('Unclassified noncontact fourth R neighbor')
    if role != 2:
        return role,spec
    full = dict(spec, names=spec['names']+('HL',),
                words=spec['words']+(('L','HL','Q'),('L','P','HL')))
    full['number'] = {n:i for i,n in enumerate(full['names'])}
    full['faces'] = tuple(tuple(full['number'][n] for n in w) for w in full['words'])
    return role,full

def controls():
    chosen = ()
    s = schema(chosen,('B','E','G'),'paired')
    if k.necessary(s['initial'],s) is not None:
        raise RuntimeError('Positive F-three-T noncontact star rejected')
    aliases = {}
    for label in (5,6):
        labels = s['initial']+(label,)
        if k.necessary(labels,s) is not None:
            raise RuntimeError('Early original L=V/W alias wrongly excluded')
        aliases['V' if label==5 else 'W'] = labels
    weights = {''.join(x) or 'outside':sum(w for c,w in representatives(x)) for x in allocations()}
    if len(weights) != 15 or set(weights.values()) != {10}:
        raise RuntimeError('Five-one U choice cover has a gap')
    return {'F_three_T_star_positive':True, 'early_L_equal_V_or_W_positive':aliases,
            'all_15_role_allocations_weighted_U_contacts_10_each':weights}

def run():
    cs=controls();trace=[];totals=Counter();terminals=[];weights=Counter()
    def record(stage,spec,initial=None):
        r=k.cover(spec,initial)
        trace.append({'stage':stage,'spec':p.serializable_spec(spec),'initial':initial,'cover':r})
        totals['covers']+=1;totals['nodes']+=r['nodes']
        totals[stage+'_covers']+=1;totals[stage+'_nodes']+=r['nodes']
        totals[stage+'_survivors']+=len(r['survivors'])
        return r
    def recurse(prefix,spec,depth=0):
        if depth>12:raise RuntimeError('INCOMPLETE: fixed12forcingdepth')
        if k.one_T_U_obstruction(prefix,spec):
            totals['one_T_U_cuts']+=1
            return
        forced=k.force_last_face(prefix,spec)
        if forced is None:
            _,_,_,edges,_=k.actual_state(prefix,spec)
            u=sorted(edges.get(1,()))
            pair=next(((x,y) for x,y in combinations(u,2) if y in edges.get(x,())),None)
            if len(u)!=3 or pair is None:raise RuntimeError('A noncontact terminal patch survives')
            totals['U_neighbor_contact_diagonal_cuts']+=1
            terminals.append({'case':spec['case'],'labels':prefix,'U_neighbors':u,'contact_pair':pair})
            return
        for labels in record('forced_last_face',forced[3],prefix)['survivors']:
            recurse(labels,forced[3],depth+1)
    for chosen in allocations():
        for contacts,weight in representatives(chosen):
            for stage in ('unpaired','paired') if not set(chosen)&{'V','W'} else ('unpaired',):
                spec=schema(chosen,contacts,stage);base=record('original_face',spec)
                weights[stage+'_representatives']+=1;weights[stage+'_labelled_cases']+=weight
                for prefix in base['survivors']:
                    if k.one_T_U_obstruction(prefix,spec):
                        totals['early_one_T_U_cuts']+=1
                        continue
                    role,full=ordinary_star(prefix,spec)
                    for labels in record('ordinary_L_star',full,prefix)['survivors']:
                        recurse(labels,full)
    return {'status':'NONCONTACT_CASE_EXCLUDED','controls':cs,'counts':dict(sorted(totals.items())),
            'original_case_cover':dict(sorted(weights.items())),'terminal_obstructions':terminals},trace
