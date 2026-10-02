#!/usr/bin/env python3
"""Independent actual-cyclic audit of a signed one-satellite pair model."""
import argparse
import hashlib
import itertools
import json
import time
from functools import lru_cache
from pathlib import Path


def need(condition,message):
    if not condition:
        raise ValueError(message)


def parameters(q,case,opposite):
    need(case in (1,2,3),'Bad hole representative')
    if q == 103:
        holes = {1:(5,53,101),2:(5,53,102),3:(5,54,101)}[case]
        local = (0,1,2,3,4,5,6,52,53,54,55,101,102)
        core = tuple(x for x in local if x not in holes)
        need(opposite in core and opposite not in range(5),'Bad regular satellite')
    else:
        need(q in (7,11,13),'Only specified small controls supported')
        holes = (0,1,case+1)
        core = tuple(x for x in range(q) if x not in holes)[:3]
        need(opposite in core[1:],'Bad small fixed-word opposite')
    regular = tuple(x for x in range(q) if x not in holes)
    pairs = tuple(itertools.combinations(regular,2))
    index = {pair:i+1 for i,pair in enumerate(pairs)}
    need(regular[0] in core and opposite != regular[0],'Bad root condition')
    return holes,core,regular,pairs,index


def parse(path,n):
    lines = path.read_text().splitlines()
    need(lines,'Empty DIMACS')
    header = lines[0].split()
    need(len(header) == 4 and header[:2] == ['p','cnf'] and int(header[2]) == n,'Bad pair domain')
    rows = []
    for line in lines[1:]:
        entries = list(map(int,line.split()))
        need(entries and entries[-1] == 0 and 0 not in entries[:-1],'Bad clause terminator')
        row = tuple(sorted(entries[:-1]))
        need(all(0 < abs(x) <= n for x in row),'Literal outside pair domain')
        need(len(set(row)) == len(row) and all(-x not in row for x in row),'Repeated/tautological row')
        rows.append(row)
    need(len(rows) == int(header[3]) and len(set(rows)) == len(rows),'DIMACS count or duplicate mismatch')
    return set(rows)


@lru_cache(maxsize=9)
def cyclic_base(q,case):
    # The common hole family is reconstructed once per audit process. Its
    # immutable clause set is reused only for different signed core units.
    provisional = 6 if q == 103 else tuple(x for x in range(q) if x not in (0,1,case+1))[1]
    holes,_,regular,pairs,index = parameters(q,case,provisional)
    root = regular[0]
    rows = set()
    for x,y in itertools.combinations(regular[1:],2):
        ids = index[(root,x)],index[(root,y)],index[(x,y)]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2:
                rows.add(tuple(sorted(v if b == 0 else -v for v,b in zip(ids,bits))))
    cycle_count = len(rows)
    length = 6*q
    groups = {}
    skipped = retained = same_field = 0
    for step in range(1,length):
        for start in range(length):
            residues = tuple((start+j*step)%length for j in range(7))
            fields = tuple(t%q for t in residues)
            if any(x in holes for x in fields):
                skipped += 1
                continue
            retained += 1
            phase = tuple(int(t%6 >= 3) for t in residues)
            if len(set(fields)) == 1:
                need(len(set(phase)) == 2,'Unexpected constant same-column phase row')
                same_field += 1
                continue
            need(len(set(fields)) == 7,'Repeated nonzero-slope field point')
            if fields[::-1] < fields:
                fields,phase = fields[::-1],phase[::-1]
            words = groups.setdefault(fields,set())
            words.add(phase)
            words.add(tuple(1-x for x in phase))
    forbidden = {word for word in itertools.product((0,1),repeat=7)
                 if len({word[j]^word[j+3] for j in range(4)}) == 1}
    need(len(forbidden) == 16,'Bad literal seven-word relation')
    ladders = set()
    for fields,words in groups.items():
        need(words == forbidden,'Actual cyclic phase words differ from both signed ladders')
        ladder = tuple(sorted(index[tuple(sorted((fields[j],fields[j+3])))] for j in range(4)))
        need(len(set(ladder)) == 4,'Collapsed parity ladder')
        ladders.add(ladder)
        rows.add(ladder)
        rows.add(tuple(sorted(-x for x in ladder)))
    return frozenset(rows),{'root_cycle_clauses':cycle_count,'seven_ladders':len(ladders),
                           'all_actual_cyclic_pairs_checked':length*(length-1),
                           'pairs_skipped_meeting_holes':skipped,'pairs_retained_outside_holes':retained,
                           'tautological_retained_pairs':same_field,'literal_seven_orientation_groups_checked':len(groups)}


def audit(path,q,case,opposite):
    started = time.monotonic()
    holes,core,regular,pairs,index = parameters(q,case,opposite)
    root = regular[0]
    base,details = cyclic_base(q,case)
    fixed = {x:int(x==opposite) for x in core}
    need(fixed[root] == 0 and sum(fixed.values()) == 1,'Wrong fixed-word anchor')
    units = {(index[(root,x)] if fixed[x] else -index[(root,x)],) for x in core if x != root}
    expected = set(base)|units
    actual = parse(path,len(pairs))
    need(actual == expected,'Exact actual-cyclic/signed-core model mismatch')
    need(all(len(row) in (1,3,4) for row in expected),'Unexpected ascent or counter clause')
    return {'q':q,'case':case,'holes':list(holes),'regular_core':list(core),'opposite_satellite':opposite,
            'fixed_core_bits':[[x,fixed[x]] for x in core],'regular_columns':list(regular),
            'root':root,'variables':len(pairs),'fixed_core_units':len(units),'positive_core_units':1,
            'clauses':len(expected),'other_regular_bits_free':len(regular)-len(core),
            'counter_variables':0,'weight_cap':None,'no_five_assumption':False,'no_six_assumption':False,
            'extra_growth_cuts':0,'orientation_anchor':'u(root)=0 by global color exchange; no root unit',
            'hypothesis':'one specified regular core satellite has color one; all other regular core points have color zero',
            'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**details,'seconds':time.monotonic()-started}


def literal(q,case,opposite,bits):
    holes,core,regular,_,_ = parameters(q,case,opposite)
    need(len(bits) == len(regular) and all(x in (0,1) for x in bits),'Bad decoded orientation')
    values = dict(zip(regular,bits))
    if any(values[x] != int(x==opposite) for x in core):
        return False,{'failure':'Wrong fixed core word'}
    length = 6*q
    colors = [None if t%q in holes else values[t%q]^int(t%6 >= 3) for t in range(length)]
    checked = skipped = 0
    for step in range(1,length):
        for start in range(length):
            row = [colors[(start+j*step)%length] for j in range(7)]
            if None in row:
                skipped += 1
                continue
            checked += 1
            if len(set(row)) == 1:
                return False,{'failure':'Cyclic seven AP','start':start,'step':step}
    return True,{'outside_seven_pairs_checked':checked,'seven_pairs_skipped':skipped}


def small(path,q,case,opposite):
    need(q in (7,11,13),'Exhaustive controls restricted to q7/11/13')
    _,_,regular,pairs,_ = parameters(q,case,opposite)
    rows = parse(path,len(pairs))
    positives = []
    inputs = 0
    for tail in itertools.product((0,1),repeat=len(regular)-1):
        word = (0,)+tail
        values = dict(zip(regular,word))
        parities = [values[x]^values[y] for x,y in pairs]
        encoded = all(any(parities[abs(x)-1] == int(x>0) for x in row) for row in rows)
        direct,_ = literal(q,case,opposite,word)
        need(encoded == direct,'Small signed-word pair model differs from literal cyclic condition')
        if direct:
            positives.append(''.join(map(str,word)))
        inputs += 1
    return {'q':q,'case':case,'opposite':opposite,'anchored_inputs':inputs,'valid_partial_words':len(positives),
            'positive_fixtures':positives[:3],
            'all_positive_words_sha256':hashlib.sha256(('\n'.join(positives)+'\n').encode()).hexdigest()}


def witness(path,q,case,opposite):
    holes,core,regular,pairs,index = parameters(q,case,opposite)
    assignment = json.loads(path.read_text())
    need(isinstance(assignment,list) and len(assignment) == len(pairs) and all(type(x) is int and x != 0 for x in assignment),'Malformed pair assignment')
    values = {abs(x):int(x>0) for x in assignment}
    need(set(values) == set(range(1,len(pairs)+1)),'Missing or duplicate pair variable')
    word = {regular[0]:0}
    for x in regular[1:]:
        word[x] = values[index[(regular[0],x)]]
    need(all(values[index[(x,y)]] == word[x]^word[y] for x,y in pairs),'Inconsistent pair cycle')
    valid,counts = literal(q,case,opposite,tuple(word[x] for x in regular))
    need(valid,'Literal outside-cyclic witness rejected: '+str(counts))
    return {'q':q,'case':case,'holes':list(holes),'regular_core':list(core),'opposite':opposite,
            'orientation':''.join(str(word[x]) for x in regular),'regular_point_order':list(regular),
            'outside_cyclic_AP_free':True,'full_coloring_AP_free':False,**counts}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('path',type=Path)
    p.add_argument('--q',type=int,default=103)
    p.add_argument('--case',type=int,required=True)
    p.add_argument('--opposite',type=int,required=True)
    group = p.add_mutually_exclusive_group()
    group.add_argument('--small',action='store_true')
    group.add_argument('--witness',action='store_true')
    a = p.parse_args()
    operation = small if a.small else witness if a.witness else audit
    print(json.dumps(operation(a.path,a.q,a.case,a.opposite)))
