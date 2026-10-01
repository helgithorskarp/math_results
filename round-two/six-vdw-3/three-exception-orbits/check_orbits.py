#!/usr/bin/env python3
"""Independently expand affine images and compare the full raw ternary domain."""
import argparse
import hashlib
import itertools
import json
import math
import resource
import time
from collections import Counter
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def check(record):
    start=time.monotonic();q=record['q'];rows=record['representatives']
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)), 'Bad prime')
    need(len(rows)<256,'Owner label overflow')
    owners=bytearray(24*q*q*q);counts=[]
    def label(b,mask,points):
        p0,p1,p2=points
        return (((b*8+mask)*q+p0)*q+p1)*q+p2
    for index,row in enumerate(rows,1):
        kind,lam=row['kind'],row['lambda']
        need(kind in ('same','mixed') and 1<lam<q,'Bad representative')
        values=(1,1,1 if kind=='same' else 2);new=0
        for multiplier in range(1,q):
            for shift in range(q):
                image=sorted(((shift%q,values[0]),((shift+multiplier)%q,values[1]),((shift+multiplier*lam)%q,values[2])))
                points=tuple(pair[0] for pair in image)
                mask=sum((value-1)<<position for position,(_,value) in enumerate(image))
                need(len(set(points))==3,'Collapsed field image')
                for background in range(3):
                    for colors in (mask,mask^7):
                        code=label(background,colors,points);previous=owners[code]
                        need(previous in (0,index),'Two proposed representative orbits intersect')
                        if not previous:owners[code]=index;new+=1
        need(new==row['raw_skeleton_orbit_size'],'Declared orbit size is wrong')
        stabilizers=[]
        source={0:values[0],1:values[1],lam:values[2]}
        for multiplier in range(1,q):
            for shift in range(q):
                image={((multiplier*x+shift)%q):value for x,value in source.items()}
                if image==source:stabilizers.append([multiplier,shift])
        need(len(stabilizers)==row['skeleton_stabilizer_order'],'Declared stabilizer differs')
        counts.append({'kind':kind,'lambda':lam,'raw_orbit_size':new,'field_stabilizer':stabilizers})
    raw=0
    for points in itertools.combinations(range(q),3):
        for background in range(3):
            for mask in range(8):
                need(owners[label(background,mask,points)]!=0,'An actual raw skeleton has no representative')
                raw+=1
    nonzero=sum(value!=0 for value in owners)
    need(raw==nonzero==sum(c['raw_orbit_size'] for c in counts)==4*q*(q-1)*(q-2),'Raw domain/union mismatch')
    need(record['representative_count']==len(rows) and record['raw_skeleton_count']==raw,'Manifest count mismatch')
    need(record['orientation_bits_per_representative']==q and record['global_complement_normalized_free_bits']==q-1 and not record['orientation_invariance_imposed'],'Orientation coverage narrowed')
    f=lambda z:int(z%6>=3)
    identities=0
    for alpha in (1,5):
        for beta in range(6):
            for phi in range(6):
                target=(pow(alpha,-1,6)*(phi-beta)+(0 if alpha==1 else 4))%6
                # f(alpha*y+beta-phi) = f(y-target), including all carries.
                for y in range(6):
                    need(f(alpha*y+beta-phi)==f(y-target),'Six-state carry identity failed')
                    identities+=1
    return {'q':q,'status':'COMPLETE_RAW_THREE_EXCEPTION_ORBIT_COVER_CHECKED',
            'raw_skeletons':raw,'representatives':len(rows),'kind_counts':dict(Counter(row['kind'] for row in rows)),
            'orbits':counts,'full_owner_array_sha256':hashlib.sha256(owners).hexdigest(),
            'phase_affine_full_state_truth_entries':identities,'seconds':time.monotonic()-start,
            'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('manifest',type=Path)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=check(json.loads(args.manifest.read_text()))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key!='orbits'}))

if __name__=='__main__':main()
