"""Independent same-author checker; imports no producer arithmetic."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,product
import json
from math import lcm,perm,prod
from pathlib import Path
from struct import pack
import time


PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(16,2),(28,4),(32,6))
def document(stage,values):
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':stage,
      'status':'exact arithmetic record; ordinary conditional proof in proof.md',
      'domain':{'minimum_exactly':8,'original_moduli_divide':10080,
        'literal_prefix':list(map(list,PREFIX)),'essential_originals_explicit':[16,32],
        'productive_TAILs_exactly':9,'hole_parent_counts':[6,3],
        'BASE_lower_bound_imported':177,'productive_lower_bound_imported':9,
        'productivity':'meets an actual BASE-hole lift x+2520k, k=0,1,2,3',
        'all_other_original_phases_and_omissions_free':True,
        'unproductive_selected_TAILs_allowed':True,'proper_divisor_actual_LCM_allowed':True,
        'original_labels_preserved':True,'prior_private_pilot_as_input':False,
        'three_H_126_numerical_input_used':False,'ordinary_proof_formalized':False,
        'independent_person_reviewed':False,'new_tenth_tail_bound_claimed':False,
        'global_bound_changed':False},**values}

P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
DS=tuple(d for d in range(3,316) if 315%d==0);O=tuple(d for d in DS if d!=3)
R=tuple(x for x in range(2520) if all(x%m!=a for m,a in P))
R2=tuple(x for x in R if x%8==2);R6=tuple(x for x in R if x%8==6)
def require(v,msg):
    if not v:raise ValueError(msg)
def load(path):return json.loads(Path(path).read_text())

def capacity_audit(data):
    families={d:[{x for x in R2 if x%d==a} for a in range(d)] for d in (1,)+DS}
    pops=[[d,[len(s) for s in families[d]]] for d in (1,)+DS]
    require(pops==data['C_all_physical_phase_populations'],'Whole odd populations')
    require(all([len(s) for s in families[d]]==[sum(x%d==a for x in R6) for a in range(d)] for d in (1,)+DS),'Second mandatory physical parent differs')
    C={d:max(len(s) for s in families[d]) for d in (1,)+DS}
    require([[d,C[d]] for d in (1,)+DS]==data['C_maxima'],'C maxima')
    pair={};pair_rows=[]
    for a,b in combinations(O,2):
        values=[len(A)+len(B)-len(A&B) for A in families[a] for B in families[b]]
        pair[a,b]=max(values);pair_rows.append([[a,b],values,max(values)])
    require(pair_rows==data['all_raw_pair_union_rows'],'Every raw physical pair union value')
    @lru_cache(None)
    def saving(H):
        if len(H)<2:return 0
        a=H[0];rest=H[1:]
        return max([saving(rest)]+[C[a]+C[b]-pair[tuple(sorted((a,b)))]+saving(tuple(c for c in rest if c!=b)) for b in rest])
    @lru_cache(None)
    def U(H):return min(150,sum(C[d] for d in H)-saving(H))
    def qb(Q):
        maxima=[]
        for bits in product((0,1),repeat=len(Q)):
            if not bits or bits[0]!=0 or 1 not in bits:continue
            A=tuple(d for d,b in zip(Q,bits) if b==0);B=tuple(d for d,b in zip(Q,bits) if b==1)
            maxima.append(min(U(A),U(B),sum(C[lcm(a,b)] for a in A for b in B)))
        return max([0]+maxima)
    urows=[[list(H),U(H)] for k in range(6) for H in combinations(O,k)]
    qrows=[[list(Q),qb(Q)] for k in range(6) for Q in combinations(O,k)]
    require(urows==data['all_union_upper_bounds'],'All pair-matching union upper bounds')
    require(qrows==data['all_Q_arm_upper_bounds'],'All binary arm capacities')
    qcaps={tuple(q):c for q,c in qrows};types=[];candidates=[]
    for h in range(6):
        values=[];high=[]
        for H in combinations(O,h):
            for Q in combinations(O,5-h):
                cap=min(150,U(H)+qcaps[Q]);values.append(cap)
                if cap>=87:high.append([list(H),list(Q),cap])
        types.append({'h':h,'q':5-h,'all_caps':values,'maximum_parent2':max(values),'surviving_inventories':high,'single_Q_redundancy_excludes_type':h==4})
        if h!=4:candidates.extend(high)
    require(types==data['all_six_parent2_types'],'Entire six relevant type streams')
    require(candidates==data['phase_candidates'],'Entire relevant inventory survivor list')
    physical=[]
    for a in range(14,48,16):
        for b in range(22,96,32):
            count=0
            for x in R6:
                quartet={x+2520*k for k in range(4)}
                covered={n for n in quartet if n%32==6 or n%48==a or n%96==b}
                count+=quartet==covered
            physical.append([a,b,count])
    require(physical==data['all_parent6_48_96_opposite_half_missing_quarter_phase_counts'],'All original48/96 physical quarter tuples')
    require(max(t['maximum_parent2'] for t in types)==data['uniform_parent2_capacity']==109,'Uniform109')
    require([[g,q,C[lcm(g,q)]] for g in DS for q in DS]==data['all_non3_HQ_LCM_capacities'],'All original-HQ LCM rows')
    require(data['prefix']==list(map(list,P))+[[16,2],[32,6]] and data['essential_originals_explicit']==[16,32] and data['minimum_exactly']==8 and data['original_moduli_divide']==10080 and data['count_pair']==[6,3],'Literal domain')
    require(data['remaining_pool']==list(O) and data['three_H_126_numerical_input_used'] is False and data['BASE177_and_nine_tail_lower_bound_imported'] is True and data['global_original_H_and_Q_distinct'] is True and data['cross_H_Q_equalities_legal'] is True and data['global_bound_changed'] is False,'Exact mathematical domain flags')
    return document('capacity', {
      'prefix':list(map(list,P))+[[16,2],[32,6]],'essential_originals_explicit':[16,32],
      'minimum_exactly':8,'original_moduli_divide':10080,'count_pair':[6,3],
      'BASE177_and_nine_tail_lower_bound_imported':True,'three_H_126_numerical_input_used':False,
      'C_all_physical_phase_populations':pops,'C_maxima':[[d,C[d]] for d in (1,)+DS],
      'remaining_pool':list(O),'all_raw_pair_union_rows':pair_rows,
      'all_parent6_48_96_opposite_half_missing_quarter_phase_counts':physical,
      'all_union_upper_bounds':urows,'all_Q_arm_upper_bounds':qrows,
      'all_six_parent2_types':types,'phase_candidates':candidates,
      'all_non3_HQ_LCM_capacities':[[g,q,C[lcm(g,q)]] for g in DS for q in DS],
      'uniform_parent2_capacity':max(t['maximum_parent2'] for t in types),
      'global_original_H_and_Q_distinct':True,'cross_H_Q_equalities_legal':True,
      'global_bound_changed':False})

# Independent normal-form enumeration by restricted-growth coordinate strings.
# No first-appearance normalization function or raw-prefix rejection is imported.
FREE=((0,2,3,4),(1,2,3,5,6),(3,6),(1,4,7),(2,5,8))
def tuples(ds):
    def choices(axis,state):
        fixed=(1,) if axis==0 else (0,4) if axis==1 else (0,) if axis==2 else ()
        vals=FREE[axis];k=state[axis]
        return fixed+vals[:min(len(vals),k+1)]
    def walk(i,ph,state):
        if i==len(ds):
            weight=prod(perm(len(f),k) for f,k in zip(FREE,state));yield ph,weight;return
        d=ds[i];components=[]
        if d%9==0:components.append((9,tuple((v,axis) for axis in (2,3,4) for v in choices(axis,state))))
        elif d%3==0:components.append((3,tuple((v,None) for v in range(3))))
        if d%5==0:components.append((5,tuple((v,0) for v in choices(0,state))))
        if d%7==0:components.append((7,tuple((v,1) for v in choices(1,state))))
        branches=[]
        for values in product(*(vals for _,vals in components)):
            nxt=list(state);a=0
            for (mod,_),(v,axis) in zip(components,values):
                a+=v*(d//mod)*pow(d//mod,-1,mod)
                if axis is not None and nxt[axis]<len(FREE[axis]) and v==FREE[axis][nxt[axis]]:nxt[axis]+=1
            branches.append((a%d,tuple(nxt)))
        for a,nxt in sorted(branches):yield from walk(i+1,ph+(a,),nxt)
    return walk(0,(),(0,0,0,0,0))

def original_phase(d,b,a,two):return a+d*((b-a)*pow(d,-1,two)%two)

def phase_audit(data,cap):
    physical={};xs=tuple(x+2520*k for x in R2 for k in range(4))
    for d in O:
        for two,b in ((16,10),(32,10),(32,26)):
            for a in range(d):
                phase=original_phase(d,b,a,two)
                physical[d,two,b,a]={(n%2520,n%32) for n in xs if n%(two*d)==phase}
    blocks=[];shapes=set();allrows=0;allraw=0
    for H,Q,_ in cap['phase_candidates']:
        H=tuple(H);Q=tuple(Q);ds=H+Q;blocks_rows=[];hist=[0]*151;ehist=[0]*151;total=0
        # Explicit quarter cases are produced independently of bit orientation.
        arms=list(product((10,26),repeat=len(Q)))
        arms=[a for a in arms if not Q or 10 in a and 26 in a]
        for ph,weight in tuples(ds):
            hs=[physical[d,16,10,a] for d,a in zip(H,ph[:len(H)])]
            for arm in arms:
                qs=[physical[d,32,b,a] for d,b,a in zip(Q,arm,ph[len(H):])]
                classes=hs+qs;filled=set()
                for v in classes:filled|=v
                left={x for x,b in filled if b==10};right={x for x,b in filled if b==26}
                repair=left&right;n=len(repair);needed=n>=87
                if needed:
                    for i,v in enumerate(classes):
                        others=set()
                        for j,w in enumerate(classes):
                            if i!=j:others|=w
                        if not any(x in repair for x,b in v-others):needed=False;break
                mask=sum(1<<i for i,x in enumerate(R2) if x in repair) if needed else None
                bb=[0 if b==10 else 1 for b in arm]
                blocks_rows.append([list(ph),bb,weight,n,needed,mask]);hist[n]+=weight;total+=weight
                if needed:ehist[n]+=weight;shapes.add(mask)
        expected=prod(ds)*len(arms);require(total==expected,'Restricted-growth census omits an original phase orbit')
        blocks.append({'H':list(H),'Q':list(Q),'all_canonical_phase_rows':blocks_rows,'weighted_raw_histogram':hist,'weighted_essential_ge87_histogram':ehist,
                       'weighted_phase_total':total,'expected_raw_phase_total':expected,'maximum_parent2':max(n for n,w in enumerate(hist) if w),'essential_ge87_weight':sum(ehist)})
        allrows+=len(blocks_rows);allraw+=total
    require(blocks==data['all_inventory_phase_blocks'],'Every normalized original physical phase row/weight/essential test')
    require(sorted(shapes)==data['canonical_repair_masks'],'All normalized repair shapes')
    require(len(shapes)==data['canonical_shapes']==113 and allrows==data['canonical_phase_rows'] and allraw==data['weighted_raw_phase_rows'],'Complete domain counters')
    require(data['fixed_parent6_phases']==[[48,14],[96,86]] and data['parent6_repair_capacity']==90 and data['large_H_uniform126_used'] is False and data['global_bound_changed'] is False,'Phase-domain flags')
    return document('phases', {'all_inventory_phase_blocks':blocks,
      'canonical_repair_masks':sorted(shapes),'canonical_shapes':len(shapes),
      'canonical_phase_rows':allrows,'weighted_raw_phase_rows':allraw,
      'fixed_parent6_phases':[[48,14],[96,86]],'parent6_repair_capacity':90,
      'large_H_uniform126_used':False,'global_bound_changed':False})

def gluing_audit(data,raw_actual,phases=None,small=False):
    base=tuple(m for m in range(8,2521) if 2520%m==0 and m not in dict(P))
    expected=0;raw=bytearray();deficits=[];expectedrows=[]
    if small:
        expectedrows=[]
        for d in (5,9):
            for a in range(d):
                shadow={x for x in R if x%8==2 or x%8==6 and x%d==a}
                s=len(shadow)
                if s<177:expectedrows.append({'d':d,'odd_phase':a,'shadow_size':s,'status':'capacity<177','all_BASE_originals_omission_free':True});continue
                families=[]
                for m in base:
                    inside=[0]*m;whole=[0]*m
                    for x in shadow:inside[x%m]+=1
                    for x in R:whole[x%m]+=1
                    counts=[[i,w-i] for i,w in zip(inside,whole)]
                    for i,o in counts:raw.extend(pack('>HH',i,o))
                    bound=max([0]+[o for i,o in counts if i<=s-177]);families.append([m,counts,bound])
                total=sum(f[-1] for f in families)
                expectedrows.append({'d':d,'odd_phase':a,'shadow_size':s,'per_phase_protected_budget':s-177,'outside_required':len(R)-s,
                                     'sum_per_original_outside_maxima':total,'all_BASE_originals_omission_free':True,
                                     'all_BASE_phase_families':families,'excluded_by_union_bound':total<len(R)-s})
                deficits.append(len(R)-s-total);expected+=sum(base)
        require(expectedrows==data['all_odd_phases'],'Entire small-shadow original phase census')
    else:
        require(sorted(row['p2_mask'] for row in data['all_canonical_shapes'])==phases['canonical_repair_masks'],'Shape coverage agrees with fresh independent phase proof')
        for mask in phases['canonical_repair_masks']:
            shadow={x for i,x in enumerate(R2) if mask&(1<<i)}|{x for x in R6 if x%3==2}
            s=len(shadow);budget=s-177;families=[]
            for m in base:
                inside=[0]*m;whole=[0]*m
                for x in shadow:inside[x%m]+=1
                for x in R:whole[x%m]+=1
                counts=[[i,w-i] for i,w in zip(inside,whole)]
                for i,o in counts:raw.extend(pack('>HH',i,o))
                bound=max([0]+[o for i,o in counts if i<=budget]);families.append([m,counts,bound])
            total=sum(f[-1] for f in families);deficit=len(R)-s-total
            reference={'p2_mask':mask,'size':s,'protected_budget':budget,'outside_required':len(R)-s,
                       'sum_per_original_outside_maxima':total,'deficit':deficit,
                       'all_unused_BASE_families':families,'excluded':deficit>0}
            expectedrows.append(reference)
            deficits.append(deficit);expected+=sum(base)
        require(data['canonical_shapes']==len(phases['canonical_repair_masks']) and data['all_BASE_phase_entries']==expected and data['minimum_deficit']==min(deficits) and data['unexcluded_shapes']==0,'BASE gluing complete counters')
    require(raw==raw_actual,'Every raw physical protected/outside count byte')
    require(len(raw)==data['raw_phase_stream_bytes' if small else 'raw_bytes'] and sha256(raw).hexdigest()==data['raw_phase_sha256' if small else 'raw_sha256'],'Raw count provenance')
    if small:
        reference=document('small', {'minimum_exactly':8,'original_moduli_divide':10080,
          'prefix':list(map(list,P))+[[16,2],[32,6]],'counts':[6,3],
          'all_H_and_Q_global_original_distinct':True,'shadow_cofactors':[5,9],
          'BASE_lower177_imported':True,'all_unused_BASE_originals':list(base),'BASE_phase_count':sum(base),
          'all_odd_phases':expectedrows,'raw_phase_stream_bytes':len(raw),
          'raw_phase_sha256':sha256(raw).hexdigest(),'whole_63_count_exclusion_claimed':False,
          'global_bound_changed':False})
    else:
        reference=document('gluing', {'all_canonical_shapes':expectedrows,'canonical_shapes':len(expectedrows),
          'all_BASE_phase_entries':expected,'raw_bytes':len(raw),'raw_sha256':sha256(raw).hexdigest(),
          'minimum_deficit':min(deficits),'unexcluded_shapes':sum(not r['excluded'] for r in expectedrows),
          'all_original_BASE_phases_and_omissions_free':True,'full_count_63_exclusion_claimed':True,
          'global_bound_changed':False})
    require(min(deficits)>0,'BASE compatibility exclusion failed')
    return reference,bytes(raw)

def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON object key')
        result[key]=value
    return result

def read_record(path):return json.loads(path.read_text(),object_pairs_hook=unique_object)

def full_equal(actual,expected):
    # Exact JSON types matter: Python equality alone aliases True with1.
    # Identity skips only shared UNCHANGED subtrees in the damage controls.
    # Fresh parsed producer data has distinct containers, so every value is
    # checked against the independently rebuilt record before those controls.
    require(type(actual) is type(expected),'Exact JSON type differs')
    if actual is expected:return
    if isinstance(expected,dict):
        require(actual.keys()==expected.keys(),'Complete record keys differ')
        for key,value in expected.items():full_equal(actual[key],value)
    elif isinstance(expected,list):
        require(len(actual)==len(expected),'Complete record list domain differs')
        for a,b in zip(actual,expected):full_equal(a,b)
    else:require(actual==expected,'Complete independently recomputed value differs')

def changed(value,path,replacement):
    if not path:return replacement
    result=value.copy();key=path[0]
    result[key]=changed(value[key],path[1:],replacement)
    return result

def negative_controls(stage,reference,raw):
    # Cached references are created ONLY after a complete independent arithmetic
    # reconstruction. Damages test that exact comparator, not a hash-only audit.
    cases=[('exact-minimum-changed',('domain','minimum_exactly'),7),
      ('literal-14-phase-changed',('domain','literal_prefix',3,1),1),
      ('essential-16-dropped',('domain','essential_originals_explicit'),[32]),
      ('BASE-premise-lowered',('domain','BASE_lower_bound_imported'),176),
      ('productive-count-ten',('domain','productive_TAILs_exactly'),10),
      ('omissions-forbidden',('domain','all_other_original_phases_and_omissions_free'),False),
      ('private-pilot-input-enabled',('domain','prior_private_pilot_as_input'),True),
      ('bool-replaced-by-int',('domain','original_labels_preserved'),1)]
    if stage=='capacity':
        cases += [('spent-original48-reused',('remaining_pool',),[3]+reference['remaining_pool']),
          ('raw-pair-phase-dropped',('all_raw_pair_union_rows',0,1),reference['all_raw_pair_union_rows'][0][1][:-1]),
          ('pair-union-increased',('all_raw_pair_union_rows',0,1,0),reference['all_raw_pair_union_rows'][0][1][0]+1),
          ('single-Q-redundancy-disabled',('all_six_parent2_types',4,'single_Q_redundancy_excludes_type'),False),
          ('inventory-omitted',('phase_candidates',),reference['phase_candidates'][:-1]),
          ('legal-cross-HQ-equality-forbidden',('cross_H_Q_equalities_legal',),False)]
    elif stage=='phases':
        row=reference['all_inventory_phase_blocks'][0]['all_canonical_phase_rows'][0]
        cases += [('orbit-row-dropped',('all_inventory_phase_blocks',0,'all_canonical_phase_rows'),reference['all_inventory_phase_blocks'][0]['all_canonical_phase_rows'][:-1]),
          ('orbit-weight-changed',('all_inventory_phase_blocks',0,'all_canonical_phase_rows',0,2),row[2]+1),
          ('quarter-arm-changed',('all_inventory_phase_blocks',0,'all_canonical_phase_rows',0,1,0),2),
          ('repair-count-changed',('all_inventory_phase_blocks',0,'all_canonical_phase_rows',0,3),row[3]+1),
          ('essential-test-changed',('all_inventory_phase_blocks',0,'all_canonical_phase_rows',0,4),not row[4]),
          ('repair-mask-changed',('canonical_repair_masks',0),reference['canonical_repair_masks'][0]^1),
          ('fixed-original96-phase-changed',('fixed_parent6_phases',1,1),54)]
    elif stage=='small':
        family=reference['all_odd_phases'][0]['all_BASE_phase_families'][0]
        cases += [('all-original-phase-domain-shortened',('all_odd_phases',0,'all_BASE_phase_families',0,1),family[1][:-1]),
          ('protected-population-changed',('all_odd_phases',0,'all_BASE_phase_families',0,1,0,0),family[1][0][0]+1),
          ('small-shadow-phase-omitted',('all_odd_phases',),reference['all_odd_phases'][:-1]),
          ('omission-zero-disabled',('all_odd_phases',0,'all_BASE_originals_omission_free'),False)]
    elif stage=='gluing':
        first=reference['all_canonical_shapes'][0];family=first['all_unused_BASE_families'][0]
        cases += [('shape-omitted',('all_canonical_shapes',),reference['all_canonical_shapes'][:-1]),
          ('protected-budget-relaxed',('all_canonical_shapes',0,'protected_budget'),first['protected_budget']+1),
          ('BASE-original-relabelled',('all_canonical_shapes',0,'all_unused_BASE_families',0,0),family[0]+1),
          ('BASE-phase-omitted',('all_canonical_shapes',0,'all_unused_BASE_families',0,1),family[1][:-1]),
          ('outside-union-bound-increased',('all_canonical_shapes',0,'sum_per_original_outside_maxima'),first['sum_per_original_outside_maxima']+1),
          ('omission-zero-disabled',('all_original_BASE_phases_and_omissions_free',),False)]
    else:
        row=reference['all_generators'][0]['all_original_phase_images'][0]
        cases += [('generator-omitted',('all_generators',),reference['all_generators'][:-1]),
          ('original-family-relabelled',('all_generators',0,'all_original_phase_images',0,0),row[0]+1),
          ('original-phase-image-changed',('all_generators',0,'all_original_phase_images',0,1,0),row[1][0]^1),
          ('fixed-96-prefix-weakened',('prefix_fixed',9,1),54),
          ('original-families-aliased',('families_not_quotiented',),False)]
    rejected=[]
    for label,path,value in cases:
        damage=changed(reference,path,value)
        try:full_equal(damage,reference)
        except ValueError:rejected.append(label)
        else:raise ValueError('Semantic damage accepted: '+label)
    extra=dict(reference);extra['unexpected_weaker_domain']=True
    try:full_equal(extra,reference)
    except ValueError:rejected.append('unexpected-schema-key')
    else:raise ValueError('Unexpected metadata key accepted')
    raw_rejected=[]
    if raw is not None:
        variants=(('count-byte-flipped',bytes([raw[0]^1])+raw[1:]),
                  ('count-byte-truncated',raw[:-1]),('count-byte-appended',raw+b'\x00'))
        for label,damage in variants:
            try:require(damage==raw,'Complete independently generated raw stream differs')
            except ValueError:raw_rejected.append(label)
            else:raise ValueError('Raw semantic damage accepted')
    return {'semantic_record_damages_rejected':rejected,'raw_stream_damages_rejected':raw_rejected,
            'fresh_complete_reference_before_controls':True,'hash_only_check':False}


def symmetry_audit(data,raw_actual):
    mods=[m for m in range(8,10081) if 10080%m==0]
    require(data['all_original_moduli']==mods and data['modulus']==10080,'Complete original divisor family')
    generators=((5,0,2),(5,2,3),(5,3,4),(7,1,2),(7,2,3),(7,3,5),(7,5,6),(9,3,6),(9,1,4),(9,4,7),(9,2,5),(9,5,8))
    expected=[];raw=bytearray()
    for axis,a,b in generators:
        # Independent proof layer: coordinate-tree bijections, then phase
        # images from the original modulus CRT, without a10080 map.
        if axis==9:require(a%3==b%3 and 0 not in (a,b),'3-adic residue-tree failure')
        require((axis!=5 or 1 not in (a,b)) and (axis!=7 or not{0,4}&{a,b}),'Spent coordinate moved')
        rows=[]
        for m in mods:
            images=[]
            for r in range(m):
                if m%axis==0:
                    v=r%axis;nv=b if v==a else a if v==b else v
                    image=(r+(nv-v)*(m//axis)*pow(m//axis,-1,axis))%m
                else:image=r
                images.append(image);raw.extend(pack('>H',image))
            require(sorted(images)==list(range(m)),'Original phase family fails bijection')
            rows.append([m,images])
        by=dict(rows)
        require(all(by[m][a]==a for m,a in data['prefix_fixed']),'Prefix not fixed in original CRT')
        expected.append({'axis':axis,'transposition':[a,b],'all_original_phase_images':rows,'whole_literal_prefix_and48_96_fixed':True,'all_original_families_preserved':True})
    require(expected==data['all_generators'] and len(expected)==data['generator_count']==12,'Entire original-family generator maps')
    require(raw==raw_actual,'Every raw phase-image byte')
    require(data['physical_n_m_checks']==12*len(mods)*10080 and data['raw_phase_images_bytes']==len(raw) and data['raw_sha256']==sha256(raw).hexdigest(),'Symmetry domain counts')
    reference=document('symmetry', {'modulus':10080,'all_original_moduli':mods,'all_generators':expected,
      'generator_count':len(expected),'physical_n_m_checks':len(expected)*len(mods)*10080,
      'raw_phase_images_bytes':len(raw),'raw_sha256':sha256(raw).hexdigest(),
      'prefix_fixed':list(map(list,PREFIX))+[[48,14],[96,86]],
      'families_not_quotiented':True,'global_bound_changed':False})
    return reference,bytes(raw)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('capacity','phases','small','gluing','symmetry'))
    p.add_argument('--work-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();work=args.work_dir;actual=read_record(work/(args.stage+'.json'));t=time.monotonic()
    raw=None
    if args.stage=='capacity':reference=capacity_audit(actual)
    elif args.stage=='phases':reference=phase_audit(actual,read_record(work/'capacity.json'))
    elif args.stage in ('small','gluing'):
        phases=read_record(work/'phases.json') if args.stage=='gluing' else None
        reference,raw=gluing_audit(actual,(work/(args.stage+'.raw')).read_bytes(),phases,small=args.stage=='small')
    else:reference,raw=symmetry_audit(actual,(work/'symmetry.raw').read_bytes())
    full_equal(actual,reference);whole=canonical(reference)
    controls=negative_controls(args.stage,reference,raw)
    args.out.write_bytes(whole)
    if raw is not None:(work/('audit-'+args.stage+'.raw')).write_bytes(raw)
    print(json.dumps({'stage':args.stage,'seconds':time.monotonic()-t,
      'whole_record_bytes':len(whole),'whole_sha256':sha256(whole).hexdigest(),
      'all_full_mathematical_records_equal':True,'all_raw_stream_bytes_equal':raw is not None,
      'producer_arithmetic_imported':False,'old_pilot_input_used':False,'negative_controls':controls}))
