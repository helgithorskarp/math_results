"""Independent square-set, ordered-root-pair and literal-progression checker.

No import from the producer. Completeness concerns the stated 404 parameter
states, not all binary colorings or all coloring equivalences.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
from math import gcd
from pathlib import Path

Q=103
M=618
SQUARES={x*x%Q for x in range(1,Q)}
INVERSE={x:next(y for y in range(1,Q) if x*y%Q==1) for x in range(1,Q)}
PAIRS=tuple((i,j) for i in range(3) for j in range(3) if i!=j)
STATES=tuple((t,a,b) for t in range(2,Q) for a in range(2) for b in range(2))
STATE_SET=set(STATES)
PACK=9

def need(ok,message):
    if not ok:raise ValueError(message)

def bit(x):
    x%=Q
    need(x!=0,'character zero is undefined')
    return int(x not in SQUARES)

def majority(a,b,c):
    return a if a==b else c

def field_color(state,x):
    t,a,b=state;x%=Q
    need(x not in (0,1,t),'all three root columns are free')
    return majority(bit(x),bit(x-1)^a,bit(x-t)^b)

def column_map(state,i,j):
    # Map the chosen two SOURCE roots to 0 and 1; choose the unused root
    # directly. This is the inverse coordinate direction of the producer.
    roots=(0,1,state[0]);palettes=(0,state[1],state[2])
    k=next(k for k in range(3) if k!=i and k!=j)
    alpha=INVERSE[(roots[j]-roots[i])%Q]
    beta=(-alpha*roots[i])%Q
    target=((alpha*roots[k]+beta)%Q,palettes[j]^palettes[i],palettes[k]^palettes[i])
    flip=bit(alpha)^palettes[i]
    return target,alpha,beta,flip,(i,j,k)

def partition():
    images={z:{column_map(z,i,j)[0] for i,j in PAIRS} for z in STATES}
    blocks={}
    for z in STATES:
        need(z in images[z] and images[z]<=STATE_SET,'complete closed image domain')
        for other in images[z]:need(images[other]==images[z],'root-pair orbit closure')
        blocks.setdefault(min(images[z]),set()).add(z)
    need(len(blocks)==69,'all69 parameter orbits')
    histogram={}
    for representative,members in blocks.items():
        need(members==images[representative],'entire orbit membership equality')
        histogram[len(members)]=histogram.get(len(members),0)+1
    need(histogram=={6:66,3:2,2:1},'short orbits counted once')
    need(sum(map(len,blocks.values()))==404,'weighted404-state coverage')
    return blocks

def decode(raw):
    try:table=list(csv.reader(io.StringIO(raw.decode('ascii'))))
    except (UnicodeError,csv.Error) as e:raise ValueError('malformed certificate') from e
    header=['index','t','d2','d3']+[v for j in range(1,PACK+1) for v in ('a'+str(j),'step'+str(j))]
    need(bool(table) and table[0]==header,'certificate header')
    need(len(table)==70,'complete69-row certificate')
    rows=[]
    for row in table[1:]:
        need(len(row)==22,'nine actual AP pairs per representative')
        try:integers=[int(x) for x in row]
        except ValueError as e:raise ValueError('noninteger certificate field') from e
        need(all(x==str(n) for x,n in zip(row,integers)),'canonical integer encoding')
        rows.append(integers)
    return rows

def literal_pack(state,pairs):
    need(len(pairs)==PACK,'nine actual progression pairs')
    used=set();records=[]
    for a,d in pairs:
        need(type(a) is int and type(d) is int,'integer progression coordinates')
        need(0<=a<M and 1<=d<=309,'actual start and nonzero short step')
        residues=[(a+k*d)%M for k in range(7)]
        support={n%Q for n in residues}
        need(len(support)==7,'seven distinct field columns')
        need(not support&{0,1,state[0]},'all three roots avoided')
        need(not support&used,'pairwise disjoint column supports')
        colors=[field_color(state,n%Q)^int(n%6 in (3,4,5)) for n in residues]
        need(len(set(colors))==1,'literal monochromatic actual AP')
        first=a if a else M;integers=[first+k*d for k in range(7)]
        need(len(set(integers))==7 and integers[0]>=1 and integers[-1]<=2472,'positive integer AP lift')
        need([n%M for n in integers]==residues,'cyclic/interval residues agree')
        used|=support;records.append([residues,sorted(support),colors,integers])
    need(len(used)==63,'nine disjoint seven-column supports')
    return records

def verify_rows(rows,blocks):
    representatives=sorted(blocks)
    need(len(rows)==69,'complete69-case coverage')
    record=hashlib.sha256();start_zero=0;step_hist={};packs={}
    for index,row in enumerate(rows):
        need(len(row)==22 and all(type(x) is int for x in row),'integer witness row')
        need(row[0]==index,'ordered unique case index')
        state=tuple(row[1:4]);need(state==representatives[index],'complete canonical parameter cover')
        pairs=[tuple(row[4+2*j:6+2*j]) for j in range(PACK)]
        literal=literal_pack(state,pairs);packs[state]=pairs
        for j,((a,d),values) in enumerate(zip(pairs,literal)):
            start_zero+=int(a==0);g=gcd(d,M);step_hist[g]=step_hist.get(g,0)+1
            record.update((json.dumps([index,j,state,a,d,values],separators=(',',':'))+'\n').encode('ascii'))
    return packs,{'representative_APs':621,'representative_points':4347,
        'start_zero_APs':start_zero,'representative_step_gcd_histogram':step_hist,
        'representative_literal_transcript_sha256':record.hexdigest()}

def transport_packs(packs,blocks):
    record=hashlib.sha256();count=0;points=0;flips={};step_hist={}
    for representative in sorted(blocks):
        for target in sorted(blocks[representative]):
            options=[column_map(representative,i,j) for i,j in PAIRS]
            image,alpha,beta,flip,_=next(mapping for mapping in options if mapping[0]==target)
            aa=alpha+Q*((1-alpha)%6);bb=beta+Q*((-beta)%6)
            need(gcd(aa,M)==1 and aa%Q==alpha and aa%6==1,'CRT transport unit')
            need(bb%Q==beta and bb%6==0,'CRT translation preserves phase')
            pairs=[]
            for a,d in packs[representative]:
                newa=(aa*a+bb)%M;newd=aa*d%M
                need(newd!=0,'transport retains a nonconstant cyclic step')
                if newd>309:newa=(newa+6*newd)%M;newd=M-newd
                pairs.append((newa,newd))
                for k in range(7):
                    n=(a+k*d)%M;m=(aa*n+bb)%M
                    need(m%Q==(alpha*(n%Q)+beta)%Q and m%6==n%6,'actual point CRT coordinates')
                    before=field_color(representative,n%Q)^int(n%6 in (3,4,5))
                    after=field_color(target,m%Q)^int(m%6 in (3,4,5))
                    need(after==before^flip,'actual AP color exchange retained')
            literal=literal_pack(target,pairs)
            for j,((a,d),values) in enumerate(zip(pairs,literal)):
                record.update((json.dumps([representative,target,flip,j,a,d,values],separators=(',',':'))+'\n').encode('ascii'))
                g=gcd(d,M);step_hist[g]=step_hist.get(g,0)+1
            flips[flip]=flips.get(flip,0)+1;count+=len(pairs);points+=7*len(pairs)
    need(count==3636 and points==25452,'all404 transported nine-packs checked')
    return {'transported_states':404,'transported_APs':count,'transported_points':points,
        'transport_color_flip_state_histogram':flips,'transported_step_gcd_histogram':step_hist,
        'transported_literal_transcript_sha256':record.hexdigest()}

def controls(blocks):
    need(len(SQUARES)==51 and 3 not in SQUARES,'nonzero square and nonsquare classes')
    multiplication=0
    for a in range(1,Q):
        for b in range(1,Q):
            need(bit(a*b)==bit(a)^bit(b),'character multiplicativity');multiplication+=1
    # Exhaust the exact finite root/palette action and actual color identity.
    fixed={};color_checks=0;composition=0
    for state in STATES:
        source_roots={0,1,state[0]}
        for i,j in PAIRS:
            target,alpha,beta,flip,p=column_map(state,i,j)
            fixed[p]=fixed.get(p,0)+int(target==state)
            need({(alpha*r+beta)%Q for r in source_roots}=={0,1,target[0]},'all roots transported')
            for x in range(Q):
                if x not in source_roots:
                    need(field_color(state,x)==field_color(target,(alpha*x+beta)%Q)^flip,'all regular color identities')
                    color_checks+=1
            for h,k in PAIRS:
                other,_,_,_,q=column_map(target,h,k)
                composite=tuple(p[label] for label in q)
                direct=column_map(state,composite[0],composite[1])[0]
                need(other==direct,'all36 action compositions per state');composition+=1
    need(sorted(fixed.values())==[2,2,2,2,2,404],'Burnside fixed-state count')
    need(sum(fixed.values())==6*len(blocks),'Burnside orbit count')
    need(color_checks==242400 and composition==14544,'complete transport identity domain')
    # Exhaust original ordered distinct-root triples; retain all leading signs
    # by the independent multiplicativity and majority truth controls below.
    triples=0
    for r1 in range(Q):
        for r2 in range(Q):
            if r2==r1:continue
            inverse=INVERSE[(r2-r1)%Q]
            for r3 in range(Q):
                if r3==r1 or r3==r2:continue
                t=(r3-r1)*inverse%Q
                need(t not in (0,1) and (t,0,0) in STATE_SET,'all ordered root triples normalized')
                need(((r2-r1)*t+r1)%Q==r3,'third root inverse coordinate identity');triples+=1
    need(triples==1061106,'all original ordered distinct-root triples')
    joint=0;repeated=0;sign_identity=0
    assignments=[tuple((word>>j)&1 for j in range(3)) for word in range(8)]
    for inputs in assignments:
        signs=[1-2*x for x in inputs]
        need(2*(1-2*majority(*inputs))==sum(signs)-signs[0]*signs[1]*signs[2],'majority sign identity');sign_identity+=1
        for palettes in assignments:
            for output in (0,1):
                original=majority(*(x^d for x,d in zip(inputs,palettes)))^output
                normalized=majority(*(x^d^palettes[0] for x,d in zip(inputs,palettes)))^output^palettes[0]
                need(original==normalized,'joint input palette normalization');joint+=1
    for labels in ((0,0,0),(0,0,1),(0,1,0),(0,1,1)):
        variables=max(labels)+1
        for palettes in assignments:
            for output in (0,1):
                truth=[]
                for word in range(1<<variables):
                    bits=tuple((word>>j)&1 for j in range(variables))
                    truth.append(majority(*(bits[label]^d for label,d in zip(labels,palettes)))^output)
                choices=[(v,p) for v in range(variables) for p in (0,1)
                    if truth==[((word>>v)&1)^p for word in range(1<<variables)]]
                need(len(choices)==1,'every repeated-root rule is one affine character')
                repeated+=len(truth)
    need(joint==128 and repeated==224,'complete Boolean truth controls')
    crt=0
    for s in range(1,Q):
        for r in range(Q):
            alpha=s+Q*((1-s)%6)
            need(gcd(alpha,M)==1,'all original CRT multipliers unit')
            for c in range(6):
                beta=r+Q*((-c-r)%6)
                for n in (0,1,617):
                    image=(alpha*n+beta)%M
                    need(image%Q==(s*(n%Q)+r)%Q and image%6==(n-c)%6,'original field/phase normalization CRT')
                crt+=1
    phase_checks=0;illegal_witnesses=0;legal=[]
    for word in range(64):
        row=tuple((word>>y)&1 for y in range(6));bad=[]
        for y in range(6):
            for delta in range(1,6):
                phase_checks+=1
                if len({row[(y+j*delta)%6] for j in range(7)})==1:bad.append((y,delta))
        if not bad:legal.append(row);continue
        y,delta=next(pair for pair in bad if pair[1] in (2,3));d=Q*delta
        for r in range(Q):
            start=r+Q*((y-r)%6);residues=[(start+j*d)%M for j in range(7)]
            need(all(n%Q==r for n in residues),'illegal phase singleton column')
            need(len({row[n%6] for n in residues})==1,'illegal phase actual AP')
            first=min(n if n else M for n in residues);integers=[first+j*d for j in range(7)]
            need(first<=d and integers[-1]<=2163 and len(set(integers))==7,'illegal phase positive interval AP')
            need(all(n%Q==r for n in integers) and len({row[n%6] for n in integers})==1,'illegal phase interval colors')
            illegal_witnesses+=1
    rotations={tuple(int((y+c)%6>=3) for y in range(6)) for c in range(6)}
    need(len(legal)==6 and set(legal)==rotations,'complete64-row phase classification')
    masks=distances=0
    for holes in range(4):
        for omitted_roots in range(min(3,holes)+1):
            e=holes-omitted_roots;m=100-e;lower=9-e;upper=91;cut=82+e
            need(m-lower==upper and m-2*lower==cut,'distinct-root masked-distance algebra')
            for distance in range(m+1):
                need((lower<=distance<=upper)==(abs(m-2*distance)<=cut),'all integer distance/correlation values')
                distances+=1
            masks+=1
    return {'multiplicativity_inputs':multiplication,'root_pair_maps':2424,
        'regular_color_identity_checks':color_checks,'parameter_action_compositions':composition,
        'fixed_states_by_permutation':{''.join(map(str,k)):v for k,v in sorted(fixed.items())},
        'original_ordered_distinct_root_triples':triples,'joint_palette_truth_inputs':joint,
        'repeated_root_truth_inputs':repeated,'majority_sign_identity_inputs':sign_identity,
        'CRT_phase_parameter_sets':crt,'phase_cycle_inputs':phase_checks,'legal_phase_rows':len(legal),
        'actual_illegal_phase_column_witnesses':illegal_witnesses,
        'zero_to_three_hole_mask_classes':masks,'integer_distance_correlation_values':distances}

def damage_controls(rows,blocks):
    trials=[]
    def add(name,change):
        damaged=copy.deepcopy(rows);change(damaged);trials.append((name,damaged))
    add('missing orbit',lambda r:r.pop())
    add('duplicate index',lambda r:r[1].__setitem__(0,0))
    add('duplicate parameter state',lambda r:r[1].__setitem__(slice(1,4),r[0][1:4]))
    add('root outside field',lambda r:r[0].__setitem__(1,103))
    add('palette outside binary domain',lambda r:r[0].__setitem__(2,2))
    add('missing AP pair',lambda r:r[0].pop())
    add('zero step',lambda r:r[0].__setitem__(5,0))
    add('start outside cyclic range',lambda r:r[0].__setitem__(4,618))
    add('root column used as regular',lambda r:r[0].__setitem__(4,0))
    add('repeated field column',lambda r:r[0].__setitem__(5,103))
    add('disjointness broken',lambda r:r[0].__setitem__(slice(6,8),r[0][4:6]))
    add('step outside short domain',lambda r:r[0].__setitem__(5,410))
    special=next(i for i,row in enumerate(rows) if row[1:4]==[47,0,0])
    add('short orbit counted with wrong representative',lambda r:r[special].__setitem__(1,57))
    state=tuple(rows[0][1:4]);bad=None
    for d in range(1,310):
        for a in range(M):
            residues=[(a+j*d)%M for j in range(7)];support={n%Q for n in residues}
            if len(support)!=7 or support&{0,1,state[0]}:continue
            colors=[field_color(state,n%Q)^int(n%6 in (3,4,5)) for n in residues]
            if len(set(colors))>1:bad=(a,d);break
        if bad:break
    need(bad is not None,'nonmonochromatic damage control found')
    add('literal colors not monochromatic',lambda r:r[0].__setitem__(slice(4,6),bad))
    rejected=[]
    for name,damaged in trials:
        try:verify_rows(damaged,blocks)
        except ValueError:rejected.append(name)
        else:raise ValueError('semantic damage accepted: '+name)
    need(len(rejected)==14,'complete semantic damage controls')
    return rejected

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();raw=args.certificate.read_bytes();rows=decode(raw);blocks=partition()
    packs,representatives=verify_rows(rows,blocks)
    result={'status':'EXACT_MAJORITY618_69_ORBITS_REPAIR_AT_LEAST9','author':'six-vdw-3','role':'researcher',
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),'parameter_states':404,'parameter_orbits':69,
        'orbit_size_histogram':{'2':1,'3':2,'6':66},'packing_per_representative':9,
        **representatives,**transport_packs(packs,blocks),'controls':controls(blocks),
        'semantic_damage_rejections':damage_controls(rows,blocks),
        'trust_boundary':'ordinary normalization/CRT/Burnside/lift proof plus exact stdlib finite checker; repeated-root repair15/16 depends on lemma9659',
        'scope':'three affine character inputs under majority; all roots free; arbitrary phase, palette and nonperiodic column edits; no W bound or repair optimum'}
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
