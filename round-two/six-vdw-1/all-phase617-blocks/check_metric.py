"""Actual observation classes and exact Hamming-distance identity.

For any binary word c, distance to the unrestricted row-table family is the
sum over observed classes of min(number of zeros, number of ones). Roots are
singletons. Ordinary independent class minimization proves this identity.
"""
from collections import Counter,defaultdict
import hashlib
import json
import struct
from check_all_domains import gauss_keys


def need(ok,message):
    if not ok:
        raise ValueError(message)


def classes():
    keys=gauss_keys();groups=defaultdict(list)
    roots=[n for n in range(3704) if n%617 in (0,1,4,16)]
    root_index={n:i for i,n in enumerate(roots)}
    tags=[]
    for n in range(3704):
        if n in root_index:
            label=('root',n);tag=577+root_index[n]
        else:
            label=('regular',n//617,n%6,keys[n%617])
            tag=1+96*label[1]+6*label[3]+label[2]
        groups[label].append(n);tags.append(tag)
    need(len(groups)==596 and len(roots)==26,'every observed independent row entry and root')
    need(sorted(n for group in groups.values() for n in group)==list(range(3704)),
         'entire disjoint actual observation partition')
    regular={label:points for label,points in groups.items() if label[0]=='regular'}
    need(len(regular)==570 and sum(map(len,regular.values()))==3678,'all regular positions and table classes')
    pairs=[]
    for label in sorted(groups):
        group=groups[label]
        pairs.extend((group[0],n) for n in group[1:])
    need(len(pairs)==3108,'independent equality-star rank on every actual coordinate')
    digest=hashlib.sha256()
    for u,v in pairs:
        digest.update(struct.pack('<HH',u,v))
    record={'all_actual_positions':3704,'actual_observation_classes':596,'regular_classes':570,
            'regular_positions':3678,'independent_root_singletons':26,'equality_star_rank':3108,
            'class_size_histogram':dict(sorted(Counter(map(len,groups.values())).items())),
            'raw_family_word_count':'2^596','whole_position_tag_sha256':hashlib.sha256(struct.pack('<3704H',*tags)).hexdigest(),
            'whole_equality_star_pair_sha256':digest.hexdigest()}
    return groups,tags,pairs,record


def distance(word,groups):
    need(type(word) is list and len(word)==3704 and all(type(x) is int and x in (0,1) for x in word),
         'entire actual binary word, with integer colors only')
    total=0
    for points in groups.values():
        ones=sum(word[n] for n in points)
        total+=min(ones,len(points)-ones)
    return total


def check():
    groups,tags,pairs,record=classes()
    need(record['whole_position_tag_sha256']=='e180a6ef50ce8315516b99a3d49050b0734212b94241173ab899cee0b6d9e1b5',
         'independent tuple-class geometry matches entire actual compact-proof map')
    baseline=[0]*3704;need(distance(baseline,groups)==0,'constant-class baseline')
    selected=[p for label,p in groups.items() if label[0]=='regular' and len(p)>=2][:2]
    need(len(selected)==2,'two independent nontrivial actual regular classes')
    word=baseline[:];word[selected[0][0]]=1;need(distance(word,groups)==1,'one actual regular exception')
    word[selected[1][0]]=1;need(distance(word,groups)==2,'two exceptions in independent classes')
    word=baseline[:]
    for n in selected[0]:word[n]=1
    need(distance(word,groups)==0,'changing a whole table class remains in the family')
    word=baseline[:]
    for label,p in groups.items():
        if label[0]=='root':word[p[0]]=1
    need(distance(word,groups)==0,'independent pole changes absorbed without regular exception')
    rejected=0
    for bad in [baseline[:-1],[True]+baseline[1:],[2]+baseline[1:]]:
        try:distance(bad,groups)
        except ValueError:rejected+=1
        else:raise ValueError('malformed binary word accepted')
    return {'author':'six-vdw-1','role':'researcher',
            'status':'ACTUAL_CLASS_PARTITION_AND_DISTANCE_FORMULA_GEOMETRY_CHECKED',
            **record,'real_geometry_controls':5,'malformed_word_controls':rejected,
            'ordinary_independent_class_minimization_formalized':False,
            'AP_free_word_distance_at_least_one_requires_separate_exact_refutation':True,
            'radius_one_family_excluded':False,'radius_one_native_started':False,'new_W_bound':False}


if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True))
