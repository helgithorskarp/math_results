"""Independent bitset-clique input audit and direct permutation orbit audit.
Does not import problem.py or trust proof-free UNSAT result metadata.
"""
from pathlib import Path
from itertools import combinations,permutations
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def decoded_core():
    d=json.loads((HERE/'CORE.json').read_text());line=d['graph6'];need(len(line)==19 and ord(line[0])-63==15,'core order')
    word=0
    for ch in line[1:]:
        v=ord(ch)-63;need(0<=v<64,'graph6 alphabet');word=64*word+v
    need(word&7==0,'core padding')
    return {(i,j):(word>>(107-j*(j-1)//2-i))&1 for j in range(1,15) for i in range(j)}

def geometry(rep):
    fixed=decoded_core()
    for block in [range(15,19),range(19,23)]:
        for e in combinations(block,2):fixed[e]=0
    for i in range(4):
        for j in range(4):fixed[15+i,19+j]=rep>>(4*i+j)&1
    free=[e for e in combinations(range(23),2) if e not in fixed]
    return fixed,free,{e:i+1 for i,e in enumerate(free)}

def clique_sets(adj,size):
    def grow(prefix,candidates,left):
        if left==0:yield tuple(prefix);return
        while candidates.bit_count()>=left:
            bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
            yield from grow(prefix+[v],candidates&adj[v],left-1)
    yield from grow([], (1<<len(adj))-1,size)

def literal_formula(rep):
    fixed,free,var=geometry(rep);rows=[];supports=[]
    for size,color in [(4,1),(5,0)]:
        adj=[0]*23
        for u,v in combinations(range(23),2):
            if (u,v) not in fixed or fixed[u,v]==color:adj[u]|=1<<v;adj[v]|=1<<u
        for S in clique_sets(adj,size):
            row=[(-1 if color else 1)*var[e] for e in combinations(S,2) if e in var]
            rows.append(row);supports.append((S,color))
    raw=(f'p cnf 120 {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode()
    return raw,rows,supports

def orbit_audit(records):
    ps=list(permutations(range(4)));covered=set();counts=[];images_by_rep={}
    forbidden=[]
    for S in combinations(range(8),5):
        forbidden.append(sum(1<<(4*i+(j-4)) for i,j in combinations(S,2) if i<4<=j))
    allowed={w for w in range(65536) if all(w&mask for mask in forbidden)}
    for item in records:
        rep=item['representative'];images=set()
        for rp in ps:
            for cp in ps:
                w=sum((rep>>(4*rp[i]+cp[j])&1)<<(4*i+j) for i in range(4) for j in range(4))
                tr=sum((rep>>(4*rp[j]+cp[i])&1)<<(4*i+j) for i in range(4) for j in range(4))
                images.update([w,tr])
        need(min(images)==rep and len(images)==item['orbit_size'],'orbit minimum/size')
        need(images<=allowed and not(images&covered),'orbit disjointness or invalid matrix')
        covered|=images;images_by_rep[rep]=images;counts.append(len(images))
    need(covered==allowed and len(allowed)==37823 and len(records)==97,'complete pair-domain cover')
    return images_by_rep

def check_tail(rep,word):
    need(type(word) is str and len(word)==136 and set(word)<=set('01'),'tail witness syntax')
    fixed=decoded_core()
    for block in [range(15,19),range(19,23)]:
        for e in combinations(block,2):fixed[e]=0
    free=[e for e in combinations(range(23),2) if e not in fixed]
    fixed.update({e:int(word[i]) for i,e in enumerate(free)})
    for i in range(4):
        for j in range(4):need(fixed[15+i,19+j]==(rep>>(4*i+j)&1),'witness pair type')
    for size,color in [(4,1),(5,0)]:
        adj=[0]*23
        for (u,v),c in fixed.items():
            if c==color:adj[u]|=1<<v;adj[v]|=1<<u
        need(next(clique_sets(adj,size),None) is None,'invalid literal tail witness')
    return True

def checked_proof(cnf,proof,checker):
    need(Path(proof).is_file(),'missing actual proof bytes')
    p=subprocess.run([str(checker),str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    need(p.returncode==0 and b's VERIFIED' in p.stdout,'UNSAT proof rejected')
    return {'proof_sha256':hashlib.sha256(Path(proof).read_bytes()).hexdigest(),'checker_output_sha256':hashlib.sha256(p.stdout).hexdigest()}

def verify(run=None,checker=None):
    expected=json.loads((HERE/'EXPECTED.json').read_text());records=expected['results'];images=orbit_audit(records)
    if run:
        need(checker is not None,'a real proof checker is required for admission')
        run=Path(run);actual=json.loads((run/'RESULT.json').read_text());need(actual['cases']==97 and len(actual['results'])==97,'incomplete run')
        records=actual['results']
        need([(r['representative'],r['status'],r['cnf_sha256']) for r in records]==[(r['representative'],r['status'],r['cnf_sha256']) for r in expected['results']],'run decisions/input identities')
    negative=positive=undecided=clauses=0;closed_words=set();retained=[];proof_receipts=[];proof_jobs=[]
    for index,r in enumerate(records):
        need(r['orbit_index']==index and r['core']==4,'scope/index');rep=r['representative'];raw,rows,_=literal_formula(rep)
        need(hashlib.sha256(raw).hexdigest()==r['cnf_sha256'] and len(rows)==r['clauses'] and r['variables']==120,'literal formula identity')
        clauses+=len(rows)
        if run:need((run/f'orbit-{index:03d}/input.cnf').read_bytes()==raw,'actual input mismatch')
        if r['status']=='SAT_TAIL_ONLY':
            check_tail(rep,r['physical_tail_word']);positive+=1;retained.append(rep)
        elif r['status']=='TAIL_UNDECIDED':
            need(rep==65535,'undeclared unresolved tail');undecided+=1;retained.append(rep)
        else:
            need(r['status']=='UNSAT_CHECKED','unsupported status');closed_words|=images[rep]
            if run:
                p=run/f'orbit-{index:03d}/proof.drat';need(hashlib.sha256(p.read_bytes()).hexdigest()==r['proof_sha256'],'proof manifest')
                proof_jobs.append((rep,run/f'orbit-{index:03d}/input.cnf',p))
    def check_one(job):
        rep,cnf,proof=job;receipt=checked_proof(cnf,proof,checker);receipt['representative']=rep;return receipt
    if run:
        with ThreadPoolExecutor(max_workers=2) as pool:proof_receipts=list(pool.map(check_one,proof_jobs))
        negative=len(proof_receipts)
    return {'status':'VERIFIED_COMPLETE_PHYSICAL_SUBDIVISION' if run else 'VERIFIED_ORBITS_ENCODINGS_AND_TAILS_ONLY','original_task':'bo1-q7-r5-c000004','orbit_classes':97,'pair_domain_size':37823,'physical_clauses_audited':clauses,'negative_proofs_checked':negative,'reported_negative_classes':97-positive-undecided,'positive_tail_witnesses_checked':positive,'undecided_tail_classes':undecided,'closed_matrix_words':len(closed_words) if run else None,'retained_representatives':retained,'retained_matrix_words':37823-len(closed_words) if run else None,'original_task_status':'UNKNOWN','original_tasks_excluded':0,'full43_candidate':False,'proof_receipts':proof_receipts}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run');p.add_argument('--drat-trim');p.add_argument('--output');a=p.parse_args();r=verify(a.run,a.drat_trim)
    if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='proof_receipts'},sort_keys=True))
