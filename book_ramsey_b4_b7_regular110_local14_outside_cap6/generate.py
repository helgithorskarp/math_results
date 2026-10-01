"""Exact seven+five exclusion; actual author six-books-3, researcher.
The row-level caps and double-low cut have written necessity proofs.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import census
import forms

HERE=Path(__file__).resolve().parent


def core_census():
    profiles=[];alignments=[];raw={}
    for config in census.CONFIGURATIONS:
        pairs=config['pairs'];degrees=config['degrees'];count=0;masks=[]
        for mask in census.degree_graphs(degrees,set(pairs)):
            count+=1;matrix,_=census.local_matrix(mask,pairs)
            if all(value>=0 for row in matrix for value in row):masks.append(mask)
        masks.sort();forms.need(len(set(masks))==len(masks),'Duplicate local core')
        group=census.stabilizer(pairs)
        forms.need(len(group)==config['stabilizer'],'Low-pair stabilizer count')
        unseen=set(masks);class_count=0
        while unseen:
            mask=min(unseen);orbit={census.transform(mask,p) for p in group}
            forms.need(orbit<=unseen,'Incomplete or overlapping core orbit')
            unseen-=orbit;class_count+=1
            profiles.append({'index':len(profiles),'intersection':config['intersection'],
                             'pairs':[list(p) for p in pairs],'F_mask':mask,'orbit_size':len(orbit)})
        raw[str(config['intersection'])]=masks
        alignments.append({'intersection':config['intersection'],
            'fixed_degree_graphs':count,'labeled_cores':len(masks),'orbits':class_count,
            'stabilizer_size':len(group),
            'labeled_masks_sha256':hashlib.sha256(json.dumps(masks,separators=(',',':')).encode()).hexdigest()})
    forms.need(len(profiles)==52,'Normalized core count')
    return profiles,alignments,raw


def selected_cases(profile):
    matrix,neighbors=census.local_matrix(profile['F_mask'],profile['pairs'])
    h=list(map(len,neighbors))
    degree0=[3*h[i]+28-24-sum(h[j] for j in neighbors[i]) for i in range(10)]
    large=list(census.row_candidates(matrix,neighbors,7,True))
    small=list(census.row_candidates(matrix,neighbors,5,True))
    for first in large:
        a=[int(i in first) for i in range(10)]
        for second in small:
            b=[int(i in second) for i in range(10)]
            base=[[matrix[i][j]-a[i]*a[j]-b[i]*b[j] for j in range(10)] for i in range(10)]
            if any(x<0 for row in base for x in row):continue
            degrees=[degree0[i]-3*a[i]-b[i] for i in range(10)]
            if any(d<0 or d>sum(base[i])-base[i][i] for i,d in enumerate(degrees)):continue
            forms.need(sum(degrees)==18,'Incident slack sum')
            capacities=[row[:] for row in base]
            if not any(i<2 for i in first):
                bound=1-profile['intersection']
                capacities[0][1]=capacities[1][0]=min(capacities[0][1],bound)
            yield first,second,base,degrees,capacities


def states(degrees,capacities):
    if any(x<0 for row in capacities for x in row):return []
    return sorted(forms.weighted_stars(degrees,capacities))


def residual(base,weights):
    matrix=[row[:] for row in base]
    for i,j,weight in weights:matrix[i][j]-=weight;matrix[j][i]-=weight
    return matrix


def integer_form(vector):
    return (tuple(x*x for x in vector),
            tuple((i,j,2*vector[i]*vector[j]) for i,j in combinations(range(10),2) if vector[i] and vector[j]))


def is_negative(matrix,data):
    diagonal,off=data
    return sum(diagonal[i]*matrix[i][i] for i in range(10))+sum(c*matrix[i][j] for i,j,c in off)<0


def json_bytes(value):
    return (json.dumps(value,separators=(',',':'),sort_keys=True)+'\n').encode()


def compute(progress=None):
    profiles,alignments,raw=core_census();pool=[];global_index={};cert_profiles=[]
    state_hash=hashlib.sha256();pair_hash=hashlib.sha256();total_pairs=0;total_states=0;direct=0
    for profile in profiles:
        vectors=[];encoded=[];case_records=[];last=None
        matrix,neighbors=census.local_matrix(profile['F_mask'],profile['pairs'])
        row_counts={str(size):{stage:dict(sorted(Counter(str(sum(i<2 for i in row))
            for row in census.row_candidates(matrix,neighbors,size,flag)).items()))
            for stage,flag in [('before_AB',False),('after_AB',True)]} for size in (5,6,7,8)}
        for first,second,base,degrees,capacities in selected_cases(profile):
            domain=states(degrees,capacities);total_pairs+=1
            pair_hash.update(json.dumps([profile['index'],first,second],separators=(',',':')).encode()+b'\n')
            if any(x<0 for row in capacities for x in row):direct+=1
            for weights in domain:
                R=residual(base,weights)
                forms.need(all(sum(row)==4*row[i] for i,row in enumerate(R)),'Literal residual row sum')
                found=last is not None and is_negative(R,encoded[last])
                if not found:
                    last=next((i for i,data in enumerate(encoded) if is_negative(R,data)),None)
                    found=last is not None
                if not found:
                    vector=forms.negative_vector(R)
                    forms.need(forms.quadratic(R,vector)<0,'Invalid literal negative form')
                    vectors.append(vector);encoded.append(integer_form(vector));last=len(vectors)-1
                state_hash.update(json.dumps([profile['index'],first,second,weights,R],separators=(',',':')).encode()+b'\n')
            total_states+=len(domain)
            case_records.append([sum(1<<i for i in first),sum(1<<i for i in second),len(domain),
                int(any(x<0 for row in capacities for x in row))])
        references=[]
        for vector in vectors:
            key=tuple(vector)
            if key not in global_index:global_index[key]=len(pool);pool.append(vector)
            references.append(global_index[key])
        cert_profiles.append({'index':profile['index'],'vector_indices':references})
        profile.update({'row_counts':row_counts,'cases':case_records})
        if progress:
            Path(progress).write_text(json.dumps({'complete':False,'completed_profiles':profile['index']+1,
                'states':total_states,'pairs':total_pairs})+'\n')
        print(json.dumps({'completed_profiles':profile['index']+1,'pairs':total_pairs,
                          'states':total_states,'vectors':len(pool)}),flush=True)
    forms.need(total_pairs==861 and total_states==184066,'Author prototype/domain crosscheck')
    forms.need(all(not p['row_counts']['8']['after_AB'] for p in profiles),'Size-eight row survived necessary filter')
    certificate={'agent':'six-books-3','role':'researcher','dimension':10,'vectors':pool,'profiles':cert_profiles}
    summary={'agent':'six-books-3','role':'researcher','complete':True,'conditional_local_histogram':'2^2,3^8',
        'alignments':alignments,'normalized_profiles':len(profiles),'labeled_fixed_alignment_cores':sum(len(v) for v in raw.values()),
        'selected_pairs':total_pairs,'direct_impossible_cut_cases':direct,'residual_matrices':total_states,
        'negative_forms':total_states,'survivors':0,'unique_vectors':len(pool),
        'profile_vector_references':sum(len(p['vector_indices']) for p in cert_profiles),
        'max_absolute_vector_entry':max(abs(x) for vector in pool for x in vector),
        'pair_stream_sha256':pair_hash.hexdigest(),'state_matrix_sha256':state_hash.hexdigest(),
        'negative_vectors_sha256':hashlib.sha256(json_bytes(certificate)).hexdigest(),'profiles':profiles}
    return summary,certificate


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write-certificates',action='store_true')
    parser.add_argument('--progress');args=parser.parse_args();summary,certificate=compute(args.progress)
    for name,value in [('expected.json',summary),('negative_vectors.json',certificate)]:
        data=json_bytes(value)
        if args.write_certificates:(HERE/name).write_bytes(data)
        else:forms.need(data==(HERE/name).read_bytes(),'Regeneration differs: '+name)
    print(json.dumps({k:v for k,v in summary.items() if k!='profiles'},sort_keys=True))
