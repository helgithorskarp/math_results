"""Deterministic controls for every routed stratum, broad cores and proof scope."""
from pathlib import Path
from itertools import combinations
import argparse,copy,json,random,sys
from common import HERE,Q8,COUNTS,need,word,matrix,source_geometry,mono,core_guards,dependencies
from transport import transport
from verify_transport import check
from registry import ranges
sys.path.insert(0,str(Q8))
import basis,worker
from join import exact_job,drat_job

def simple_source(q,r,c,data):
    line=(Path(data)/f'r44_{43-4*q}.g6').read_bytes().splitlines()[c]
    n=43-4*q;bits=[(x-63)>>b&1 for x in line[1:] for b in range(5,-1,-1)]
    a=[[0]*43 for _ in range(43)]
    for b in range(r):
        for u,v in combinations(range(4*b,4*b+4),2):a[u][v]=a[v][u]=1
    for k,(i,j) in enumerate((i,j) for j in range(1,n) for i in range(j)):a[4*q+i][4*q+j]=a[4*q+j][4*q+i]=bits[k]
    return dict(word(a),task=f'bo1-q{q}-r{r}-c{c:06d}',carrier_to_input=list(range(43)))

def relabel(source,rng):
    a=matrix(source);p=list(range(43));rng.shuffle(p);aa=[[0]*43 for _ in range(43)]
    for u,v in combinations(range(43),2):aa[p[u]][p[v]]=aa[p[v]][p[u]]=a[u][v]
    return dict(word(aa),task=source['task'],carrier_to_input=[p[x] for x in source['carrier_to_input']])

def reject(call):
    try:call()
    except (ValueError,KeyError,TypeError,IndexError):return 1
    raise ValueError('corrupt or out-of-scope control was accepted')

def main(data,queue,output,checker):
    dependencies();output=Path(output);output.mkdir(exist_ok=False);rng=random.Random(5532001)
    fixtures=json.loads((HERE/'MIXED_CONTROLS.json').read_text())
    for row in ranges():
        q,r=row['q'],row['r']
        if q>=8 and row['route']=='Q8_PHYSICAL':
            for c in [0,COUNTS[q]-1]:fixtures.append(simple_source(q,r,c,data))
    results=[];corruptions=0;broad=0;source_strata=set()
    for i,base in enumerate(fixtures):
        for variant,src in enumerate([base,relabel(base,rng)]):
            packet=transport(src,data,queue);receipt=check(src,packet,data,queue)
            need(receipt['status']=='COMPLETE_Q8_PHYSICAL_TRANSPORT_VERIFIED','control did not exercise transport')
            a,q,r,c,blocks,C=source_geometry(src);source_strata.add((q,r));aa=matrix(packet['graph'])
            blue4=mono(aa,list(range(32,43)),4,0)
            if q>=9:need(blue4 is not None,'absorbed blue block must violate core catalog membership');broad+=1
            need(mono(a,list(range(43)),5,0) is not None or mono(a,list(range(43)),5,1) is not None,'fixtures must not masquerade as good43')
            (output/f'{i:02d}-{variant}-source.json').write_text(json.dumps(src,sort_keys=True)+'\n')
            (output/f'{i:02d}-{variant}-packet.json').write_text(json.dumps(packet,sort_keys=True)+'\n')
            results.append(dict(receipt,source_q=q,source_r=r,source_core=c,core_contains_blue4=blue4 is not None))
            for mode in range(6):
                bad=copy.deepcopy(packet)
                if mode==0:bad['new_to_old'][0]=bad['new_to_old'][1]
                elif mode==1:bad['graph']['red_hex']=format(int(bad['graph']['red_hex'],16)^1,'0226x')
                elif mode==2:bad['original_task_unsat']=True
                elif mode==3:bad['source_task']='bo1-q7-r7-c000000'
                elif mode==4:bad['core_assumptions'][0]*=-1
                else:bad['destination_core_catalog_membership_required']=True
                corruptions+=reject(lambda:check(src,bad,data,queue))
    # Every wholly retained original stratum must be refused by this route.
    for row in ranges():
        if row['route']=='ORIGINAL_PARENT':
            src=simple_source(row['q'],row['r'],0,data)
            corruptions+=reject(lambda:transport(src,data,queue))
    # A real positive RUP proof on a deliberately impossible core. It covers no
    # complete catalog cohort, and must not enter target admission.
    corevars=sorted(basis.VARIABLES[e] for e in combinations(range(32,36),2));r=8
    meta=worker.metadata(r);target=set(-x for x in corevars);clauseid=None
    for ident,clause in enumerate(basis.read_cnf(Path(queue)/'q8-r8.cnf'),1):
        if set(clause)==target:clauseid=ident;break
    need(clauseid is not None,'literal red core K4 clause')
    proof=[{'clause':[],'hints':list(range(meta['clauses']+1,meta['clauses']+7))+[clauseid]}]
    job={'r':8,'core_assumptions':corevars,'edge_cube':[119]};cert=worker.wrap(job,proof);worker.verify(queue,cert)
    guards=core_guards(queue);corruptions+=reject(lambda:exact_job(cert,8,guards[0]))
    bad=copy.deepcopy(cert);bad['proof'][0]['hints']=[];corruptions+=reject(lambda:worker.verify(queue,bad))
    (output/'impossible-core-positive-control.json').write_text(json.dumps(cert,indent=2)+'\n')
    # Exercise the new full-DIMACS DRAT receiving path on the same zero-cohort
    # control. This evidence is kept outside Git and never admitted as a target.
    cnf=output/'impossible-core-positive.cnf';trace=output/'impossible-core-positive.drat'
    worker.materialize(queue,job,cnf);trace.write_text('0\n')
    mask=sum(1<<(v-802) for v in corevars);drat=drat_job(queue,8,(mask,mask),cnf,trace,checker)
    corruptions+=reject(lambda:drat_job(queue,8,guards[0],cnf,trace,checker))
    # A status-only object and an unfinished original physical child are refused.
    corruptions+=reject(lambda:exact_job({'status':'UNSAT'},8,guards[0]))
    bad=copy.deepcopy(cert);bad['core_assumptions']=[(802+i)*(1 if guards[0][1]>>i&1 else -1) for i in range(55) if guards[0][0]>>i&1];bad['edge_cube']=[119,120]
    corruptions+=reject(lambda:exact_job(bad,8,guards[0]))
    need(len(source_strata)==14,'all routed strata exercised')
    return {'status':'ALL_FOURTEEN_ROUTED_STRATA_AND_PROOF_SCOPE_CONTROLS_PASSED','physical_transports':len(results),
            'routed_strata':sorted(map(list,source_strata)),'explicit_unlisted_core_transports':broad,
            'corrupt_or_out_of_scope_rejections':corruptions,'receipts':results,
            'full_base_positive_RUP_control':'VERIFIED_ONLY_ON_IMPOSSIBLE_CORE; REJECTED_FOR_COHORT_ADMISSION',
            'full_base_positive_DRAT_control':drat,
            'verified_good43':0,'original_task_exclusions':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('queue');p.add_argument('output');p.add_argument('checker');s=p.parse_args()
    print(json.dumps(main(s.catalog,s.queue,s.output,s.checker),indent=2,sort_keys=True))
