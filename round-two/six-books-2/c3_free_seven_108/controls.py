"""Positive baselines, literal two-implementation controls and input damage."""
import copy
import hashlib
import itertools
from pathlib import Path
import random

import blocks
import independent
import verify


def require(condition,message):
    if not condition:
        raise ValueError(message)


def reject(function):
    try:
        function()
    except (ValueError,RuntimeError):
        return
    raise ValueError('damaged input was accepted')


def check(cases):
    spec,labels,kg = blocks.kg_control()
    controls = [spec]
    for number in range(24):
        rng = random.Random(611300+number)
        controls.append(dict(internal=[rng.randrange(2) for _ in range(7)],
            cross=[rng.randrange(8) for _ in range(21)],
            joins=None if number<8 else [rng.randrange(2) for _ in range(7)]))
    assignment = blocks.assignment(spec)
    for variable in range(1,71):
        model = [v if (not assignment[v] if v==variable else assignment[v]) else -v for v in range(1,71)]
        controls.append(blocks.decode_model(model,None))
    spines = 0
    for control in controls:
        rows = blocks.graph(control)
        bits = verify.block_rows(control)
        require(rows==[{v for v in range(len(bits)) if word>>v&1} for word in bits],
                'literal constructors differ')
        require(blocks.literal_summary(rows)==verify.summary(bits),'literal physical spines differ')
        values = blocks.assignment(control)
        require(blocks.decode_model([v if values[v] else -v for v in range(1,71)],control['joins'])==control,
                'edge-orbit codec differs')
        spines += len(rows)*(len(rows)-1)//2
    primary_path = Path(__file__).with_name('primary21.rows')
    primary_bits = verify.read_rows(primary_path)
    primary = verify.summary(primary_bits)
    primary_sets = [{j for j in range(21) if row>>j&1} for row in primary_bits]
    require(primary==blocks.literal_summary(primary_sets),'primary physical spine checks differ')
    require(primary['caps_valid'] and primary['edges']==93,'primary baseline invalid')
    require(primary['degrees_histogram']=={'8':4,'9':16,'10':1},'primary degrees changed')
    require(primary['red_histogram']=={'1':3,'2':33,'3':57},'primary red pages changed')
    require(primary['blue_histogram']=={'4':5,'5':44,'6':68},'primary blue pages changed')
    primary_sha = hashlib.sha256(primary_path.read_bytes()).hexdigest()
    require(primary_sha=='4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec','primary fixture pin')
    # Credited7526: independently evaluate all scalar blue-degree budgets.
    blue_budgets = [d*max((4*d-22)*h-3*h*h for h in range(7))
                    +(5-d)*d*(d-1)+42*(21-d) for d in range(15,22)]
    require(blue_budgets==[-48,-126,-240,-396,-600,-858,-1176],'lower-seven scalar budgets')
    damage_count = 0
    for target,field,value in ((blocks.graph,'cross',[8]+spec['cross'][1:]),
                              (verify.block_rows,'internal',[True]+spec['internal'][1:]),
                              (blocks.graph,'joins',[0]*6),
                              (verify.block_rows,'cross',spec['cross'][:-1])):
        damaged = copy.deepcopy(spec)
        damaged[field] = value
        reject(lambda:target(damaged))
        damage_count += 1
    damaged_rows = primary_bits.copy()
    damaged_rows[0] |= 1
    reject(lambda:verify.summary(damaged_rows))
    damage_count += 1
    damaged_rows = primary_bits.copy()
    damaged_rows[0] ^= 2
    reject(lambda:verify.summary(damaged_rows))
    damage_count += 1
    damaged_cases = []
    damaged_cases.append(cases[:-1])
    damaged = copy.deepcopy(cases); damaged[0]['incidence_representatives'].pop(); damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['incidence_representatives'][0][0][0] ^= 1; damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['incidence_representatives'].append(damaged[0]['incidence_representatives'][0]); damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['code'] = 74; damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['status'] = 'INCOMPLETE'; damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['high_domains'] += 1; damaged_cases.append(damaged)
    damaged = copy.deepcopy(cases); damaged[0]['representatives'] -= 1; damaged_cases.append(damaged)
    for damaged in damaged_cases:
        reject(lambda:independent.check_incidence_input(damaged))
        damage_count += 1
    return dict(literal_controls=len(controls),literal_spines=spines,primary_spines=210,
                damages_rejected=damage_count,primary_sha256=primary_sha,
                primary_edges=primary['edges'],primary_degrees=primary['degrees_histogram'],
                primary_red_pages=primary['red_histogram'],primary_blue_pages=primary['blue_histogram'],
                KG_edges=kg['edges'],KG_red_pages=kg['red_histogram'],KG_blue_pages=kg['blue_histogram'],
                blue_degree_15_to_21_budgets=blue_budgets)
