import hashlib
import json
from collections import Counter
from columns import allocations, occupancy_profiles
from populations import census
from rows import load, require

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def main():
    raw,capped,types = load()
    require((len(raw),len(capped),len(types))==(426,410,51),'literal carrier')
    cases,vectors,hist = census(types)
    residuals = [(case,[(types[i],n) for i,n in enumerate(v) if n],c)
                 for case,v,c in vectors if c['verdict']=='joint_column']
    require(len(residuals)==2 and all(r[0][0]==3 for r in residuals), 'two T3 residuals')
    require(sorted(r[0][5] for r in residuals)==[12,13], 'K12/K13')
    for case,rows,c in residuals:
        require(all(r[1]<=1 and r[10] in (0,r[1],2*r[1]) and r[2]<=1 for r,n in rows),'disjoint-support/heavy roles')
        require(c['exceptional_B']==2,'two actual B centers')
        require(not allocations(case[5]),'joint column obstruction')
    cols={str(k):allocations(k) for k in (12,13,14)}
    require([len(cols[str(k)]) for k in (12,13,14)]==[0,0,18],'column calibration')
    control=((4,4,3,2,1),(1,1,3,0,0),(5,5,6,2,1))
    require(control in cols['14'],'positive K14 abstract allocation')
    profiles=occupancy_profiles()
    record={'raw_marks':len(raw),'capped_marks':len(capped),'types':types,
            'raw_sha256':hashlib.sha256(canonical(raw)).hexdigest(),
            'capped_sha256':hashlib.sha256(canonical(capped)).hexdigest(),
            'cases':[{k:v for k,v in r.items() if k!='states'} for r in cases],
            'case_T_histogram':dict(sorted(Counter(r['case'][0] for r in cases).items())),
            'population_count':len(vectors),'certificates':hist,'residuals':residuals,
            'complete_vectors_sha256':hashlib.sha256(canonical(vectors)).hexdigest(),
            'labelled_columns':cols,'positive_K14':control,'same_owner_profiles':profiles}
    print(json.dumps(record,sort_keys=True))

if __name__=='__main__':
    main()
