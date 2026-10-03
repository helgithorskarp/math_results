"""Typed full-record comparison and explicit original-domain coverage checks.

Identity skips are allowed only for derived damage fixtures after full fresh
parsed-record comparison. This is a checker/contract, not a third math kernel.
"""
import itertools,math
P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
O=(5,7,9,15,21,35,45,63,105,315)
CONTEXT={'period':10080,'BASE_period':2520,'minimum_exactly':8,'literal_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],'original_moduli_distinct':True,'essential16_32':True,'BASE_holes_lower_bound':177,'productive_tail_count':9,'productive_allocation':[6,3],'other_phases_and_omissions_free':True,'selected_unproductive_tails_allowed':True,'proper_divisor_actual_LCM_allowed':True,'imports':{'BASE177':9934,'productive9':10022,'classification_only':10054},'ordinary_proof_unformalized':True}

def need(ok,why):
    if not ok:raise ValueError(why)

def equal(a,b,path=(),fixtures=False):
    if fixtures and a is b:return
    if type(a)is not type(b):raise ValueError('type mismatch at '+repr(path))
    if type(a)is dict:
        if a.keys()!=b.keys():raise ValueError('keys at '+repr(path))
        for k in a:equal(a[k],b[k],path+(k,),fixtures)
    elif type(a)is list:
        if len(a)!=len(b):raise ValueError('length at '+repr(path))
        for i,(x,y)in enumerate(zip(a,b)):equal(x,y,path+(i,),fixtures)
    else:
        if type(a)not in(int,bool,str,type(None)):raise ValueError('non-exact JSON scalar at '+repr(path))
        if a!=b:raise ValueError('value at '+repr(path))

def check_bundle(first,phases,sym,glue,context):
    equal(context,CONTEXT);R=[n for n in range(2520)if all(n%m!=a for m,a in P)];parents={str(s):[n for n in R if n%8==s]for s in(2,6)};base=[m for m in range(8,2521)if 2520%m==0 and m not in{m for m,a in P}]
    domain={'period':10080,'base_period':2520,'prefix':[list(x)for x in P],'placed_tail':[[16,2],[32,6]],'essential16_32_required':True,'minimum_exactly8':True,'actual_LCM_proper_divisor_allowed':True,'selected_unproductive_tails_allowed':True,'original_cofactors':list(O),'unused_BASE_originals':base,'BASE_original_phase_count':sum(base)}
    equal(first['domain'],domain);equal(first['initial_R'],R);equal(first['parents'],parents)
    need(len(first['small_shadows'])==14,'all5/9 original shadows')
    for r in first['small_shadows']:
        S=sorted(set(parents['2'])|{n for n in parents['6']if n%r['d']==r['phase']});equal(r['shadow'],S);need(r['size']==len(S)and r['budget']==len(S)-177,'small protected177 bridge');need(r['outside_need']==len(R)-len(S),'small outside need');need(r['omission_allowed']is True,'small omission')
        need(set(r['phase_populations'])==set(map(str,base)),'small original BASE labels')
        upper=0
        for m in base:
            rows=r['phase_populations'][str(m)];need(len(rows)==m,'all small original phases');upper+=max([0]+[b for a,b in rows if a<=r['budget']])
        need(upper==r['bound']and r['deficit']==r['outside_need']-upper,'small upper sum')
        need(len(S)<177 or r['deficit']>0,'small shadow exclusion')
    need(len(first['group_bounds'])==1024 and len(first['Q_arm_bounds'])==1024,'all cofactor groups')
    need(len(first['raw_pair_unions'])==45,'all original pairs')
    for r,(a,b)in zip(first['raw_pair_unions'],itertools.combinations(O,2)):
        equal(r['original_cofactors'],[a,b]);need(len(r['values'])==a*b,'all pair phases')
    total=0;expected_blocks=[]
    for h,record in enumerate(first['inventories']):
        q=5-h;need(record['h']==h and record['q']==q,'all5-extra strata');choices=[(list(A),list(B))for A in itertools.combinations(O,h)for B in itertools.combinations(O,q)];need(len(record['rows'])==len(choices),'full original inventory')
        for row,(H,Q)in zip(record['rows'],choices):
            equal(row['H'],H);equal(row['Q'],Q);need(type(row['bound'])is int and 0<=row['bound']<=150,'union bound type/range')
            if row['bound']>=87 and q!=1:expected_blocks.append({**row,'raw_phase_tuples':math.prod(H+Q)*(2 if q==2 else 1)})
        total+=len(choices)
    need(total==15504,'complete inventories');equal(first['phase_blocks'],expected_blocks);need(len(phases)==len(expected_blocks),'full26 phase blocks')
    shape_masks=set();weighted=0;canonical=0
    for i,(block,original)in enumerate(zip(phases,expected_blocks)):
        need(block['block']==i,'complete phase block order');equal(block['H'],original['H']);equal(block['Q'],original['Q']);need(block['canonical_rows']==len(block['rows']),'canonical count')
        ds=block['H']+block['Q'];last=None;weight=0
        for r in block['rows']:
            a=r['odd_phases'];arms=r['Q_arms'];key=(a,arms)
            if last is not None:need(last<key,'unique sorted full rows')
            last=key;need(len(a)==5 and all(type(v)is int and 0<=v<d for v,d in zip(a,ds)),'all original phases');need(arms in([10,26],[26,10])if block['Q']else arms==[],'ordered Q arms')
            original_phases=[]
            for j,(d,v)in enumerate(zip(ds,a)):
                p=16 if j<len(block['H'])else 32;b=10 if p==16 else arms[j-len(block['H'])];original_phases.append(b+p*((v-b)*pow(p,-1,d)%d))
            equal(r['original_phases'],original_phases);mask=int(r['repair_mask_hex'],16);need(0<=mask<1<<150 and format(mask,'x')==r['repair_mask_hex'],'literal repair mask');need(r['repair_size']==mask.bit_count(),'repair size');need(type(r['orbit_weight'])is int and r['orbit_weight']>0,'orbit weight');flags=r['exclusive_initial_witness'];need(len(flags)==5 and all(type(b)is bool for b in flags),'original exclusive witnesses bool');need(type(r['survives_necessary_tests'])is bool and r['survives_necessary_tests']==(mask.bit_count()>=87 and all(flags)),'necessary tests bridge')
            weight+=r['orbit_weight']
            if r['survives_necessary_tests']:shape_masks.add(mask)
        need(weight==block['raw_weight']==original['raw_phase_tuples'],'full raw phase weight per original inventory');weighted+=weight;canonical+=len(block['rows'])
    need(weighted==17393805 and canonical==137963,'complete phase domain');need(len(shape_masks)==113,'full113 distinct repair sets')
    originals=[m for m in range(8,10081)if 10080%m==0];equal(sym['originals'],originals);need(len(sym['generators'])==12,'full generators')
    for g in sym['generators']:
        need(g['physical_membership_domain_size']==len(originals)*10080,'membership domain');need(len(g['family_images'])==65,'all original families')
        for m,row in zip(originals,g['family_images']):need(row['m']==m and sorted(row['phase_images'])==list(range(m)),'same-original phase bijection')
    fixed=[x for x in parents['6']if all(n%32==6 or n%48==14 or n%96==86 for n in(x+2520*k for k in range(4)))];equal(glue['fixed_parent6'],fixed);need(len(fixed)==90,'forced physical90')
    need(len(glue['shapes'])==len(shape_masks),'all final shapes')
    for mask,row in zip(sorted(shape_masks),glue['shapes']):
        equal(row['parent2_mask_hex'],format(mask,'x'));p2=[x for j,x in enumerate(parents['2'])if mask>>j&1];equal(row['parent2_holes'],p2);S=sorted(p2+fixed);equal(row['shadow'],S);need(row['size']==len(S)and row['protected_budget']==len(S)-177,'literal177 shadow budget');need(row['outside_need']==len(R)-len(S),'all outside points');need(len(row['BASE_phase_rows'])==len(base),'every unused BASE original')
        upper=0
        for m,f in zip(base,row['BASE_phase_rows']):
            need(f['original']==m and len(f['phases'])==m,'every original BASE phase');need(f['omission_allowed']is True,'free BASE omission');bound=max([0]+[b for a,b in f['phases']if a<=row['protected_budget']]);need(bound==f['outside_max_with_omission'],'per-original relaxed maximum');upper+=bound
        need(upper==row['outside_upper']and row['deficit']==row['outside_need']-upper and row['deficit']>0,'final coverage contradiction')
    return {'context':CONTEXT,'complete_blocks':len(phases),'canonical_rows':canonical,'raw_phase_weight':weighted,'final_shapes':len(shape_masks),'phase_entries':len(shape_masks)*sum(base),'all_deficits_positive':True,'comparison':'Full fresh parsed two-method records and canonical byte products checked separately; fixtures only may skip identical already-verified subtrees.'}
