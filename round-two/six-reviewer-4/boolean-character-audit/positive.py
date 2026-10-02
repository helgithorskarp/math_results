"""Pre-author-access positive AP9 verifier in an independent neutral schema.

Input is a regenerated list of {state:[r,t,w],aps:[[a,d],...]} records.
Producer search success is never inferred; each positive AP is checked.
"""
import argparse,hashlib,json,math,time
from pathlib import Path
from geometry import *

def validate_state(state):
    need(type(state)is list and len(state)==3 and all(type(v)is int for v in state),'typed state triple')
    r,t,w=state;need(r in(1,2,3),'original root count')
    need((r==1 and t==0)or(r==2 and t==1)or(r==3 and 2<=t<103),'distinct original root labels')
    need(0<=w<(1<<(1<<r)) and w%2==0,'complete normalized truth domain')
    return tuple(state)

def validate_pack(state,aps):
    need(type(aps)is list and len(aps)==9,'nine complete AP witnesses')
    used=set();transcript=[]
    for pair in aps:
        need(type(pair)is list and len(pair)==2 and all(type(x)is int for x in pair),'typed AP pair')
        a,d=pair;need(0<=a<618 and 1<=d<=309 and d%103!=0,'nonzero regular-column AP step')
        points=tuple((a+j*d)%618 for j in range(7));columns={n%103 for n in points}
        need(len(set(points))==len(columns)==7,'seven distinct residue/field points')
        need(not columns&set(roots(state)),'AP meets an original free root, including ignored inputs')
        colors=tuple(color(state,n)for n in points)
        need(len(set(colors))==1,'actual complete Boolean/phase monochromaticity')
        need(not used&columns,'positive packing supports overlap')
        used|=columns;transcript.append([list(points),sorted(columns),list(colors)])
    need(len(used)==63,'whole nine-pack disjoint support cardinality')
    return transcript

def verify(certificate,start,end):
    cover=orbit_cover(103);reps=[o[0]for o in cover]
    need(type(certificate)is list and len(certificate)==len(reps),'complete canonical certificate record count')
    for row,expected in zip(certificate,reps):
        need(type(row)is dict and set(row)=={'state','aps'},'exact neutral input schema')
        need(validate_state(row['state'])==expected,'whole sorted representative list')
    need(0<=start<end<=len(reps),'bounded complete case slice')
    repAP=rawAP=repPoints=rawPoints=0;states_checked=0;flips={0:0,1:0};maxend=0;hashes=[];samples=[]
    started=time.monotonic()
    for k in range(start,end):
        need(time.monotonic()-started<20,'fixed20s positive case guard; incomplete certificate')
        representative=reps[k];aps=certificate[k]['aps'];record=validate_pack(representative,aps)
        repAP+=9;repPoints+=63;h=hashlib.sha256();h.update(canonical([k,representative,record]))
        for state in cover[k]:
            A,B,flip=inverse_transport(state,representative)
            need(math.gcd(A,618)==1 and A%6==1 and B%6==0,'CRT unit keeps row phase')
            need({(A*x+B)%103 for x in roots(representative)}==set(roots(state)),'complete free-root transport')
            localused=set();pack=[]
            for a,d in aps:
                oldpoints=[(a+j*d)%618 for j in range(7)]
                actual=[(A*n+B)%618 for n in oldpoints];step=A*d%618
                if step>309:actual.reverse();oldpoints.reverse();step=618-step
                need(0<step<=308 and step%103!=0,'nonzero field short step excludes309')
                support={n%103 for n in actual};need(len(support)==7 and not support&set(roots(state)) and not support&localused,'all-state root avoidance/disjointness')
                localused|=support
                colors=[]
                for old,new in zip(oldpoints,actual):
                    need(new%6==old%6 and new%103==(A*old+B)%103,'every actual transported point coordinate')
                    cc=color(state,new);need(cc==(color(representative,old)^flip),'whole Boolean output-flip identity')
                    colors.append(cc)
                need(len(set(colors))==1,'literal transported monochromatic AP')
                first=actual[0] or 618;integers=[first+j*step for j in range(7)]
                need([n%618 for n in integers]==actual and len(set(integers))==7 and integers[-1]<=2466,'whole positive integer lift')
                maxend=max(maxend,integers[-1]);rawAP+=1;rawPoints+=7
                pack.append([actual,sorted(support),colors,integers])
            need(len(localused)==63,'all-state complete pack support')
            h.update(canonical([state,A,B,flip,pack]));flips[flip]+=1;states_checked+=1
        hashes.append([k,list(representative),len(cover[k]),h.hexdigest()])
        if k in(0,1,2,3,8,9,100,1000,2175):samples.append(certificate[k])
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','schema':1,'case_start':start,'case_end':end,
            'whole_certificate_sha256':hashlib.sha256(canonical(certificate)).hexdigest(),'whole_representatives_sha256':hashlib.sha256(canonical(reps)).hexdigest(),
            'case_transcript_digests':hashes,'representative_APs':repAP,'representative_points':repPoints,
            'all_raw_states':states_checked,'all_transported_APs':rawAP,'all_transported_points':rawPoints,
            'flip_histogram':flips,'maximum_literal_lift_endpoint':maxend,'nine_disjoint_regular_columns_verified':True,'positive_samples':samples}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--start',type=int,required=True);ap.add_argument('--end',type=int,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=verify(json.loads(args.certificate.read_text()),args.start,args.end);raw=canonical(out);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(raw)
    print(json.dumps({'status':'PASS','range':[args.start,args.end],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
if __name__=='__main__':main()
