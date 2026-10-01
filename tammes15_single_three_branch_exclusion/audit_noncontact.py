"""Separate noncontact raw-label/role/free-bijection/terminal audit.
No production imports. All labelled U choices audited; same researcher.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib, importlib.util, json
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tammes15_ordinary_five_four_one_exclusion/audit.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != 'f9d4ebbab1316f68e4dffdec8375ad158203c3cf2fd0627d90da68dee019eabb':
    raise RuntimeError('Published8180 auditor changed')
loader = importlib.util.spec_from_file_location('published8180_unoriented', SOURCE)
a = importlib.util.module_from_spec(loader)
loader.loader.exec_module(a)
old_check = a.check
def check(labels,spec,use_orientability=True):
    return len(set(labels)) <= 15 and old_check(labels,spec,use_orientability)
a.check = check
ANCHORS = ('F','U','X','R','S','V','W','B','C')
ENDPOINTS = ('X','S','V','W')
FREE = ('E','G','D')
BASE = (('F','R','X'),('F','S','R'),('F','W','V'),
        ('F','V','B','S'),('F','X','C','W'),
        ('R','S','Q','L'),('R','L','P','X'))

def specification(chosen,contacts,stage):
    free = FREE[:3-len(chosen)]
    originals = ANCHORS+free
    ones = ('B','C')+chosen+free
    names,words = originals+('L','P','Q'),BASE
    if 'X' in chosen:
        names += ('AX',)
        words += (('X','P','AX','C'),)
    else:
        words += (('X','P','C'),)
    if 'S' in chosen:
        names += ('AS',)
        words += (('S','B','AS','Q'),)
    else:
        words += (('S','B','Q'),)
    if stage == 'unpaired':
        if 'V' not in chosen:
            names += ('JV',)
            words += (('V','JV','B'),)
        if 'W' not in chosen:
            names += ('JW',)
            words += (('W','C','JW'),)
    elif stage == 'paired' and not set(chosen)&{'V','W'}:
        names += ('H','M','N')
        words += (('W','H','V'),('V','H','M','B'),('W','C','N','H'))
        if 'S' in chosen:
            words += (('B','M','AS'),)
        else:
            names += ('JB',)
            words += (('B','M','JB','Q'),)
        if 'X' in chosen:
            words += (('C','AX','N'),)
        else:
            names += ('KC',)
            words += (('C','P','KC','N'),)
    else:
        raise RuntimeError('Incorrect second-triangle alternative')
    number = {n:i for i,n in enumerate(names)}
    return {'case':'one_'+(''.join(chosen) or 'outside')+'_U'+''.join(contacts)+'_'+stage,
            'names':names,'words':words,
            'faces':tuple(tuple(number[n] for n in w) for w in words),
            'mode':'full','maxima':{0:3},'exact':{0:3,1:0,**{number[n]:1 for n in ones}},
            'distinct':(),'initial':tuple(range(len(originals))),
            'contact_edges':tuple((1,number[n]) for n in contacts)}

def original_cases():
    cases,renamings = {},[]
    for bits in product((0,1),repeat=4):
        if sum(bits)>3:
            continue
        chosen = tuple(n for n,flag in zip(ENDPOINTS,bits) if flag)
        free = FREE[:3-len(chosen)]
        originals = ANCHORS+free
        ones = tuple(n for n in originals if n in ('B','C')+chosen+free)
        for flags in product((0,1),repeat=5):
            if sum(flags)!=3:
                continue
            contacts = tuple(n for n,flag in zip(ones,flags) if flag)
            selected = tuple(n for n in free if n in contacts)
            remaining = tuple(n for n in free if n not in contacts)
            q = len(selected)
            rename = dict(zip(selected+remaining,free))
            all_names = dict((n,rename.get(n,n)) for n in originals)
            if set(all_names.values()) != set(originals) or len(all_names.values()) != len(set(all_names.values())):
                raise RuntimeError('Outside-name map is not a bijection')
            canonical = tuple(n for n in ones if n in set(all_names[x] for x in contacts))
            if tuple(n for n in free if n in canonical) != free[:q]:
                raise RuntimeError('Outside-name contact representative differs')
            for stage in ('unpaired','paired') if not set(chosen)&{'V','W'} else ('unpaired',):
                spec = specification(chosen,canonical,stage)
                key = spec['case']
                if key not in cases:
                    cases[key] = {'spec':spec,'weight':0}
                cases[key]['weight'] += 1
                original = specification(chosen,contacts,stage)
                if not a.same_words(tuple(tuple(all_names.get(x,x) for x in w) for w in original['words']),spec['words']):
                    raise RuntimeError('Free bijection changes a named original face')
                old_edges={(all_names[original['names'][x]],all_names[original['names'][y]]) for x,y in original['contact_edges']}
                new_edges={(spec['names'][x],spec['names'][y]) for x,y in spec['contact_edges']}
                if old_edges!=new_edges:
                    raise RuntimeError('Free bijection changes an actual U contact')
                old_roles={all_names[original['names'][i]]:t for i,t in original['exact'].items()}
                new_roles={spec['names'][i]:t for i,t in spec['exact'].items()}
                if old_roles!=new_roles:
                    raise RuntimeError('Free bijection changes exact roles')
                renamings.append({'case':key,'from_contacts':contacts,'bijection':all_names})
    if len(cases)!=160 or sum(x['weight'] for x in cases.values())!=190 or len(renamings)!=190:
        raise RuntimeError('Independent full original role/contact cover differs')
    return cases,renamings

def ordinary_star(labels,spec):
    position=spec['names'].index('L')
    role=a.actual_role(labels,spec,labels[position])
    if role not in (0,1,2):
        raise RuntimeError('Unclassified original L')
    if role!=2:
        return role,spec
    return role,a.append_words(spec,('HL',),(('L','Q','HL'),('L','HL','P')))

def run(data,required):
    if hashlib.sha256(data).hexdigest()!='e19a793b2338205fcd5726edd179911d4770efe7c6aeaf2f0e160c9a29da56b8':
        raise RuntimeError('Regenerated component trace changed')
    trace=json.loads(data)
    cases,renamings=original_cases()
    counts=Counter();position=0;terminals=[];reference=None
    def record(stage,spec,initial=None):
        nonlocal position
        entry=trace[position];position+=1;wanted=entry['spec']
        if entry['stage']!=stage or entry['initial']!=(list(initial) if initial is not None else None):
            raise RuntimeError('Branch schedule differs')
        if list(spec['names'])!=wanted['names'] or not a.same_words(spec['words'],wanted['words']):
            raise RuntimeError('Independent reversed original-face schema differs')
        if {spec['names'][i]:t for i,t in spec['exact'].items()}!=wanted['exact']:
            raise RuntimeError('Independent exact triangle roles differ')
        if set(spec['contact_edges'])!=set(map(tuple,wanted['contact_edges'])):
            raise RuntimeError('Actual U contacts differ')
        states,raw,boundaries=a.cover(spec,entry['cover'],spec['initial'] if initial is None else initial)
        counts[stage]+=1;counts['raw_label_assignments']+=raw;counts['entrywise_compared_boundaries']+=boundaries
        return states
    def recurse(labels,spec,depth=0):
        if depth>12:
            raise RuntimeError('INCOMPLETE: fixed12forcingdepth')
        if a.new_U_offenders(labels,spec):
            counts['one_T_U_cuts']+=1
            return
        forced=a.last_face(labels,spec)
        if forced is None:
            corners,neighbors,links,edges=a.cells_and_links(labels,spec)
            u=edges.get(1,set())
            pairs=sorted({tuple(sorted((x,y))) for x in u for y in edges.get(x,set())&u if x!=y})
            if len(u)!=3 or not pairs:
                raise RuntimeError('A terminal partial/closed patch survives')
            counts['U_neighbor_contact_diagonal_cuts']+=1
            terminals.append({'case':spec['case'],'labels':list(labels),'U_neighbors':sorted(u),'contact_pair':list(pairs[0])})
            return
        for survivor in record('forced_last_face',forced[3],labels):
            recurse(survivor,forced[3],depth+1)
    while position<len(trace):
        entry=trace[position]
        if entry['stage']!='original_face' or entry['spec']['case'] not in cases:
            raise RuntimeError('Duplicated, missing, or nonoriginal root case')
        row=cases.pop(entry['spec']['case']);spec=row['spec']
        if spec['case']=='one_outside_UBEG_paired':reference=(spec,entry['cover'])
        states=record('original_face',spec)
        for prefix in states:
            if a.new_U_offenders(prefix,spec):
                counts['early_one_T_U_cuts']+=1
                continue
            role,full=ordinary_star(prefix,spec)
            for labels in record('ordinary_L_star',full,prefix):
                recurse(labels,full)
    if cases:
        raise RuntimeError('Unexamined original role/contact cases')
    if terminals!=required or len(terminals)!=4:
        raise RuntimeError('Independent terminal original-label obstructions differ')
    spec,expected=reference
    one=a.cover(spec,expected,spec['initial'],1)
    two=a.cover(spec,expected,spec['initial'],2)
    if one[0]!=two[0] or len(one[0])!=8:
        raise RuntimeError('Nontrivial raw-block reference differs')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'SEPARATE_SAME_AUTHOR_ALL_BOUNDARIES_AND_FINAL_OBSTRUCTIONS_MATCH',
            'counts':dict(sorted(counts.items())),'full_U_choice_free_bijections':len(renamings),
            'free_bijections_sha256':hashlib.sha256((json.dumps(renamings,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest(),
            'terminal_obstructions':terminals,
            'raw_block_reference':[{'width':1,'raw_tuples':one[1],'boundaries':one[2]},
                                   {'width':2,'raw_tuples':two[1],'boundaries':two[2]}],
            'production_trace_sha256':hashlib.sha256(data).hexdigest(),
            'scope':'Written geometry, original-face and U-neighbor diagonal bridges unformalized; independent mathematical review pending.'}
