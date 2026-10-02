"""Independent ordered-root-pair, square-set and literal AP checker.

No import from the producer, no solver, no truth table evaluated at zero.
All original roots remain free even when the function ignores an input.
The 2176 classes are for a specified parameter action, not all colorings.
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
PACK=9
SQUARES={x*x%Q for x in range(1,Q)}
INV={x:next(y for y in range(1,Q) if x*y%Q==1) for x in range(1,Q)}
ORDERS={1:((0,),),2:((0,1),(1,0)),
    3:tuple((i,j,next(h for h in range(3) if h!=i and h!=j))
        for i in range(3) for j in range(3) if i!=j)}
STATES=tuple([(1,0,w) for w in (0,2)]+[(2,0,w) for w in range(0,16,2)]
    +[(3,t,w) for t in range(2,Q) for w in range(0,256,2)])
DOMAIN=set(STATES)
# Decode by division and explicit square membership; the producer uses
# Euler powers and packed bit rotations. Character tuples precede F.
TABLES={(k,w):tuple(w//(2**i)%2 for i in range(2**k))
    for k in (1,2,3) for w in range(0,2**(2**k),2)}

def need(ok,message):
    if not ok:raise ValueError(message)

def bit(x):
    x%=Q
    need(x!=0,'character zero is undefined')
    return int(x not in SQUARES)

def roots(state):
    k,t,_=state
    need(k in (1,2,3),'one through three original roots')
    return (0,) if k==1 else ((0,1) if k==2 else (0,1,t))

def bits_at(labels,x):
    need(x not in labels,'every original root is free, including ignored inputs')
    return tuple(bit(x-r) for r in labels)

PATTERNS={labels:tuple(None if x in labels else bits_at(labels,x) for x in range(Q))
    for labels in [(0,),(0,1)]+[(0,1,t) for t in range(2,Q)]}

def field_color(state,x):
    labels=roots(state);values=PATTERNS[labels][x%Q]
    need(values is not None,'no field truth value assigned at an original root')
    assignment=sum(v*2**i for i,v in enumerate(values))
    return TABLES[state[0],state[2]][assignment]

def column_map(state,order):
    # Inverse coordinate direction: send two SOURCE roots to 0 and 1.
    # Old truth values are explicitly tabulated on new abstract arguments.
    k,t,w=state;labels=roots(state)
    if k==1:return state,1,0,0
    i,j=order[:2];alpha=INV[(labels[j]-labels[i])%Q]
    beta=-alpha*labels[i]%Q
    target_t=(alpha*labels[order[2]]+beta)%Q if k==3 else 0
    toggle=bit(alpha);changed=[]
    for argument in range(2**k):
        new=tuple(argument//(2**h)%2 for h in range(k))
        old=[0]*k
        for h,label in enumerate(order):old[label]=new[h]^toggle
        old_argument=sum(v*2**h for h,v in enumerate(old))
        changed.append(TABLES[k,w][old_argument])
    flip=changed[0]
    target_w=sum((v^flip)*2**h for h,v in enumerate(changed))
    return (k,target_t,target_w),alpha,beta,flip

def partition():
    maps={(z,p):column_map(z,p) for z in STATES for p in ORDERS[z[0]]}
    images={z:{maps[z,p][0] for p in ORDERS[z[0]]} for z in STATES}
    blocks={}
    for z in STATES:
        need(z in images[z] and images[z]<=DOMAIN,'complete closed normalized domain')
        for other in images[z]:need(images[other]==images[z],'ordered-root-pair orbit closure')
        blocks.setdefault(min(images[z]),set()).add(z)
    hist={1:{},2:{},3:{}}
    for representative,members in blocks.items():
        need(members==images[representative],'entire orbit membership equality')
        k=representative[0];hist[k][len(members)]=hist[k].get(len(members),0)+1
    need(hist=={1:{1:2},2:{1:4,2:2},3:{2:8,3:16,6:2144}},'all short parameter orbits counted once')
    need(len(STATES)==12938 and len(blocks)==2176 and sum(map(len,blocks.values()))==12938,
        'complete12938-state/2176-class parameter cover')
    return blocks,maps,hist

def decode(raw):
    try:table=list(csv.reader(io.StringIO(raw.decode('ascii'))))
    except (UnicodeError,csv.Error) as e:raise ValueError('malformed certificate') from e
    header=['index','roots','t','truth']+[v for j in range(1,PACK+1) for v in ('a'+str(j),'step'+str(j))]
    need(bool(table) and table[0]==header,'certificate header')
    need(len(table)==2177,'complete2176-row certificate')
    rows=[]
    for row in table[1:]:
        need(len(row)==22,'nine actual AP pairs per case')
        try:integers=[int(x) for x in row]
        except ValueError as e:raise ValueError('noninteger certificate field') from e
        need(all(x==str(n) for x,n in zip(row,integers)),'canonical integer encoding')
        rows.append(integers)
    return rows

def literal_pack(state,pairs):
    need(len(pairs)==PACK,'nine actual progression pairs')
    labels=set(roots(state));used=set();records=[]
    for a,d in pairs:
        need(type(a) is int and type(d) is int,'integer progression coordinates')
        need(0<=a<M and 1<=d<=309,'actual start and nonzero short step')
        residues=[(a+h*d)%M for h in range(7)]
        support={n%Q for n in residues}
        need(len(support)==7,'seven distinct field columns')
        need(not support&labels,'all original roots avoided')
        need(not support&used,'pairwise disjoint column supports')
        colors=[field_color(state,n%Q)^int(n%6 in (3,4,5)) for n in residues]
        need(len(set(colors))==1,'literal monochromatic actual AP')
        first=a if a else M;integers=[first+h*d for h in range(7)]
        need(d<=308 and integers[0]>=1 and integers[-1]<=2466 and len(set(integers))==7,'positive integer AP lift')
        need([n%M for n in integers]==residues,'cyclic/interval residues agree')
        used|=support;records.append([residues,sorted(support),colors,integers])
    need(len(used)==63,'nine disjoint seven-column supports')
    return records

def row_domain(rows,blocks):
    canonical=sorted(blocks)
    need(len(rows)==len(canonical),'complete2176-case coverage')
    # Check the whole ordered parameter cover before any AP work.
    for index,row in enumerate(rows):
        need(len(row)==22 and all(type(x) is int for x in row),'complete integer witness row')
        need(row[0]==index,'unique ordered case index')
        need(tuple(row[1:4])==canonical[index],'complete canonical parameter cover')
    return {tuple(row[1:4]):[tuple(row[4+2*j:6+2*j]) for j in range(PACK)] for row in rows}

def verify_rows(rows,blocks):
    packs=row_domain(rows,blocks)
    record=hashlib.sha256();zero=0;hist={}
    for index,row in enumerate(rows):
        state=tuple(row[1:4]);pairs=[tuple(row[4+2*j:6+2*j]) for j in range(PACK)]
        values=literal_pack(state,pairs);packs[state]=pairs
        for j,((a,d),literal) in enumerate(zip(pairs,values)):
            zero+=int(a==0);g=gcd(d,M);hist[g]=hist.get(g,0)+1
            record.update((json.dumps([index,j,state,a,d,literal],separators=(',',':'))+'\n').encode('ascii'))
    return packs,{'representative_APs':2176*9,'representative_points':2176*63,
        'start_zero_APs':zero,'representative_step_gcd_histogram':hist,
        'representative_literal_transcript_sha256':record.hexdigest()}

def transport_packs(packs,blocks,maps,first,last):
    record=hashlib.sha256();count=0;points=0;flips={};hist={};commitments=[]
    for representative in sorted(blocks)[first:last]:
        case=hashlib.sha256()
        for target in sorted(blocks[representative]):
            _,alpha,beta,flip=next(maps[representative,p] for p in ORDERS[representative[0]]
                if maps[representative,p][0]==target)
            aa=alpha+Q*((1-alpha)%6);bb=beta+Q*((-beta)%6)
            need(gcd(aa,M)==1 and aa%Q==alpha and aa%6==1,'CRT transport unit')
            need(bb%Q==beta and bb%6==0,'CRT translation preserves phase')
            pairs=[]
            for a,d in packs[representative]:
                newa=(aa*a+bb)%M;newd=aa*d%M
                need(newd!=0,'transport retains a nonconstant step')
                if newd>309:newa=(newa+6*newd)%M;newd=M-newd
                pairs.append((newa,newd))
                for h in range(7):
                    n=(a+h*d)%M;m=(aa*n+bb)%M
                    need(m%Q==(alpha*(n%Q)+beta)%Q and m%6==n%6,'actual point CRT coordinates')
                    before=field_color(representative,n%Q)^int(n%6 in (3,4,5))
                    after=field_color(target,m%Q)^int(m%6 in (3,4,5))
                    need(after==before^flip,'actual point color exchange retained')
            values=literal_pack(target,pairs)
            for j,((a,d),literal) in enumerate(zip(pairs,values)):
                event=(json.dumps([representative,target,flip,j,a,d,literal],separators=(',',':'))+'\n').encode('ascii')
                record.update(event);case.update(event)
                g=gcd(d,M);hist[g]=hist.get(g,0)+1
            flips[flip]=flips.get(flip,0)+1;count+=len(pairs);points+=7*len(pairs)
        commitments.append([list(representative),len(blocks[representative]),case.hexdigest()])
    states=sum(len(blocks[z]) for z in sorted(blocks)[first:last])
    need(count==states*9 and points==states*63,'entire specified transport batch checked')
    return {'first':first,'last':last,'transported_states':states,'transported_APs':count,'transported_points':points,
        'transport_color_flip_state_histogram':flips,'transported_step_gcd_histogram':hist,
        'batch_literal_transcript_sha256':record.hexdigest(),'case_commitments':commitments}

def controls(blocks,maps):
    need(len(SQUARES)==51 and 102 not in SQUARES,'square classes and nonsquare -1')
    multiplication=0
    for a in range(1,Q):
        for b in range(1,Q):
            need(bit(a*b)==bit(a)^bit(b),'character multiplicativity');multiplication+=1
    fixed={k:{p:0 for p in ORDERS[k]} for k in (1,2,3)}
    abstract=0;compositions=0
    for state in STATES:
        k,t,w=state;source_roots=roots(state)
        for p in ORDERS[k]:
            target,alpha,beta,flip=maps[state,p]
            fixed[k][p]+=int(target==state)
            need({(alpha*r+beta)%Q for r in source_roots}==set(roots(target)),'all original roots transported')
            toggle=bit(alpha)
            for argument in range(2**k):
                new=tuple(argument//(2**h)%2 for h in range(k));old=[0]*k
                for h,label in enumerate(p):old[label]=new[h]^toggle
                old_argument=sum(v*2**h for h,v in enumerate(old))
                need(TABLES[k,w][old_argument]==TABLES[k,target[2]][argument]^flip,
                    'every abstract truth transport entry')
                abstract+=1
            for q in ORDERS[k]:
                final,alpha2,beta2,flip2=maps[target,q]
                composite=tuple(p[h] for h in q)
                direct,aa,bb,ff=maps[state,composite]
                need((final,flip^flip2)==(direct,ff),'all action/output-flip compositions')
                need(alpha2*alpha%Q==aa and (alpha2*beta+beta2)%Q==bb,'all coordinate compositions')
                compositions+=1
    need(fixed[1]=={(0,):2} and sorted(fixed[2].values())==[4,8]
        and sorted(fixed[3].values())==[16,16,16,16,16,12928],'Burnside fixed-state counts')
    for k in (1,2,3):
        count=sum(z[0]==k for z in blocks)
        need(sum(fixed[k].values())==len(ORDERS[k])*count,'root-count-preserving Burnside equality')
    need(abstract==620612 and compositions==465442,'complete abstract truth/action domains')
    # The actual character-coordinate identity is independent of F. Combine
    # it with the ENTIRE abstract truth tables above by ordinary substitution.
    # 7,758,620 regular COLOR identities are implied, not literally iterated.
    coordinate=0
    for state in [(1,0,0),(2,0,0)]+[(3,t,0) for t in range(2,Q)]:
        for p in ORDERS[state[0]]:
            target,alpha,beta,_=maps[state,p];toggle=bit(alpha)
            for x in range(Q):
                old=PATTERNS[roots(state)][x]
                if old is None:continue
                new=PATTERNS[roots(target)][(alpha*x+beta)%Q]
                need(new is not None and all(old[p[h]]==new[h]^toggle for h in range(state[0])),
                    'actual regular field-input coordinate identity')
                coordinate+=1
    need(coordinate==60904,'complete character-coordinate basis')
    triples=0
    for r1 in range(Q):
        for r2 in range(Q):
            if r2==r1:continue
            inverse=INV[(r2-r1)%Q]
            for r3 in range(Q):
                if r3==r1 or r3==r2:continue
                t=(r3-r1)*inverse%Q
                need((3,t,0) in DOMAIN and ((r2-r1)*t+r1)%Q==r3,'all ordered root triples normalize')
                triples+=1
    need(triples==1061106,'complete ordered distinct-root triple domain')
    # Include constant and ignored-variable truth tables. Repeated labels
    # do not permit releasing any original root or claiming linear16.
    folds=0;folded={};distinct=0
    for labels in ((0,1,2),(0,0,0),(0,0,1),(0,1,0),(0,1,1)):
        variables=max(labels)+1;values=set()
        for word in range(256):
            original_truth=tuple(word//(2**i)%2 for i in range(8))
            for palette in range(8):
                truth=[]
                for argument in range(2**variables):
                    inputs=tuple((argument//(2**label)%2)^(palette//(2**i)%2)
                        for i,label in enumerate(labels))
                    original=sum(v*2**i for i,v in enumerate(inputs));truth.append(original_truth[original])
                flip=truth[0];normalized=sum((v^flip)*2**i for i,v in enumerate(truth))
                need(TABLES[variables,normalized]==tuple(v^flip for v in truth),'complete affine-sign/repeated-root truth folding')
                values.add(normalized)
                if variables==3:distinct+=len(truth)
                else:folds+=len(truth)
        need(values==set(range(0,2**(2**variables),2)),'every folded normalized truth table covered')
        folded[''.join(map(str,labels))]=len(values)
    need(folds==28672 and distinct==16384,'complete original Boolean folding domains')
    crt=0
    for s in range(1,Q):
        for r in range(Q):
            aa=s+Q*((1-s)%6);need(gcd(aa,M)==1,'all original CRT multipliers unit')
            for c in range(6):
                bb=r+Q*((-c-r)%6)
                for n in (0,1,617):
                    image=(aa*n+bb)%M
                    need(image%Q==(s*(n%Q)+r)%Q and image%6==(n-c)%6,
                        'all original field/phase normalization CRT parameters')
                crt+=1
    phase=0;illegal=0;legal=[]
    for word in range(64):
        row=tuple(word//(2**y)%2 for y in range(6));bad=[]
        for y in range(6):
            for delta in range(1,6):
                phase+=1
                if len({row[(y+h*delta)%6] for h in range(7)})==1:bad.append((y,delta))
        if not bad:legal.append(row);continue
        y,delta=next(pair for pair in bad if pair[1] in (2,3));d=Q*delta
        for r in range(Q):
            start=r+Q*((y-r)%6);residues=[(start+h*d)%M for h in range(7)]
            need(all(n%Q==r for n in residues) and len({row[n%6] for n in residues})==1,
                'illegal phase singleton-column mono AP')
            first=min(n if n else M for n in residues);integers=[first+h*d for h in range(7)]
            need(1<=first<=d and integers[-1]<=2163 and len(set(integers))==7,
                'illegal phase positive interval AP lift')
            need(all(n%Q==r for n in integers) and len({row[n%6] for n in integers})==1,
                'illegal phase integer colors')
            illegal+=1
    rotations={tuple(int((y+c)%6>=3) for y in range(6)) for c in range(6)}
    need(len(legal)==6 and set(legal)==rotations and phase==1920 and illegal==5974,'all six-row phases classified')
    masks=distances=0
    for r in (1,2,3):
        for holes in range(4):
            for omitted_roots in range(min(r,holes)+1):
                e=holes-omitted_roots;m=103-r-e;lower=9-e;upper=94-r;cut=85-r+e
                need(m-lower==upper and m-2*lower==cut,'masked distance/correlation algebra')
                for distance in range(m+1):
                    need((lower<=distance<=upper)==(abs(m-2*distance)<=cut),'all integer masked distance values')
                    distances+=1
                masks+=1
    need(masks==26 and distances==2620,'all zero-to-three-hole root-count classes')
    return {'multiplicativity_inputs':multiplication,'ordered_root_pair_maps':len(maps),
        'abstract_truth_transport_entries':abstract,'action_output_flip_and_coordinate_compositions':compositions,
        'fixed_states_by_root_count_and_permutation':{str(k):{''.join(map(str,p)):v for p,v in fixed[k].items()} for k in fixed},
        'actual_regular_field_input_coordinate_values':coordinate,
        'regular_field_COLOR_identities_IMPLIED_by_factorization':7758620,
        'original_ordered_distinct_root_triples':triples,'original_distinct_root_palette_truth_inputs':distinct,
        'original_repeated_root_truth_fold_inputs':folds,'folded_normalized_truth_functions':folded,
        'CRT_phase_parameter_sets':crt,'phase_cycle_inputs':phase,'legal_phase_rows':len(legal),
        'actual_illegal_phase_column_witnesses':illegal,'zero_to_three_hole_mask_classes':masks,
        'integer_distance_correlation_values':distances}

def damage_controls(rows,blocks):
    trials=[]
    def add(name,change):trials.append((name,change))
    add('missing canonical case',lambda r:r.pop())
    add('duplicate index',lambda r:r[1].__setitem__(0,0))
    add('duplicate parameter state',lambda r:r[1].__setitem__(slice(1,4),r[0][1:4]))
    add('zero original roots',lambda r:r[0].__setitem__(1,0))
    add('four original roots',lambda r:r[0].__setitem__(1,4))
    add('two-root field parameter not normalized',lambda r:r[2].__setitem__(2,103))
    add('truth table outside arity',lambda r:r[0].__setitem__(3,4))
    add('odd truth table outside output gauge',lambda r:r[0].__setitem__(3,1))
    add('missing AP pair',lambda r:r[0].pop())
    add('zero step',lambda r:r[0].__setitem__(5,0))
    add('start outside cyclic range',lambda r:r[0].__setitem__(4,618))
    add('ignored-input original root treated as regular',lambda r:r[0].__setitem__(4,0))
    add('repeated field column',lambda r:r[0].__setitem__(5,103))
    add('disjointness broken',lambda r:r[0].__setitem__(slice(6,8),r[0][4:6]))
    add('step outside short domain',lambda r:r[0].__setitem__(5,410))
    special=next(i for i,row in enumerate(rows) if row[1]==3 and len(blocks[tuple(row[1:4])])<6)
    wrong=next(z for z in sorted(blocks[tuple(rows[special][1:4])]) if z!=tuple(rows[special][1:4]))
    add('short orbit represented twice or incorrectly',lambda r:r[special].__setitem__(slice(1,4),wrong))
    state=tuple(rows[0][1:4]);bad=None
    for d in range(1,310):
        for a in range(M):
            residues=[(a+h*d)%M for h in range(7)];support={n%Q for n in residues}
            if len(support)!=7 or support&set(roots(state)):continue
            colors=[field_color(state,n%Q)^int(n%6 in (3,4,5)) for n in residues]
            if len(set(colors))>1:bad=(a,d);break
        if bad:break
    need(bad is not None,'actual nonmonochromatic damage control exists')
    add('literal colors not monochromatic',lambda r:r[0].__setitem__(slice(4,6),bad))
    # Also test a *second* free root for a constant function of two inputs.
    add('ignored second input root treated as regular',lambda r:r[2].__setitem__(4,1))
    rejected=[]
    for name,change in trials:
        damaged=copy.deepcopy(rows);change(damaged)
        try:verify_rows(damaged,blocks)
        except ValueError:rejected.append(name)
        else:raise ValueError('semantic damage accepted: '+name)
    need(len(rejected)==18,'complete semantic damage controls')
    return rejected

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--stage',choices=['cover','controls','transport'],required=True)
    p.add_argument('--first',type=int);p.add_argument('--last',type=int)
    args=p.parse_args();raw=args.certificate.read_bytes();rows=decode(raw);blocks,maps,hist=partition()
    common={'author':'six-vdw-3','role':'researcher','certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'certificate_bytes':len(raw)}
    if args.stage=='cover':
        _,representative=verify_rows(rows,blocks)
        result={**common,'status':'COMPLETE_PARAMETER_COVER_AND_REPRESENTATIVE_APS','parameter_states':12938,
            'parameter_classes':2176,'raw_states_by_original_root_count':{'1':2,'2':8,'3':12928},
            'parameter_classes_by_original_root_count':{'1':2,'2':6,'3':2168},
            'orbit_size_histograms_by_original_root_count':hist,'packing_per_case':9,**representative,
            'semantic_damage_rejections':damage_controls(rows,blocks),'canonical_states':[list(z) for z in sorted(blocks)]}
    elif args.stage=='controls':
        row_domain(rows,blocks)
        result={**common,'status':'COMPLETE_BOOLEAN_NORMALIZATION_AND_PHASE_CONTROLS','controls':controls(blocks,maps)}
    else:
        need(args.first is not None and args.last is not None and 0<=args.first<args.last<=2176,
            'explicit nonempty transport range')
        packs=row_domain(rows,blocks)
        result={**common,'status':'COMPLETE_SPECIFIED_POSITIVE_TRANSPORT_BATCH',
            **transport_packs(packs,blocks,maps,args.first,args.last)}
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
