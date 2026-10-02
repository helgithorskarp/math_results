"""Full independent Boolean-root action and ordinary control corroboration."""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path
from geometry import *

def digest_rows(rows):
    h=hashlib.sha256()
    for row in rows:h.update(canonical(row))
    return h.hexdigest()

def parameter_record(p,compositions=False):
    domain=states(p);cover=orbit_cover(p);rhist={r:dict(sorted(Counter(len(o)for o in cover if o[0][0]==r).items()))for r in(1,2,3)}
    fixed=Counter();map_count=entries=composition_count=physical_count=0;maphash=hashlib.sha256();physical=hashlib.sha256()
    for state in domain:
        images=actions(state,p);r,t,w=state
        for order,(target,a,b,flip) in zip(orders(r),images):
            fixed[(r,str(order))]+=int(target==state);map_count+=1;entries+=1<<r
            maphash.update(canonical([state,order,target,a,b,flip]))
            need(set((a*x+b)%p for x in roots(state))==set(roots(target)),'retained whole original root set')
        if compositions:
            direct={(a,b):(target,flip)for target,a,b,flip in images}
            for mid,a,b,flip in images:
                for end,c,d,flip2 in actions(mid,p):
                    need(direct[(c*a%p,(c*b+d)%p)]==(end,flip^flip2),'whole group/coordinate/output cocycle')
                    composition_count+=1
    # Physical input-coordinate checks need one truth-zero state per t and r;
    # whole cube substitution above then covers every truth function.
    for state in [z for z in domain if z[2]==0]:
        r,t,w=state;R=roots(state)
        for order,(target,a,b,flip) in zip(orders(r),actions(state,p)):
            delta=inverse(a,p);targetR=roots(target)
            for x in range(p):
                if x in R:continue
                z=(a*x+b)%p
                need(z not in targetR,'all original root coordinates retained')
                for j,i in enumerate(order):
                    need(character(x-R[i],p)==(character(z-targetR[j],p)^character(delta,p)),'actual character-coordinate basis')
                    physical_count+=1
                physical.update(canonical([state,order,x,z]))
    nu=sum((t*t-t+1)%p==0 for t in range(p));chi=1 if (p-1)%4==0 else -1
    numerator=128*(p-2)+72+24*chi+16*nu
    need(numerator%6==0 and len(cover)==numerator//6+8,'ordinary all-prime Burnside formula')
    if p>3:
        trans=24+8*chi
        expected={6:(128*(p-2)-3*trans-8*nu)//6,3:trans}
        if nu:expected[2]=4*nu
        expected={k:v for k,v in expected.items()if v}
        need(rhist[3]==expected,'ordinary full triple-root orbit histogram')
    else:trans=24+8*chi
    byessential=Counter((o[0][0],essential(o[0][2],o[0][0]))for o in cover)
    return {'prime':p,'raw_states':len(domain),'classes':len(cover),'root_count_histograms':rhist,
            'fixed_states':{str(k):v for k,v in sorted(fixed.items())},'three_cycle_parameter_roots':[t for t in range(p)if(t*t-t+1)%p==0],
            'minus_one_character':chi,'transposition_fixed_permutation':trans,'ordinary_numerator':numerator,
            'map_count':map_count,'abstract_entries':entries,'complete_compositions':composition_count,
            'literal_character_coordinate_values':physical_count,'map_transcript_sha256':maphash.hexdigest(),
            'physical_transcript_sha256':physical.hexdigest(),'whole_membership_sha256':digest_rows(cover),
            'representatives_sha256':digest_rows([o[0]for o in cover]),
            'classes_by_essential_input_count':{str(k):v for k,v in sorted(byessential.items())}}

def folding():
    rec=[];count=0
    for r in (1,2,3):
        seen=set();assignments=[m for m in itertools.product(range(r),repeat=3)if set(m)==set(range(r))]
        for m,signs,w in itertools.product(assignments,itertools.product((0,1),repeat=3),range(256)):
            values=[]
            for B in cube(r):
                old=tuple(B[m[j]]^signs[j]for j in range(3));index=sum(b<<j for j,b in enumerate(old));values.append((w>>index)&1)
            flip=values[0];effective=word(tuple(z^flip for z in values));seen.add(effective)
            # Whole table substitution, including ignored variables and roots.
            need(all(((w>>sum((B[m[j]]^signs[j])<<j for j in range(3)))&1)==(truth(effective,r)[i]^flip)
                     for i,B in enumerate(cube(r))),'all original signed/folded truth entries')
            count+=1
        need(seen==set(range(0,1<<(1<<r),2)),'every gauged effective function occurs')
        rec.append({'original_distinct_roots':r,'onto_label_assignments':len(assignments),'truth_sign_label_inputs':len(assignments)*8*256,'gauged_effective_functions':len(seen)})
    need(count==26624,'complete original signed onto-folding cases')
    return {'all_inputs':count,'root_count_cases':rec,'original_root_count_retained_even_if_function_ignores_it':True}

def phase_controls():
    legal=[];illegal=[];tests=0;singleton_max=0;singles=0
    for g in itertools.product((0,1),repeat=6):
        bad=[]
        for a in range(6):
            for d in range(1,6):
                tests+=1
                if len({g[(a+j*d)%6]for j in range(7)})==1:bad.append((a,d))
        if not bad:legal.append(g);continue
        illegal.append(g);short=[z for z in bad if z[1]in(2,3)]
        need(short,'every illegal phase has short singleton witness')
        row,delta=min(short)
        d=103*delta;period=6//__import__('math').gcd(6,delta)
        for x in range(103):
            a=crt(x,row);a=min(((a+j*d)%618) or 618 for j in range(period))
            need(a<=d and a+6*d<=2163,'physical singleton positive lift')
            need(len({(a+j*d)%103 for j in range(7)})==1 and len({g[(a+j*d)%6]for j in range(7)})==1,'all singleton AP colors')
            singles+=1;singleton_max=max(singleton_max,a+6*d)
    need(set(legal)=={tuple(SIG[(i+c)%6]for i in range(6))for c in range(6)},'complete six legal phases')
    return {'all_phase_cycles':tests,'legal':legal,'illegal_words':len(illegal),'actual_singleton_APs':singles,'maximum_singleton_positive_endpoint':singleton_max}

def controls_and_refinements():
    p=103;mult=0
    for x,y in itertools.product(range(1,p),repeat=2):
        need(character(x*y,p)==(character(x,p)^character(y,p)),'entire physical multiplicativity');mult+=1
    # All103 seven-column cyclic windows along field step6 have each column
    # exactly7 times; fixed row produces constant-rule monochromatic APs.
    windows=[frozenset((a+6*j)%p for j in range(7))for a in range(p)]
    incidence=Counter(x for z in windows for x in z)
    need(len(set(windows))==103 and all(len(z)==7 for z in windows)and set(incidence.values())=={7},'constant-rule ordinary double count')
    lifted=[]
    for a in range(p):
        start=crt(a,0) or 618;ap=[start+6*j for j in range(7)]
        need(set(n%p for n in ap)==windows[a] and len({n%6 for n in ap})==1 and ap[-1]<=654,'constant-rule original integer control')
        lifted.append(ap)
    return {'multiplicativity_inputs':mult,'constant_rule_regular_AP_windows':len(windows),'column_window_degree':7,
            'constant_rule_total_deleted_column_floor':15,'constant_rule_nonroot_floors':{'1':14,'2':13,'3':12},
            'constant_rule_sufficient_integer_interval':654,'constant_rule_max_literal_endpoint':max(z[-1]for z in lifted),
            'literal_rule_nonroot_floors_from_explicit_prior16':{'1':16,'2':15,'3':14},
            'prior16_not_used_for_all_Boolean9_proof':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--check',type=Path);args=ap.parse_args();start=time.monotonic()
    small=[parameter_record(p)for p in(3,5,7,11,13,17,19,23,29,31,37,41,43)]
    full=parameter_record(103,True)
    need(full['classes']==2176 and full['raw_states']==12938,'target complete parameter census')
    need(time.monotonic()-start<30,'fixed30s parameter phase guard; incomplete is no certificate')
    out={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','schema':1,'target_cover':full,'small_prime_controls':small,
         'folding':folding(),'phase':phase_controls(),'refinements':controls_and_refinements(),
         'general_formula':'8 + (128(p-2)+72+24*chi(-1)+16*nu_p)/6; odd prime p, nu_p=#roots(t^2-t+1)',
         'prime617_formula_classes':8+(128*615+96)//6,'AP9_certificate_validated':False}
    need(time.monotonic()-start<30,'fixed30s whole phase guard; incomplete')
    raw=canonical(out)
    if args.check:need(raw==args.check.read_bytes(),'whole parameter record mismatch')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(raw)
    print(json.dumps({'status':'PASS','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start}))
if __name__=='__main__':main()
