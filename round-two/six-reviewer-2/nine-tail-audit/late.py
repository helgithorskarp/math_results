"""POST-SEAL data-only native correspondence. Never imports native code.

This format-aware check was written after native exposure, so is corroboration.
The original sealed literal/direct proofs remain the independent evidence.
"""
import json,sys,hashlib
from itertools import combinations,product
from math import lcm
from literal import masks,wire,need

def check(own,native):
    R=own['R'];D=own['cofactors'];C=dict(own['capacity']);U=sorted(n%315 for n in R if n%8==2);ph={d:masks(U,d)for d in [1]+D};UB={tuple(v[0]):v[2]for v in own['all_exact_H_unions']};checked=0
    def eq(a,b,label):
        nonlocal checked
        need(a==b,'native correspondence '+label);checked+=1
    eq(native['all_marked_odd_phase_population_rows'],[[d,[v.bit_count()for v in ph[d]]]for d in [1]+D],'all marked odd populations')
    eq(native['Q_pairs'],[[v[0],v[1]]for v in own['intersections']['2']],'55 Q pairs')
    eq(native['Q_triples'],[[v[0],v[1],v[2]]for v in own['intersections']['3']],'165 Q triples')
    for k,key in [(4,'Q_four_triple_sums'),(5,'Q_five_triple_sums')]:eq(native[key],[[v[0],v[3]]for v in own['intersections'][str(k)]],key)
    eq(native['all_five_H_cofactor_capacity_sums'],[[list(ds),sum(C[d]for d in ds)]for ds in combinations(D,5)],'all462 global H sums')
    required={tuple(subgroup)for family in own['high_five_H_sets']for n in range(1,5)for subgroup in combinations(family,n)}
    required.update(tuple(v[0])for v in own['H_triples']if v[1]>126);required.update(combinations((3,5,9),2))
    eq([v[0]for v in native['all_raw_H_union_phase_blocks']],[list(ds)for ds in sorted(required)],'116 complete native UB groups')
    raw_H=0
    for ds,claimed,maximum in native['all_raw_H_union_phase_blocks']:
        fresh=[]
        for aa in product(*(range(d)for d in ds)):
            bits=0
            for d,a in zip(ds,aa):bits|=ph[d][a]
            fresh.append(bits.bit_count())
        eq([claimed,maximum],[fresh,max(fresh)],'whole raw H group '+str(ds));raw_H+=len(fresh)
    eq(native['all_three_H_union_bounds'],[v[:3]for v in own['H_triples']],'all H triple bounds')
    five=[]
    for ds in map(tuple,own['high_five_H_sets']):
        for k in range(1,5):
            for P in combinations(ds,k):
                rest=[d for d in ds if d not in P]
                for n in range(1,len(rest)+1):
                    for O in combinations(rest,n):
                        A=[d for d in rest if d not in O];cross=sum(C[lcm(o,a)]for o in O for a in A)
                        qs=[[q,min(C[q],sum(C[lcm(o,q)]for o in O))]for q in D]
                        five.append([list(ds),list(P),list(O),A,UB[P],UB[O],cross,qs,UB[P]+min(UB[O],cross+max(v[1]for v in qs))])
    eq(native['all_high_five_H_orientation_rows'],five,'whole1620 high-H orientations')
    arms=[]
    for ds in combinations(D,4):
        for size in (1,2):
            for A in combinations(ds,size):
                B=tuple(d for d in ds if d not in A)
                if size==2 and A>B:continue
                cross=sum(C[lcm(a,b)]for a in A for b in B)
                arms.append([list(ds),list(A),list(B),cross,min(sum(C[a]for a in A),sum(C[b]for b in B),cross)])
    eq(native['all_four_Q_arm_bounds'],arms,'all2310 native arm partitions')
    mixed=[]
    for f in D:
        for pair in combinations([d for d in D if d!=f],2):
            for O in ((pair[0],),(pair[1],),pair):
                A=[d for d in pair if d not in O];cross=sum(C[lcm(o,a)]for o in O for a in A);qs=[[q,min(C[q],sum(C[lcm(o,q)]for o in O))]for q in D]
                # Native uses the weaker individual sum for O; independently audit it.
                mixed.append([f,list(pair),list(O),A,cross,qs,C[f]+30+min(sum(C[d]for d in O),cross+max(v[1]for v in qs))])
    eq(native['all_HQQ_HHQ_bounds'],mixed,'whole1485 conservative native mixed rows')
    inventory=[]
    for f,ab,gh,q,total in own['remaining_inventory']:
        inventory.append([f,ab,gh,q,UB[tuple(ab)],C[lcm(*gh)],C[lcm(f,q)],total])
    eq(native['all_special_HHQQ_HQ_original_inventory_bounds'],inventory,'all1485 original final inventories')
    eq(native['special_inventory_rows_reaching177'],[v for v in inventory if v[-1]>=177],'only surviving original inventory')
    eq(sorted(native['all_eight_two_parent_type_cases']),sorted(v[:5]for v in own['type_rows']),'all34 terminal types')
    local=[]
    for r,types,rows in own['all_raw_local_types']:
        for vs,filled,h,q in rows:
            halves=0
            for state,t in zip(vs,types):
                if t=='H':halves|=state
            local.append([r,types,vs,filled,halves==15])
    eq(sorted(native['complete_local_binary_controls']),sorted(local),'all10980 local controls')
    raw_final=0
    for r,ms,placed in ((2,(48,144,96,288),(16,2)),(6,(80,160),(32,6))):
        points=[n for n in R if n%8==r];ones=(1<<len(points))-1
        def quarter(m,a):return [sum(1<<j for j,n in enumerate(points)if(n+2520*k)%m==a)for k in range(4)]
        pc=quarter(*placed);pm={m:{a:quarter(m,a)for a in range(r,m,8)}for m in ms};counts=[]
        for aa in product(*(range(r,m,8)for m in ms)):
            layers=list(pc)
            for m,a in zip(ms,aa):
                for k in range(4):layers[k]|=pm[m][a][k]
            z=ones
            for v in layers:z&=v
            counts.append(z.bit_count())
        block=native['parent'+str(r)+'_full_original_phase_block'];fresh=next(v for v in own['final_phases']if v['parent']==r)
        eq(block,{'parent':r,'original_moduli':list(ms),'phase_lists':[list(range(r,m,8))for m in ms],'all_raw_phase_repair_counts':counts,'qualifying_phase_tuples':[v[0]for v in fresh['qualifying']]},'ENTIRE physical phase block '+str(r));raw_final+=len(counts)
    labels=[v[0]for v in own['BASE_gluing'][0]['labels']];glue=[]
    for c in range(5):
        shape=[n for n in R if n%8==2 or(n%8==6 and n%5==c)];S=set(shape);blocks=[]
        for m in labels:
            rows=[[0,0]for a in range(m)]
            for n in R:rows[n%m][0 if n in S else 1]+=1
            blocks.append([m,rows,max(b for a,b in rows if a<=3)])
        glue.append({'c':c,'protected_shape':shape,'shape_size':len(shape),'outside_holes':len(R)-len(shape),'all_original_phase_rows':blocks,'restricted_sum_max_outside':sum(v[-1]for v in blocks)})
    eq(native['all_five_BASE_gluing_shapes'],glue,'EVERY original46255 protected/outside phase entry')
    third=native['three_parent_reduction'];phase_rows=[];maxima={}
    for r in (1,2,3,4,5,6,7):
        for d in [1]+D:
            pops=[sum(n%d==a for n in R if n%8==r)for a in range(d)]
            phase_rows.append([r,d,pops]);maxima[r,d]=max(pops)
    eq(third['whole_physical_phase_rows'],phase_rows,'all seven physical parent populations')
    coupling=[]
    for r in (1,3,4,5,7):
        for gh in combinations(D,2):
            for abc in combinations([d for d in D if d not in gh],3):
                a=maxima[r,lcm(*gh)];b=sum(C[d]for d in abc);coupling.append([r,*gh,*abc,a,b,a+b])
    eq(third['all_global_five_extra_H_coupling_rows'],coupling,'all23100 physical-parent labelled couplings')
    thirdlocal=[[r,t,vs,filled]for r,t,rows in own['third_local_states']for vs,filled,h,q in rows]
    eq(third['complete_literal_three_class_controls'],thirdlocal,'all1360 third physical controls')
    cases=[];tags=('HHQ','HQQ','QQQ','HH / HQ','HQ / HQ','QQ / HQ','HHH','HHQ','HQQ')
    for r in (1,3,4,5,7):
        source=[v for v in own['three_parent_allocations']if v[0]==r]
        cases.extend([[r,'+'.join(map(str,v[1])),tag,v[-1]]for v,tag in zip(source,tags)])
    eq(third['all_three_parent_eight_tail_cases'],cases,'all45 original allocation bounds')
    # Explicitly audit all remaining domain/claim metadata, not author spelling.
    for record in (native,third):
        eq(sorted(record['full_marked_prefix']),sorted(own['scope']['prefix']),'literal prefix');eq(record['essential_originals_explicit'],[16,32],'author essential domain')
        for key in ('capacity_sharpness_claimed','ordinary_proof_formalized','independent_reviewer','global_bound_changed'):eq(record[key],False,key)
    eq(native['original_moduli_divide'],10080,'original period');eq(native['minimum_modulus_exactly'],8,'minimum');eq(native['actual_LCM_may_divide10080'],True,'LCM divisor');eq(native['new_productive_TAIL_lower_bound'],9,'new bound');eq(native['at_least_eight_productive_TAILs_imported_from_public9978'],True,'explicit old dependency')
    for record in (native,third):eq(record['BASE_holes_lower_bound_imported_from_public9934'],177,'credited lower hole bound')
    eq(third['coupled_maxima'],{str(r):max(v[-1]for v in coupling if v[0]==r)for r in (1,3,4,5,7)},'whole coupling maxima');eq(third['maximum_three_parent_eight_tail_BASE_holes'],176,'three parent maximum');eq(third['remaining_two_parent_counts'],[[2,6],[3,5],[4,4],[5,3]],'complete remaining counts');eq(third['exactly_eight_productive_TAILs_imply_exactly_two_hole_parents'],True,'scope')
    return {'status':'COMPLETE_POST_SEAL_NATIVE_CORRESPONDENCE','whole_own_record_sha256':hashlib.sha256(wire(own)).hexdigest(),'whole_native_record_sha256':hashlib.sha256(wire(native)).hexdigest(),'whole_field_comparisons':checked,'native_raw_H_union_entries':raw_H,'raw_original_final_phase_entries':raw_final,'raw_BASE_phase_entries':46255,'native_global_H_coupling_rows':23100,'native_code_imported':False,'format_blind':False,'native_mixed_individual_sum_relaxation_explicitly_rebuilt':True,'trust':'post-seal native format exposed; does not replace pre-native independent kernels/ordinary proof'}

if __name__=='__main__':print(wire(check(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))).decode())
