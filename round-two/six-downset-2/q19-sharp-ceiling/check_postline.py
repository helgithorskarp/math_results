"""Exact full-original candidate checker; imports neither search nor recover."""
from pathlib import Path
import sys
from binding import check_current
check_current()
from encoding import F,comparison,scalar_rows,classify,schur_forms,model,physical
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time


def read_candidate(path):
    data=json.loads(Path(path).read_text());base=comparison();table={}
    for row in data['free_pair_values']:
        key=tuple(map(tuple,row['types']));v=F(row['value'])
        model.require(key==tuple(sorted(key)) and key not in table and key in base,'every distinct original invariant key')
        model.require(v-base[key]==F(row['delta']),'exact defining coordinate decoding')
        table[key]=v
    model.require(set(table)==set(base) and len(table)==143,'entire143 original real-coordinate witness')
    tau=F(data['tau']);model.require(tau==F(42901,98304)+F(1,32768),'selected NEW exact post-ceiling endpoint only')
    return table,base,tau


def audit_entries(L,den,masks,tau):
    N=303;s=61;checked=0;minimum=None;locations=[]
    z=[N*int(bool(m&1))-s for m in masks]
    for i in range(N):
        model.require(sum(L[i])==N*den and sum(v*x for v,x in zip(L[i],z))==0,
                      'all original rows and forced centered-star equations')
        for j in range(N):
            model.require(L[i][j]==L[j][i] and (not masks[i]&masks[j] or L[i][j]==s*den*int(i==j)),
                          'all original support and symmetry')
            if not masks[i]&masks[j]:
                value=F(L[i][j]-s*den*int(i==j),den)
                model.require(value>=tau,'every actual original allowed floor')
                checked+=1
                if minimum is None or value<minimum:minimum=value;locations=[(i,j)]
                elif value==minimum:locations.append((i,j))
    model.require(checked==72817 and minimum==tau,'all original floor coverage including actual loop')
    return dict(all_original_positions=N*N,all_allowed_ordered_positions=checked,
                min_Cunit_floor=str(minimum),tight_actual_positions=locations,
                all_original_row_support_floor_star_identities=True)


def full_schur(point,table,basis,reduced):
    s=61;den=point['den'];members=point['members'][1:]
    st=[i for i,v in enumerate(members) if 0 in v]
    nn=[i for i,v in enumerate(members) if 0 not in v]
    C=[[point['L'][i+1][j+1]-den for j in range(302)] for i in range(302)]
    model.require(len(st)==61 and len(nn)==241 and all(C[i][j]==den*(s*int(i==j)-1) for i in st for j in st),
                  'ENTIRE fixed singular star block')
    A=[[C[i][j] for j in nn] for i in st]
    model.require(all(sum(row[j] for row in A)==0 for j in range(241)), 'ENTIRE star-column range condition')
    energy=[[sum(row[i]*row[j] for row in A) for j in range(241)] for i in range(241)]
    R=[[s*den*C[nn[i]][nn[j]]-energy[i][j] for j in range(241)] for i in range(241)]
    model.require(all(R[i][j]==R[j][i] and R[i][j]+energy[i][j]==s*den*C[nn[i]][nn[j]]
                      for i in range(241) for j in range(241)), 'ENTIRE original Schur identity')
    qnn=[i for i,t in enumerate(point['types']) if not t[0]&1]
    newindex={old:i for i,old in enumerate(qnn)}
    nn_basis=[v for v in basis if all(i in newindex for i in v['sparse'])]
    model.require(len(nn_basis)==241 and len({(v['tag'],v['sub']) for v in nn_basis})==241,
                  'complete distinct nonstar physical basis')
    counts={tag:sum(v['tag']==tag for v in nn_basis) for tag in sorted({v['tag'] for v in nn_basis})}
    model.require(counts==dict(trivial=13,X_standard=40,Y_standard=54,XX_harmonic=27,YY_harmonic=35,XY_mixed=72),
                  'every nonstar physical multiplicity')
    scale=s*den**2;paid=0
    for v in nn_basis:
        block=reduced[v['tag']+'_lower'];t=v['sub'][0];j=block['types'].index(t)
        action=[block['matrix'][i][j]/block['metric'][i] for i in range(len(block['types']))]
        sparse={newindex[i]:x for i,x in v['sparse'].items()}
        for i,old in enumerate(qnn):
            member=point['members'][old+2];u=point['types'][old]
            observed=sum(R[i][k]*x for k,x in sparse.items())
            if v['tag']=='trivial':expected=scale*action[block['types'].index(u)]
            elif v['tag'] in ('X_standard','Y_standard'):
                start=3 if v['tag']=='X_standard' else 12
                value=int(start in member)-int(start+v['sub'][1] in member)
                expected=scale*action[block['types'].index(u)]*value if u in block['types'] else F(0)
            else:expected=scale*action[0]*v['values'][old]
            model.require(expected.denominator==1 and observed==expected.numerator,
                          'EVERY full-original Schur row/basis action, '+v['tag'])
            paid+=1
    model.require(paid==58081,'whole241-square Schur physical action coverage')
    return dict(star_block_positions=3721,star_range_column_checks=241,
                full_original_schur_identity_positions=58081,
                full_original_schur_action_positions=paid,nonstar_basis_counts=counts,
                original_Schur_num_sha256=model.digest(R),scale=str(scale),
                original_Schur_matches_every_reduced_action=True)


def run(path):
    start=time.monotonic();table,base,tau=read_candidate(path)
    parts,b=classify(base);rows=scalar_rows(table)
    xy=(0,1,1)
    GGzero={tuple(sorted((xy,t))) for t in (xy,(0,2,0),(2,0,0),(2,1,0),(4,0,0),(4,1,0),(6,0,0))}
    model.require(len(GGzero)==7 and GGzero<=set(parts['GG']),'all seven original boundary zero GG orbits')
    model.require(all(v>=tau for v in rows.values()) and all(rows[('empty',t)]==tau for t in b['bad_nn'])
                  and rows[('loop',)]==tau,'all180 scalar rows, five sharp equations')
    delta={k:table[k]-base[k] for k in table}
    model.require(all(delta[k]<0 for k in parts['KK']) and all(delta[k]==0 for k in parts['KG'])
                  and all(delta[k]==-F(1,131072) if k==(xy,xy) else delta[k]==0 if k in GGzero else delta[k]>0 for k in parts['GG']), 'all boundary sharp-pattern signs')
    forced={('empty',t) for t in b['bad_nn']}|{('loop',),('empty',xy),('proper',(0,0,1),xy),('proper',(0,1,0),xy)}
    model.require(len(forced)==8 and all(rows[k]==tau for k in forced),'all eight sharp-ceiling floor equations')
    nonforced_entry_margin=min(v-tau for key,v in rows.items() if key not in forced)
    strict_repair_margin=min([-delta[key] for key in parts['KK']]+[delta[key] for key in parts['GG'] if key not in GGzero])
    model.require(nonforced_entry_margin>=F(1,256) and strict_repair_margin>=F(1,256),
                  'quantitative full-optimizer entry/sign relative-interior margins')
    point=physical.original(table,9,10);literal=model.literal_point(table,9,10)
    model.require(all(F(point['L'][i][j],point['den'])==literal['L'][i][j] for i in range(303) for j in range(303))
                  and all(F(point['T'][i][j],point['den'])==literal['T'][i][j] for i in range(301) for j in range(301)),
                  'ENTIRE independent-within-author original matrix readers')
    masks=point['masks'];entry=audit_entries(point['L'],point['den'],masks,tau)
    model.require(len(entry['tight_actual_positions'])==3391,'EVERY3391 actual tight original floor position')
    zero_GG=0;negative_GG=0
    counts={'KK':0,'KG':0,'GG':0};P=F(0);bad_members=set(t for t in b['bad_nn'])
    nn=[i for i,v in enumerate(point['members']) if i>0 and 0 not in v]
    for at,i in enumerate(nn):
        t=model.type_of(point['members'][i],9)
        for j in nn[at+1:]:
            if masks[i]&masks[j]:continue
            u=model.type_of(point['members'][j],9);key=tuple(sorted((t,u)))
            tag='KK' if t in bad_members and u in bad_members else 'KG' if t in bad_members or u in bad_members else 'GG'
            observed=F(point['L'][i][j]-point['den'],point['den'])-base[key]
            model.require(observed==delta[key] and (observed<0 if tag=='KK' else observed==0 if tag=='KG' or (key in GGzero and key!=(xy,xy)) else observed==-F(1,131072) if key==(xy,xy) else observed>0),
                          'every ORIGINAL individual repair sign and degree coordinate')
            P+=max(observed,F(0));counts[tag]+=1
            if tag=='GG' and observed==0:zero_GG+=1
            if tag=='GG' and observed<0:negative_GG+=1
    model.require(counts==dict(KK=1800,KG=10820,GG=11245) and zero_GG==4230 and negative_GG==3240 and P==b['P0']+38*tau+810*(tau-F(42901,98304)),
                  'full23865 individual cost and exact universal lower-bound attainment')
    basis,gram=physical.complete_basis(point);actions=physical.literal_actions(point,table,basis)
    reduced=schur_forms(table);schur=full_schur(point,table,basis,reduced)
    schur_tests={tag:model.exact_ldl(block['matrix'],block['metric'],F(0)) for tag,block in reduced.items()}
    model.require(all(v['positive_definite'] for v in schur_tests.values()),'all six reduced physical Schur forms PD')
    full_tests={tag:model.exact_ldl(block['matrix'],block['metric'],F(1,1024))
                for tag,block in model.sector_forms(table,9,10).items()}
    model.require(all(v['positive_definite'] for v in full_tests.values()),'all twelve NEW exact shifted physical comparisons')
    return dict(agent='six-downset-2',role='researcher',tau=str(tau),epsilon=str(tau/242),
                P0=str(b['P0']),P=str(P),sharp_cost_attained=False,refined_piecewise_cost_bound_attained=True,
                refined_cost_excess=str(810*(tau-F(42901,98304))),
                entire143_rational_candidate_verified=True,candidate_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                original_entries=entry,individual_repair_counts=counts,original_ranks=[302,302],
                full_physical_floor='1/1024',all_other301_lower_upper_gaps='1/247808',
                min_all_nonforced_Cunit_entry_surplus=str(nonforced_entry_margin),
                min_all_unforced_strict_KK_GG_repair_sign=str(strict_repair_margin),
                seven_special_GG_orbits=sorted(GGzero),original_negative_GG_count=negative_GG,original_zero_GG_count=zero_GG,
                original_refined_line_forced_floor_positions=3391,
                all_boundary_nonforced_entry_and_unforced_repair_margins_at_least='1/256',
                full_original_L_rational_sha256=model.digest([[str(v) for v in row] for row in literal['L']]),
                full_original_T_rational_sha256=model.digest([[str(v) for v in row] for row in literal['T']]),
                complete_original_basis_and_Gram=gram,full_original_actions=actions,
                full_original_Schur=schur,all_six_Schur_PD=schur_tests,all_twelve_shifted_forms=full_tests,
                no_search_or_recovery_imported=True,no_floating_solver_status_used=True,
                ordinary_real_averaging_completeness_and_interpolation_bridges_unformalized=True,
                independently_reviewed=False,adverse_suite_not_run_by_this_single_endpoint_check=True,
                observed_seconds=time.monotonic()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();r=run(args.candidate);args.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('all_six_Schur_PD','all_twelve_shifted_forms','original_entries')}))
