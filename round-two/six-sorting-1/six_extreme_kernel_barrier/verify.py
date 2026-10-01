"""Standalone numeric-rank scalar audit of selected original clampings.

Imports no producer, profile, sibling checker, search, or solver. Only the
selected lower potential is a proof premise: no complete-family upper envelope
or claim of maximality is accepted from the generator.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
FIXTURE_SHA256='35c3a7cfa9973cce369f40590ad72335325acba41d7276c26b84c7a58843d27c'
GATE_EVALUATIONS=0


def need(condition,message):
    if not condition:
        raise ValueError(message)


def pinned_fixture(data):
    need(hashlib.sha256(data).hexdigest()==FIXTURE_SHA256,'fixture pin differs')
    fixture=json.loads(data)
    need(fixture['n']==13 and fixture['kernel_id']==0,'wrong literal instance')
    need(fixture['kernel']==[[5,6],[7,8],[9,10],[6,8],[10,11],[8,11]],'wrong kernel')
    need(fixture['forced_word']==[[11,12],[1,2]],'wrong forced word')
    need(fixture['native_prefix24']==fixture['known46'][:24],'native fixture differs')
    need(fixture['prefix']==fixture['native_prefix24']+fixture['forced_word']+fixture['kernel'],
         'literal prefix components differ')
    need(len(fixture['prefix'])==32 and len(fixture['known45'])==45 and len(fixture['known46'])==46,
         'wrong word sizes')
    for word in (fixture['prefix'],fixture['known45'],fixture['known46']):
        need(all(type(a)==int and type(b)==int and 0<=a<b<13 for a,b in word),'invalid gate')
    ids=[0,2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,25,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42]
    need(fixture['parent_remaining_nine_wire_ids']==ids,'parent frontier differs')
    need(fixture['remaining_nine_wire_ids']==ids[1:],'new frontier differs')
    return fixture


def marked(value):
    return value<0 or value>1


def ports(row):
    return (sum(2**p for p,value in enumerate(row) if value<0),
            sum(2**p for p,value in enumerate(row) if value>1))


def scalar_record(gates,low,high):
    global GATE_EVALUATIONS
    need(type(low)==int and type(high)==int and 0<=low<8192 and 0<=high<8192,'invalid original masks')
    need(not low&high and low.bit_count()==3 and high.bit_count()==3,'wrong original clamping')
    lows=[p for p in range(13) if low>>p&1]
    highs=[p for p in range(13) if high>>p&1]
    free=[p for p in range(13) if p not in lows+highs]
    need(len(free)==7,'wrong free-input cube')
    template=[0]*13
    for j,p in enumerate(lows):template[p]=j-3
    for j,p in enumerate(highs):template[p]=j+2
    touch=final_ports=None
    activity=0
    for assignment in range(128):
        row=list(template)
        for j,p in enumerate(free):row[p]=(assignment>>j)&1
        this_touch=0
        for t,(a,b) in enumerate(gates):
            hit=marked(row[a]) or marked(row[b])
            if hit:this_touch+=2**t
            if row[a]>row[b]:
                if not hit:activity|=2**t
                row[a],row[b]=row[b],row[a]
        if touch is None:touch,final_ports=this_touch,ports(row)
        need(this_touch==touch and ports(row)==final_ports,'marker trajectory depends on free input')
        GATE_EVALUATIONS+=len(gates)
    redundant=(2**len(gates)-1)&~(touch|activity)
    return {'original_low_mask':low,'original_high_mask':high,
            'current_low_mask':final_ports[0],'current_high_mask':final_ports[1],
            'marked_touch_mask':touch,'redundancy_mask':redundant,
            'D':touch.bit_count(),'R':redundant.bit_count(),
            'C':touch.bit_count()+redundant.bit_count()}


def reconstructed(fixture,candidate):
    rows=[]
    for witness in candidate['witnesses']:
        rows.append(scalar_record(fixture['prefix'],witness['original_low_mask'],witness['original_high_mask']))
    realized=[(row['current_low_mask'],row['current_high_mask']) for row in rows]
    need(len(rows)==18 and len(set(realized))==18 and realized==sorted(realized),
         'selected configurations repeated, missing, or unsorted')
    need(set(realized)=={(lo,hi) for lo in (7,11,19) for hi in (6176,6208,6272,6400,6656,7168)},
         'selected configuration grid differs')
    mass=sum(2**row['C'] for row in rows)
    need(mass==281018368 and mass>2**28,'strict lower-witness obstruction absent')
    # Small-size input S(7)>=16 and general semantic lemma8539 are mathematical
    # dependencies. This checker proves the concrete finite premises only.
    return {'schema':'native-kernel-zero-six-extreme-lower-witnesses-v1',
            'agent':'six-sorting-1','role':'researcher','fixture_sha256':FIXTURE_SHA256,
            'n':13,'kernel_id':0,'prefix_size':32,'l':3,'h':3,'free_inputs':7,
            'small_size_lower_bound':16,'size_budget':44,'witnesses':rows,
            'witness_lower_mass':mass,'cap':2**28,'minimum_sorter_total':45,
            'remaining_nine_wire_ids':fixture['remaining_nine_wire_ids']}


def match(candidate,expected):
    need(candidate==expected,'complete reconstructed certificate differs')


def full_boolean_control(n,gates):
    global GATE_EVALUATIONS
    for x in range(2**n):
        row=[(x>>p)&1 for p in range(n)]
        original=list(row)
        for a,b in gates:
            if row[a]>row[b]:row[a],row[b]=row[b],row[a]
        need(row==sorted(original),'known positive sorter fails')
        GATE_EVALUATIONS+=len(gates)


def main():
    begin=time.monotonic()
    fixture=pinned_fixture((ROOT/'fixture.json').read_bytes())
    data=(ROOT/'certificate.json').read_bytes()
    candidate=json.loads(data)
    expected=reconstructed(fixture,candidate)
    match(candidate,expected)
    full_boolean_control(13,fixture['known45'])
    full_boolean_control(13,fixture['known46'])
    sorter7=[[0,6],[2,3],[4,5],[0,2],[1,4],[3,6],[0,1],[2,5],
             [3,4],[1,2],[4,6],[2,3],[4,5],[1,2],[3,4],[5,6]]
    full_boolean_control(7,sorter7)
    positive_masses=[]
    for name in ('known45','known46'):
        envelope={}
        for row in expected['witnesses']:
            actual=scalar_record(fixture[name],row['original_low_mask'],row['original_high_mask'])
            key=(actual['current_low_mask'],actual['current_high_mask'])
            envelope[key]=max(envelope.get(key,0),actual['C'])
        mass=sum(2**c for c in envelope.values())
        need(set(envelope)=={(7,7168)} and mass<=2**(len(fixture[name])-16),
             'lower-witness method rejects known positive sorter')
        positive_masses.append(mass)
    damaged=[deepcopy(candidate) for _ in range(5)]
    damaged[0]['witnesses'][0]['D']-=1
    damaged[1]['witnesses'][1]['redundancy_mask']^=1
    damaged[2]['witnesses'][2]=deepcopy(damaged[2]['witnesses'][1])
    damaged[3]['witness_lower_mass']-=1
    damaged[4]['remaining_nine_wire_ids'].pop()
    for item in damaged:
        try:match(item,expected)
        except ValueError:pass
        else:raise ValueError('damaged certificate accepted')
    try:pinned_fixture((ROOT/'fixture.json').read_bytes()+b' ')
    except ValueError:pass
    else:raise ValueError('damaged fixture pin accepted')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'ALL_SIX_EXTREME_KERNEL_LOWER_WITNESS_CHECKS_PASSED',
                      'kernel_id':0,'selected_original_domains':18,
                      'proof_original_free_assignments':18*128,
                      'positive_clamping_free_assignments':36*128,
                      'full_boolean_control_inputs':16384,'seven_wire_positive_inputs':128,
                      'scalar_gate_evaluations':GATE_EVALUATIONS,
                      'witness_lower_mass':expected['witness_lower_mass'],'cap':2**28,
                      'minimum_sorter_total':45,'remaining_targets':32,
                      'positive_control_masses':positive_masses,'corruptions_rejected':6,
                      'certificate_sha256':hashlib.sha256(data).hexdigest(),
                      'seconds':time.monotonic()-begin,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
