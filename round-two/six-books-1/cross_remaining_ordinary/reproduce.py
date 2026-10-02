"""Exact corroboration of PROOF.md from the already proved T2=C.

The complete ordinary theorem composes written lemmas 9795 and 9685.
This program neither imports those proofs as data nor replaces them.
Standard Python only; no solver, census, imported verdict, or floating point.
"""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import time
import literal
import rules as R

START = time.monotonic()

def require(test,message):
    if not test:
        raise ValueError(message)

def guard():
    if time.monotonic()-START>30:
        raise RuntimeError('30s phase guard: incomplete is not an exclusion')

def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def core(r,rows,sy):
    red,d,q = R.build(r,rows,sy)
    sets,ld,lq = literal.build(r,rows,sy)
    require(tuple(sum(1<<j for j in s) for s in sets)==red
            and d==ld and q==lq,'whole literal/coordinate core equality')
    caps = R.allowances(red,d)
    require(caps==literal.allowances(sets,ld),
            'all 120 physical colored-spine allowances agree')
    return red,d,q,caps

def union_cut(q,caps,i,j,z):
    require(q[i]+q[j]-6==caps[i,j], 'specified pair forces Q union')
    require(q[z]>caps[z,i]+caps[z,j], 'specified ordinary union contradiction')
    return [i,j,z,q[z],caps[z,i],caps[z,j]]

def run():
    covers = [w for w in range(64) if R.covers(w)]
    missing = [w for w in range(64) if R.independent(w)]
    require(len(covers)==18 and covers==[63^w for w in reversed(missing)],
            'whole covers/complementary missing sets')
    base,bd,bq,_ = core(0,(R.H,R.K,R.C),(R.P,R.S))
    nu = set(range(1,11))
    inside = sum((base[i]&sum(1<<j for j in nu)).bit_count() for i in nu)//2
    require(inside==13 and sum(bd[i] for i in nu)==99,'cut equality inputs')
    require((bq[11:16],bq[9:11],bq[:3])==((2,2,3,2,3),(4,4),(0,6,0)),
            'four-regular cut row ranks')

    # Whole two-endpoint row domain for the six-cycle union identities.
    cycles = []
    for i,j in R.CYCLE:
        records = []
        for di,dj in product(range(32),repeat=2):
            if (bool(di&16)!=(i<2) or bool(dj&16)!=(j<2)
                or di.bit_count()>(4 if i<2 else 3)
                or dj.bit_count()>(4 if j<2 else 3)):
                continue
            qi = (7 if i<2 else 6)-di.bit_count()
            qj = (7 if j<2 else 6)-dj.bit_count()
            known = 1+(di&dj).bit_count()
            words = [(1<<i if di>>k&1 else 0)|(1<<j if dj>>k&1 else 0)
                     for k in range(4)]
            sets,_,lq = literal.build(0,(*words[2:],R.C),tuple(words[:2]))
            require(known==len(sets[i+3]&sets[j+3])
                    and (qi,qj)==(lq[i+3],lq[j+3]),
                    'literal pages/ranks on the whole cycle row domain')
            possible = known+max(0,qi+qj-6)<=3
            target = 31 if i<2 or j<2 else 15
            require(possible==((di|dj)==target),'full endpoint row-union equivalence')
            if possible:
                require(known+(qi+qj-6)==3,'cycle Q union is tight')
            records.append([di,dj,qi,qj,known,possible])
        cycles.append({'edge':[i,j],'records':len(records),
                       'admissible':sum(x[-1] for x in records),'sha256':digest(records)})

    A = [w for w in covers if R.independent(w,R.PATH_A)]
    D = [w for w in covers if R.independent(w,R.PATH_D)]
    require(A==[R.P,R.H,R.S] and D==[R.P,R.K,R.S],
            'whole path-cover descriptions')
    tpairs = [[a,d] for a,d in product(A,D) if a|d==63]
    require(tpairs==[[R.P,R.S],[R.H,R.K],[R.S,R.P]],'whole three T-cover pairs')
    path_bounds = []
    # Check the occurrence argument on every doubled restricted edge.
    for endpoint,paths in ((13,R.PATH_A),(14,R.PATH_D)):
        records = []
        for w in covers:
            for i,j in paths:
                if not ((w>>i&1) and (w>>j&1)):
                    continue
                for u,v in product(covers,repeat=2):
                    rows = (w,R.K,R.C) if endpoint==13 else (R.H,w,R.C)
                    sets,_,_ = literal.build(0,rows,(u,v))
                    known = len(sets[endpoint]&sets[i+3])+len(sets[endpoint]&sets[j+3])
                    require(known>=(4 if endpoint==13 else 5),
                            'literal doubled-edge path contradiction bound')
                    records.append([w,i,j,u,v,known])
                guard()
        path_bounds.append({'endpoint':endpoint,'records':len(records),
                            'minimum_known_sum':min(x[-1] for x in records),
                            'whole_records_sha256':digest(records)})
    t_cuts = []
    transports = []
    for a,d in tpairs:
        records = []
        for u,v in product(covers,repeat=2):
            red,deg,q,caps = core(0,(a,d,R.C),(u,v))
            if (a,d)!=(R.H,R.K):
                x = 5 if a==R.P else 7
                records.append([u,v,*union_cut(q,caps,10,13,x)])
            for which in ('phi','psi'):
                p = R.permutation(which)
                rows = tuple(R.row_transport(w,p) for w in (a,d,R.C))
                sy = tuple(R.row_transport(w,p) for w in (u,v))
                nr,nd,nq,_ = core(which=='psi',rows,sy)
                require(all(nd[p[i]]==deg[i] and nq[p[i]]==q[i]
                    and nr[p[i]]==sum(1<<p[j] for j in range(16) if red[i]>>j&1)
                    for i in range(16)),'whole colored core/rank/degree transport')
                transports.append([a,d,u,v,which,rows,sy])
            guard()
        if records:
            t_cuts.append({'T_rows':[a,d,R.C],'SY_pairs':len(records),
                'minimum_deficit':min(x[-3]-x[-2]-x[-1] for x in records),
                'whole_records_sha256':digest(records)})

    us = [w for w in covers if (w&R.K).bit_count()<=2]
    vs = [w for w in covers if (w&R.K).bit_count()<=2 and (w&R.H).bit_count()<=2]
    require(us==[R.P,R.H,45,R.S,58,R.L] and vs==[R.P,R.S,R.L],
            'whole six SY0 and three SY1 cover descriptions')
    require(all((u&R.K).bit_count()==2 for u in us),'saturated SY0--T1')
    for u,v in product(us,vs):
        _,_,q,b = core(0,(R.H,R.K,R.C),(u,v))
        require(b[11,14]==b[14,15]==0 and q[11]==2 and q[14]==2 and q[15]==3,
                'rank-forced SY0/T2 intersection')
        if u==R.H:
            require(b[11,15]==0,'H has contradictory empty SY0/T2 intersection')
    four_pages = []
    for m in missing:
        first = next(i for i in (2,5) if not (m>>i&1))
        second = next(i for i in (3,4) if not (m>>i&1))
        red,_,_,_ = core(0,(R.H,R.K,R.C),(R.L,R.P))
        pages = (1,15,3+first,3+second)
        q_known = {1,15}|{3+i for i in range(6) if not (m>>i&1)}
        require(len(set(pages))==4 and all(red[11]>>p&1 and p in q_known for p in pages),
                'L gives four distinct physical red pages')
        four_pages.append([m,list(pages)])

    us = [u for u in us if u not in (R.H,R.L)]
    sy_pairs = [[u,v] for u,v in product(us,vs) if (u|v).bit_count()>=5]
    require(sy_pairs==[[13,50],[13,60],[45,50],[45,60],
                      [50,13],[50,60],[58,13],[58,60]],'whole eight SY union cases')
    cuts = []
    for u,v in ((R.P,R.L),(45,R.S),(45,R.L)):
        red,deg,q,b = core(0,(R.H,R.K,R.C),(u,v))
        if u==R.P:
            witness = union_cut(q,b,13,8,12)
        else:
            witness = union_cut(q,b,3,8,5)
        p = R.permutation('phi')
        tu,tv = (R.row_transport(w,p) for w in (u,v))
        _,_,tq,tb = core(0,(R.H,R.K,R.C),(tu,tv))
        tw = union_cut(tq,tb,*(p[i] for i in witness[:3]))
        cuts.append({'SY':[u,v],'witness':witness,'phi_SY':[tu,tv],'phi_witness':tw})
    excluded = {tuple(z[k]) for z in cuts for k in ('SY','phi_SY')}
    terminal = [p for p in sy_pairs if tuple(p) not in excluded]
    require(terminal==[[R.P,R.S],[R.S,R.P]],'exact two terminal ordered SY patterns')

    # Meaningful damages: label bridge, actual r, one cycle edge, red cap.
    damaged_map = list(literal.OLD_MAP)
    damaged_map[4],damaged_map[5] = damaged_map[5],damaged_map[4]
    try:
        literal.build(0,(R.H,R.K,R.C),(R.P,R.S),damaged_map)
    except ValueError:
        rejected_map = True
    else:
        rejected_map = False
    require(rejected_map,'damaged literal labeling must be rejected')
    require(R.build(0,(R.H,R.K,R.C),(R.P,R.S))[0]
            !=R.build(1,(R.H,R.K,R.C),(R.P,R.S))[0],
            'actual r choice cannot be silently collapsed')
    damaged_edges = tuple(e for e in R.CYCLE if set(e)!={2,5})
    require(R.independent(36,damaged_edges) and not R.independent(36),
            'dropping 25 admits the missing pair and loses the four-page argument')
    red,deg,q,b = core(0,(R.H,R.K,R.C),(R.P,R.L))
    require(q[12]>b[12,13]+b[12,8] and q[12]<=b[12,13]+b[12,8]+2,
            'loosening both red caps loses the terminal SY union cut')
    guard()
    return {'agent':'six-books-1','role':'researcher',
        'status':'same-author exact corroboration of ordinary remaining-row proof',
        'execution_boundary':'starts from T2=C; written9795 and9685 are external ordinary theorem dependencies',
        'cut':{'Nu_edges':inside,'Nu_degree_sum':99,'Nu_cut':63,'E_minus_B_edges':86,
               'B_order':11,'B_degree':4,'forced_E':108},
        'whole_C6_covers':covers,'whole_independent_missing_sets':missing,
        'six_cycle_union_identities':cycles,'T0_path_cover_rows':A,'T1_path_cover_rows':D,
        'whole_literal_doubled_edge_bounds':path_bounds,
        'whole_T_pairs':tpairs,'nonterminal_T_joint_cuts':t_cuts,
        'whole_core_transports':{'records':len(transports),'sha256':digest(transports),
                                  'all_120_spines_compared_per_core':True},
        'SY0_six_covers':[13,43,45,50,58,60],'SY1_three_covers':vs,
        'H_exclusion':'forced SY0/T2 intersection contradicts red saturated spine',
        'L_four_page_witnesses':four_pages,'whole_eight_SY_cases':sy_pairs,
        'representative_and_phi_joint_cuts':cuts,'terminal_SY_rows':terminal,
        'terminal_cores':[[r,list((R.H,R.K,R.C) if r==0 else (R.K,R.H,R.C)),sy]
                          for r in (0,1) for sy in terminal],
        'semantic_damages':{'old_label_bridge_rejected':True,'actual_r_not_collapsed':True,
             'cycle_edge_drop_loses_four_pages':True,'red_cap_loosen_loses_joint_cut':True},
        'solver_used':False,'external_census_input':False,'floating_point_math':False,
        'formalized':False,'independent_review_of_new_proof':'pending'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check',type=Path)
    args = p.parse_args()
    raw = canonical(run())
    if args.check:
        require(raw==args.check.read_bytes(),'entire canonical expected record differs')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(raw)
    print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                      'wall_seconds':time.monotonic()-START,'guard_seconds':30}))

if __name__=='__main__':
    main()
