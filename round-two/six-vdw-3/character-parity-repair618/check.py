#!/usr/bin/env python3
"""Independent literal CRT APs, set-incidence inverse and set-XOR enumeration."""
import argparse
import copy
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


def need(ok,message):
    if not ok:
        raise ValueError(message)


def actual_rows(data):
    need(data['q']==103 and data['period']==618 and data['phase']==[0,0,0,1,1,1]
         and data['seed_actual_AP']=={'start':80,'step':1},'Changed canonical geometry')
    squares={x*x%103 for x in range(1,103)}
    need(len(squares)==51 and 0 not in squares,'Bad exact nonzero square definition')
    bits={x:int(x not in squares) for x in range(1,103)}
    multiplicativity=0
    for x in range(1,103):
        for y in range(1,103):
            need(bits[x*y%103]==bits[x]^bits[y],'Character multiplicativity failed')
            multiplicativity+=1
    rows={};transcript=[]
    for A in range(1,618):
        if A%6!=1 or math.gcd(A,618)!=1:
            continue
        points=[A*(80+j)%618 for j in range(7)]
        columns={point%103 for point in points}
        need(0 not in columns and len(columns)==7,'Bad literal regular support')
        colors={bits[point%103]^int(point%6>=3) for point in points}
        need(len(colors)==1,'Literal actual orbit AP is mixed')
        rows[A%103]=columns
        transcript.append([A,*points,*sorted(columns),next(iter(colors))])
    need(set(rows)==set(range(1,103)),'Incomplete actual CRT unit family')
    need(len({tuple(sorted(s)) for s in rows.values()})==102,'Repeated orbit support')
    need(all(sum(r in s for s in rows.values())==7 for r in range(1,103)),
         'Nonuniform actual incidence degree')
    digest=hashlib.sha256(json.dumps(transcript,separators=(',',':')).encode()).hexdigest()
    return rows,digest,multiplicativity


def inverse_sets(data):
    columns=data['inverse_columns_hex']
    need(len(columns)==102,'Incomplete inverse')
    result=[]
    for word in columns:
        need(type(word) is str and word.startswith('0x'),'Bad inverse word type')
        value=int(word,16)
        need(0<=value<2**102,'Out-of-domain inverse bit')
        result.append({r for r in range(1,103) if value//2**(r-1)%2})
    return result


def check_inverse(data,rows):
    columns=inverse_sets(data);tests=0
    for j,support in enumerate(columns,1):
        for k,row in rows.items():
            need(len(support.intersection(row))%2==int(k==j),
                 'Literal inverse product is not identity')
            tests+=1
    return columns,tests


def summary_check(data,hist,count):
    need(data['parity_input_weights']==[1,3] and data['parity_input_count']==count==171802,
         'Wrong complete parity-excess cover')
    need(min(hist)==35 and hist.get(15,0)==0 and data['minimum_reconstructed_weight']==35,
         'Proposed no15-cover certificate failed')
    need(dict(hist)=={int(k):v for k,v in data['complete_weight_histogram'].items()},
         'Entire producer/checker histograms differ')


def controls(data,rows,hist,count):
    inverse_damages=[]
    r=copy.deepcopy(data);r['inverse_columns_hex'][0]=hex(int(r['inverse_columns_hex'][0],16)^1);inverse_damages.append(r)
    r=copy.deepcopy(data);r['inverse_columns_hex'][0],r['inverse_columns_hex'][1]=r['inverse_columns_hex'][1],r['inverse_columns_hex'][0];inverse_damages.append(r)
    r=copy.deepcopy(data);r['inverse_columns_hex'].pop();inverse_damages.append(r)
    r=copy.deepcopy(data);r['inverse_columns_hex'][0]=hex(2**102);inverse_damages.append(r)
    r=copy.deepcopy(data);r['inverse_columns_hex'][0]='0x-1';inverse_damages.append(r)
    r=copy.deepcopy(data);r['inverse_columns_hex'][0]=True;inverse_damages.append(r)
    for damage in inverse_damages:
        try:
            check_inverse(damage,rows)
        except (ValueError,KeyError,TypeError,IndexError):
            continue
        raise ValueError('Damaged inverse accepted')
    summary_damages=[]
    r=copy.deepcopy(data);r['parity_input_weights']=[1,2];summary_damages.append(r)
    r=copy.deepcopy(data);r['parity_input_count']-=1;summary_damages.append(r)
    r=copy.deepcopy(data);r['minimum_reconstructed_weight']-=1;summary_damages.append(r)
    r=copy.deepcopy(data);key=next(iter(r['complete_weight_histogram']));r['complete_weight_histogram'][key]+=1;summary_damages.append(r)
    for damage in summary_damages:
        try:
            summary_check(damage,hist,count)
        except (ValueError,KeyError,TypeError):
            continue
        raise ValueError('Damaged parity summary accepted')
    return len(inverse_damages)+len(summary_damages)


def verify(path):
    raw=path.read_bytes();data=json.loads(raw)
    rows,geometry,multiplicativity=actual_rows(data)
    inverse,products=check_inverse(data,rows)
    full=set(range(1,103));hist=Counter();count=0
    for a in range(102):
        x=full.symmetric_difference(inverse[a]);hist[len(x)]+=1;count+=1
    # Ordinary sets and literal nested field-index loops independently check
    # the producer's bit Gaussian elimination and bit-XOR/popcount catalogue.
    for a in range(100):
        for b in range(a+1,101):
            pair=full.symmetric_difference(inverse[a]).symmetric_difference(inverse[b])
            for c in range(b+1,102):
                x=pair.symmetric_difference(inverse[c]);hist[len(x)]+=1;count+=1
    summary_check(data,hist,count);damages=controls(data,rows,hist,count)
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_CHARACTER_PARITY_REPAIR16_AUTHOR_CHECKED',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'actual_geometry_transcript_sha256':geometry,'literal_actual_APs':102,
            'literal_actual_AP_points':714,'nonzero_multiplicativity_truth_inputs':multiplicativity,
            'GF2_inverse_product_entries':products,'complete_singleton_parity_inputs':102,
            'complete_triple_parity_inputs':171700,'complete_parity_inputs':count,
            'minimum_reconstructed_weight':min(hist),'weight15_candidates':hist.get(15,0),
            'damaged_certificates_rejected':damages,
            'histogram_sha256':hashlib.sha256(json.dumps(dict(sorted(hist.items())),separators=(',',':')).encode()).hexdigest(),
            'character_regular_column_edit_lower_bound':16,
            'three_hole_distance_if_root_regular':[13,86],
            'three_hole_distance_if_root_hole':[14,86],
            'reference_cut_count_at_most':206,
            'all_original_binary_words_explicitly_enumerated':False,
            'integer_cover_optimum_claimed':False,'repair35_bound_claimed':False,
            'native_solver_invoked':False,'W_bound_improved':False,
            'external_review_claimed':False,'formalized':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path)
    a=p.parse_args();print(json.dumps(verify(a.certificate)))
